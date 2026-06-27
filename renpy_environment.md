# Ren'Py Environment

## Installed SDK

- Version: Ren'Py 8.5.3
- SDK path: `C:\Users\12726\Documents\Codex\tools\renpy-sdk\renpy-8.5.3-sdk`
- SDK archive: `C:\Users\12726\Documents\Codex\tools\renpy-sdk.zip`
- Web support archive: `C:\Users\12726\Documents\Codex\tools\renpy-web.zip`

## SHA256

- `renpy-sdk.zip`: `FF57648F9C04F27E381C48AF6D8E3EE3CDEC296BED4D3831F47F09B0A71B505E`
- `renpy-web.zip`: `954DB897E65F51EA63CB2FB7B203D02BE0447F4E22069514020BBE6C6691FDFC`

## Commands

```powershell
renpy --version
renpyweb --version
renpyweb --help
```

`renpyweb` is a local command shim installed next to the Ren'Py SDK. It maps:

```powershell
renpyweb compile PROJECT OUTDIR
```

to Ren'Py web build execution.
