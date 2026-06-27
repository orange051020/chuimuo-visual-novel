# 外部美术交接清单

Codex 不生成任何图片。本文件用于外部文生图AI完成素材后，交回工程整合。

## 交付数量

- 背景图与UI底图：24 张，放入 `game/images/background/`
- 角色立绘、特写、群像：36 张，放入 `game/images/character/`
- 总计：60 张 WebP 文件

## 命名来源

所有文件名以 `game/images/asset_list.md` 为唯一准绳，大小写、下划线、拼写必须完全一致。

## 技术检查

交付后运行：

```bash
node work/tests/validate_assets_ready.js
```

该脚本检查：

- 是否缺文件
- 是否为真实 WebP 文件
- 背景/特写是否为 1920x1080
- 半身立绘是否为高度 900px
- 全身/群像是否为高度 1000px
- 角色立绘是否带透明通道
- 背景单张是否不超过 2MB
- 角色单张是否不超过 500KB

## 一票否决项

1. 出现清晰人脸、五官、面部细节。
2. 大面积纯色填充、几何方块、扁平矢量质感。
3. 高饱和鲜亮色彩。
4. 无水墨笔触、宣纸纹理、晕染过渡、做旧质感。
5. 尺寸、格式、透明通道、文件名不符合规范。
6. 出现文字、水印、现代元素、3D渲染感。

## Codex整合步骤

1. 确认全部素材放入对应目录。
2. 运行 `node work/tests/validate_assets_ready.js`。
3. 运行 `node work/tests/validate_project.js`。
4. 用 Ren'Py 启动工程，检查无缺图、无路径报错。
5. 执行 renpyweb 编译到 `build-web/`。
6. 将 `web-meta.html` 内容合并到 `build-web/index.html` 的 `<head>`。
7. 推送 GitHub，触发 Pages 部署。
