# 风暴中的大顺朝：序章《垂暮》

架空历史悬疑悲剧水墨风视觉小说网页工程。

## 当前状态

已完成：

- 项目目录与全局规则
- `spec/` 规格文档
- 新版序章 Ren'Py 剧情脚本
- 素材清单 `game/images/asset_list.md`
- Ren'Py 文字样式、对话框样式、场景转场与立绘动效代码
- GitHub Pages 部署工作流骨架
- 分享元标签模板

未完成：

- 正式美术素材导入
- Ren'Py/renpyweb 编译
- GitHub Pages 实际部署

## 美术边界

Codex 不生成任何图片、背景、立绘、UI底图或特写素材。所有 WebP 素材必须由独立文生图AI按 `game/images/asset_list.md` 产出后放入：

- `game/images/background/`
- `game/images/character/`

## 素材就位后校验

在外层工作区运行：

```bash
node work/tests/validate_assets_ready.js
node work/tests/validate_project.js
```

构建前检查：

```bash
node chuimuo-visual-novel/tools/prebuild_check.js
```

renpyweb 编译完成后注入分享元标签：

```bash
node chuimuo-visual-novel/tools/inject_web_meta.js
```

生成最终验收报告：

```bash
node chuimuo-visual-novel/tools/write_acceptance_report.js
```

## 部署

见 `deploy_notes.md`。
