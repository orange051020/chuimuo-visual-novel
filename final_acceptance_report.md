# 最终验收报告

## 剧情验收

- 李东升开口结局遗言必须为“老百姓以后会怎么样，只有天知道。”
- 默然结局不得出现李东升临终台词
- 十二年时间线、御书房争执、顾子明悬疑、赵铁栓殉道必须落地

## 美术素材验收

- 背景图与UI底图：24 张
- 角色立绘、特写、群像：36 张
- 总计：60 张 WebP 文件
- 所有素材必须通过 `node work/tests/validate_assets_ready.js`

## 功能验收

- Ren'Py 入口 `label start` 可进入 `chapter_prologue`
- 文字样式、对话框样式、选择菜单、转场定义存在
- 素材路径全部来自 `game/images/asset_list.md`

## 部署验收

- renpyweb 输出存在于 `build-web/`
- `web-meta.html` 已注入 `build-web/index.html`
- GitHub Pages workflow 使用 `build-web/` 作为发布目录
- 匿名浏览器可打开最终 URL

## 自动化检查输出

### C:\Program Files\nodejs\node.exe work/tests/validate_project.js

Exit code: 0

```text
Project validation passed.
```

### C:\Program Files\nodejs\node.exe work/tests/validate_assets_ready.js

Exit code: 0

```text
All listed assets are present and pass basic file checks: 60
```
