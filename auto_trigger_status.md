# 自动触发状态

## 美术禁令

已锁定：Codex 不得自行生成任何图片、背景、立绘素材，不得使用代码绘图、矢量色块、纯色占位图替代正式美术资产。

## 监听规则

监听目录：

```text
external-art-drop/
```

触发条件：

```text
目录内存在至少 60 个 .webp 文件
```

触发脚本：

```powershell
work/auto_asset_pipeline.ps1
```

执行顺序：

1. `node chuimuo-visual-novel/tools/import_external_assets.js --dry-run`
2. `node chuimuo-visual-novel/tools/import_external_assets.js`
3. `node work/tests/validate_assets_ready.js`
4. `node chuimuo-visual-novel/tools/prebuild_check.js`
5. `renpyweb compile chuimuo-visual-novel ./build-web`
6. `node chuimuo-visual-novel/tools/inject_web_meta.js`
7. `git add/commit`
8. `git push origin main`，仅在 origin 已配置时执行
9. `node chuimuo-visual-novel/tools/write_acceptance_report.js`

## 当前限制

GitHub CLI 当前未登录，远端仓库无法自动创建。`origin` 未配置时，自动流程会跳过 push 并写入日志。
