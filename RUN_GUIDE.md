# 运行说明 — 风暴中的大顺朝

## 一、系统要求

| 项目 | 最低要求 | 推荐 |
|------|----------|------|
| 操作系统 | Windows 7+ / macOS 10.12+ / Linux | Windows 10+ |
| Ren'Py SDK | 8.0+ | 8.5.3（开发验证版本） |
| 内存 | 512 MB | 1 GB |
| 硬盘空间 | 50 MB（含素材） | 100 MB |
| 显示分辨率 | 1280×720 | 1920×1080 |
| 音频 | 可选（当前为静音占位） | 支持音频输出 |

## 二、获取 Ren'Py SDK

1. 访问 https://www.renpy.org/latest.html
2. 下载对应系统的 SDK：
   - Windows: `renpy-8.5.3-sdk.zip`
   - macOS: `renpy-8.5.3-sdk.dmg`
   - Linux: `renpy-8.5.3-sdk.tar.bz2`
3. 解压到任意目录

## 三、启动游戏

### 方法一：通过 Ren'Py 启动器

1. 运行解压目录中的 `renpy.exe`（Windows）/ `renpy.sh`（Linux）/ `renpy.app`（macOS）
2. 在启动器界面左侧「项目」列表中，点击「+ Add Project」或直接将 `dashun-dynasty` 文件夹复制到 SDK 目录下
3. 在项目列表中选择「风暴中的大顺朝」
4. 点击「Launch Project」启动游戏

### 方法二：通过命令行

```bash
# 进入 Ren'Py SDK 目录
cd /path/to/renpy-8.5.3-sdk

# 直接运行游戏
./renpy.exe /path/to/dashun-dynasty run

# 运行 Lint 检查
./renpy.exe /path/to/dashun-dynasty lint

# 编译脚本
./renpy.exe /path/to/dashun-dynasty compile
```

## 四、游戏操作

| 操作 | 按键 | 说明 |
|------|------|------|
| 推进对话 | 鼠标左键 / 空格键 / 回车键 | 推进到下一句对话 |
| 自动推进 | A 键 | 切换自动推进模式 |
| 跳过 | Ctrl 键 / S 键 | 快速跳过已读对话 |
| 打开菜单 | 鼠标右键 / Esc 键 | 打开游戏菜单 |
| 存档 | 在菜单中选择「存档」 | 保存到 8 个槽位之一 |
| 读档 | 在菜单中选择「读档」 | 读取已保存的进度 |
| 历史回放 | 在菜单中选择「历史」 | 查看已读对话记录 |
| 设置 | 在菜单中选择「设置」 | 调节音量/文字速度/显示模式 |
| 全屏切换 | Alt+Enter | 切换窗口/全屏模式 |

## 五、游戏流程

```
启动 → 标题画面（"风暴中的大顺朝" / "垂暮"）
  → 片段一：京城市井（说书人讲述大顺律兴衰）
  → 片段二：皇城寝殿（帝王临终幻觉回忆）
  → 片段三：北方乡野（老兵殉道、消息隔绝）
  → 片段四：南方行辕（权臣复盘大局）
  → 分支选择：
      ├─ 选项A「留下最后的独白」→ 结局A：临终留憾
      └─ 选项B「无言」→ 结局B：默然离世
  → 游戏结束
```

**预计通关时间**: 15-20 分钟（单条线路）

## 六、已验证状态

本项目已在 Ren'Py 8.5.3 SDK 中通过以下验证：

| 验证项 | 结果 | 日期 |
|--------|------|------|
| Lint 静态检查 | ✅ PASS (0 错误) | 2026-06-26 |
| Compile 编译 | ✅ PASS (9 .rpyc) | 2026-06-26 |
| Run 实际运行 | ✅ PASS (10s 无错误) | 2026-06-26 |
| 素材引用校验 | ✅ PASS (18/18) | 2026-06-26 |
| 字数校验 | ✅ PASS (4,390 字) | 2026-06-26 |

## 七、注意事项

1. **音频说明**: 当前 BGM 和 SFX 为静音 WAV 占位文件，替换为实际音频时保持文件名不变即可
2. **图片说明**: 背景图和角色立绘为程序化生成的占位素材，替换为实际美术素材时保持文件名和尺寸不变
3. **存档说明**: 游戏存档保存在 `game/saves/` 目录下，首次运行会自动创建
4. **分辨率说明**: 游戏默认 1920×1080，在较低分辨率下会自动缩放

## 八、项目结构

```
dashun-dynasty/
├── AGENTS.md                 ← 项目地图
├── ASSETS.md                 ← 素材清单
├── RUN_GUIDE.md              ← 运行说明（本文档）
├── generate_assets.py        ← 素材生成脚本
├── spec/                     ← 规格文档
│   ├── spec.md               ← 主规格文档
│   ├── story-spec.md         ← 剧情规格
│   ├── art-spec.md           ← 美术规格
│   ├── technical-spec.md     ← 技术规格
│   ├── acceptance-criteria.md ← 验收标准
│   ├── test-cases.md         ← 测试用例
│   ├── test-execution-report.md ← 测试执行报告
│   └── verification-report.md   ← 验收报告
└── game/                     ← 游戏工程
    ├── script.rpy            ← 主脚本（角色/图片/转场定义）
    ├── options.rpy           ← 游戏配置
    ├── gui.rpy               ← GUI 配置
    ├── screens.rpy           ← 界面定义
    ├── story/                ← 剧情脚本
    │   ├── chapter1_market.rpy
    │   ├── chapter2_palace.rpy
    │   ├── chapter3_north.rpy
    │   ├── chapter4_south.rpy
    │   └── endings.rpy
    ├── images/               ← 图片素材
    │   ├── backgrounds/      ← 6 张背景图
    │   ├── characters/       ← 8 张角色立绘
    │   └── ui/               ← 1 张 UI 图
    └── audio/                ← 音频素材
        ├── bgm/              ← 4 个 BGM
        └── sfx/              ← 4 个 SFX
```

---

*更新日期: 2026-06-26*
*验证 SDK: Ren'Py 8.5.3.26051504*
