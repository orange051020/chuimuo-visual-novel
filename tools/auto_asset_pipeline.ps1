$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Drop = Join-Path $Root "external-art-drop"
$Log = Join-Path $Root "work\auto_asset_pipeline.log"
$RenpyPath = "C:\Users\12726\Documents\Codex\tools\renpy-sdk\renpy-8.5.3-sdk"
$env:Path = "$RenpyPath;$env:Path"

function Write-Log($message) {
    $line = "$(Get-Date -Format s) $message"
    Add-Content -LiteralPath $Log -Value $line -Encoding UTF8
    Write-Host $line
}

function Run-Step($name, $command, $arguments) {
    Write-Log "START $name"
    $process = Start-Process -FilePath $command -ArgumentList $arguments -WorkingDirectory $Root -NoNewWindow -PassThru -Wait
    if ($process.ExitCode -ne 0) {
        Write-Log "FAIL $name exit=$($process.ExitCode)"
        throw "$name failed"
    }
    Write-Log "PASS $name"
}

function Wait-Pages-Deploy {
    Push-Location (Join-Path $Root "chuimuo-visual-novel")
    try {
        $remote = git remote get-url origin 2>$null
        if ($LASTEXITCODE -ne 0 -or -not $remote) {
            Write-Log "SKIP pages wait: origin remote not configured"
            return
        }
        $head = git rev-parse HEAD
        $runId = $null
        for ($i = 0; $i -lt 30; $i++) {
            $json = gh run list --limit 10 --json databaseId,headSha,status,conclusion 2>$null
            if ($LASTEXITCODE -eq 0 -and $json) {
                $runs = $json | ConvertFrom-Json
                $match = $runs | Where-Object { $_.headSha -eq $head } | Select-Object -First 1
                if ($match) {
                    $runId = $match.databaseId
                    break
                }
            }
            Start-Sleep -Seconds 5
        }
        if (-not $runId) {
            Write-Log "SKIP pages wait: no GitHub Actions run found for $head"
            return
        }
        Write-Log "START pages deploy wait run=$runId"
        gh run watch $runId --exit-status
        if ($LASTEXITCODE -ne 0) {
            Write-Log "FAIL pages deploy wait run=$runId"
            throw "pages deploy failed"
        }
        Write-Log "PASS pages deploy wait run=$runId"
    } finally {
        Pop-Location
    }
}

function Run-Pipeline {
    Write-Log "Pipeline triggered"
    Run-Step "import dry-run" "node" @("chuimuo-visual-novel/tools/import_external_assets.js", "--dry-run")
    Run-Step "import assets" "node" @("chuimuo-visual-novel/tools/import_external_assets.js")
    Run-Step "validate assets" "node" @("work/tests/validate_assets_ready.js")
    Run-Step "prebuild check" "node" @("chuimuo-visual-novel/tools/prebuild_check.js")
    Run-Step "renpyweb compile" "renpyweb" @("compile", "chuimuo-visual-novel", "./build-web")
    Run-Step "inject web meta" "node" @("chuimuo-visual-novel/tools/inject_web_meta.js")
    Run-Step "write acceptance report" "node" @("chuimuo-visual-novel/tools/write_acceptance_report.js")
    Push-Location (Join-Path $Root "chuimuo-visual-novel")
    try {
        git add -A
        git -c user.name="Codex" -c user.email="codex@local" commit -m "build: update web release after asset import"
        $remote = git remote get-url origin 2>$null
        if ($LASTEXITCODE -eq 0 -and $remote) {
            git push origin main
            Write-Log "PASS git push"
        } else {
            Write-Log "SKIP git push: origin remote not configured"
        }
    } finally {
        Pop-Location
    }
    Wait-Pages-Deploy
    Write-Log "Pipeline completed"
}

Write-Log "Watching $Drop for 60 external WebP assets"
while ($true) {
    $count = (Get-ChildItem -LiteralPath $Drop -Filter *.webp -File -ErrorAction SilentlyContinue | Measure-Object).Count
    if ($count -ge 60) {
        $dryRun = Start-Process -FilePath "node" -ArgumentList @("chuimuo-visual-novel/tools/import_external_assets.js", "--dry-run") -WorkingDirectory $Root -NoNewWindow -PassThru -Wait
        if ($dryRun.ExitCode -eq 0) {
            try {
                Run-Pipeline
            } catch {
                Write-Log "Pipeline stopped: $($_.Exception.Message)"
            }
            break
        } else {
            Write-Log "Detected $count WebP files, but filename/format precheck failed. Waiting for corrected external assets."
        }
    }
    Start-Sleep -Seconds 10
}
