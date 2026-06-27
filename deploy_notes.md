# 部署说明

## 前置条件

1. 外部文生图AI已按 `game/images/asset_list.md` 产出全部 WebP 素材。
2. 背景素材放入 `game/images/background/`。
3. 角色与群像素材放入 `game/images/character/`。
4. 本地安装 Ren'Py 最新稳定版，并可执行 renpyweb 打包。

## 素材校验

在仓库根目录的上级工作区运行：

```bash
node work/tests/validate_assets_ready.js
```

## 编译

构建前运行：

```bash
node chuimuo-visual-novel/tools/prebuild_check.js
```

使用 Ren'Py 启动器或命令行执行 web build，将输出目录设置为：

```text
chuimuo-visual-novel/build-web/
```

编译完成后，注入分享元标签：

```bash
node chuimuo-visual-novel/tools/inject_web_meta.js
```

该脚本会读取 `web-meta.html` 并写入 `build-web/index.html` 的 `<head>`。

## GitHub Pages

1. 将 `chuimuo-visual-novel/` 推送到 GitHub 仓库 `main` 分支。
2. 在仓库 Settings -> Pages 中选择 GitHub Actions。
3. `.github/workflows/pages.yml` 会上传 `build-web/` 并部署到 Pages。

## 标准分享文案

《风暴中的大顺朝：垂暮》  
一部架空历史悬疑悲剧水墨风视觉小说。  
四段多视角碎片化叙事，单分支双结局，讲述《大顺律》十二年兴衰中理想、制度、阶层与信息差共同塑造的历史悲剧。

## 最终验收报告

部署前运行：

```bash
node chuimuo-visual-novel/tools/write_acceptance_report.js
```
