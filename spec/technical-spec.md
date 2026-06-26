# 技术规格文档 — 风暴中的大顺朝

## 一、引擎与运行环境

- **引擎**：Ren'Py 最新稳定版（8.x）
- **脚本语法**：标准 Ren'Py 脚本（.rpy）+ 少量 Python 辅助逻辑
- **运行平台**：Windows（主要）、macOS、Linux
- **打包格式**：Ren'Py 标准打包，可直接通过 SDK 启动

## 二、工程文件结构

```
game/
├── script.rpy               # 主入口：角色定义、默认值、游戏启动
├── options.rpy              # 配置：游戏名、版本、窗口尺寸
├── gui.rpy                  # GUI：色值、字体、尺寸、布局
├── screens.rpy              # 界面：主菜单、存档/读档、设置、回放、快捷菜单
├── story/
│   ├── chapter1_market.rpy  # 片段一：京城市井
│   ├── chapter2_palace.rpy  # 片段二：皇城寝殿
│   ├── chapter3_north.rpy   # 片段三：北方乡野
│   ├── chapter4_south.rpy   # 片段四：南方行辕
│   └── endings.rpy          # 双结局分支
├── images/
│   ├── backgrounds/         # 场景背景 PNG
│   ├── characters/          # 角色剪影 PNG
│   └── ui/                  # UI元素 PNG
└── audio/
    ├── bgm/                 # 背景音乐 MP3
    └── sfx/                 # 音效 OGG
```

## 三、角色定义规范（script.rpy）

```renpy
# 角色定义格式
define narrator = Character(None, what_prefix="", what_suffix="")  # 旁白
define storyteller = Character("说书人", color="#8B3A3A")  # 朱砂红
define emperor = Character("李东升", color="#5B7A8C")  # 石青灰蓝
define liusilian = Character("刘思廉", color="#8B6B4A")  # 赭石
define guziming = Character("顾子明", color="#6B4B3A")  # 深褐
define zhaotieshuan = Character("赵铁栓", color="#6B6B5A")  # 枯灰
```

## 四、场景切换与转场规范

```renpy
# 场景背景切换
scene bg_palace with ink_transition

# 转场定义（在 script.rpy 或单独的 transitions.rpy 中）
define ink_transition = ImageDissolve("images/ui/ink_mask.png", 1.5, ramplen=256)
define scroll_transition = ImageDissolve("images/ui/scroll_mask.png", 2.0, ramplen=128)
```

## 五、分支逻辑规范

```renpy
# 结尾分支（endings.rpy）
label ending_choice:
    menu:
        "留下最后的独白。":
            jump ending_a
        "无言。":
            jump ending_b
```

## 六、存档/读档规范

- 使用 Ren'Py 内置存档系统（`renpy.save` / `renpy.load`）
- 存档槽位：默认 4×2 = 8 个（可扩展）
- 自动存档：每个章节开始时触发 `$ renpy.force_autosave()`
- 快速存档：快捷菜单提供按钮

## 七、GUI 配置规范（gui.rpy）

### 色值映射
```renpy
define gui.text_color = "#2C2C2C"          # 主色墨黑 — 正文文字
define gui.idle_color = "#5B7A8C"           # 石青灰蓝 — 按钮常态
define gui.hover_color = "#8B3A3A"          # 朱砂红 — 按钮悬停
define gui.selected_color = "#A0524F"       # 朱砂浅 — 选中态
define gui.insensitive_color = "#8B8B7A"    # 枯灰 — 禁用态
define gui.frame_color = "#D4C5A9"          # 绢黄旧纸 — 面板底色
define gui.background_color = "#1A1A1A"     # 深墨黑 — 纯背景
```

### 字体配置
```renpy
define gui.text_font = "gui/font/fangsong.ttf"       # 仿宋 — 正文
define gui.name_text_font = "gui/font/xingkai.ttf"    # 行书 — 角色名
define gui.interface_text_font = "gui/font/kaiti.ttf" # 楷书 — 界面
define gui.title_text_font = "gui/font/lishu.ttf"     # 隶书 — 标题
```

## 八、界面定义规范（screens.rpy）

### 必须实现的界面
1. **main_menu** — 主菜单（开始游戏、读档、设置、退出）
2. **game_menu** — 游戏内菜单（存档、读档、设置、回放、主菜单）
3. **save** — 存档界面（缩略图、时间戳、槽位）
4. **load** — 读档界面（同存档布局）
5. **preferences** — 系统设置（音量、文字速度、自动推进、窗口/全屏）
6. **history** — 文本回放（历史对话记录）
7. **quick_menu** — 快捷菜单（存档、读档、设置、跳过、自动、回放）
8. **say** — 对话界面（角色名 + 文本框）
9. **choice** — 选项界面（朱砂印章风格）

## 九、代码规范

1. 每个 .rpy 文件顶部添加注释标明片段名称与用途
2. label 命名规范：`chapter1_market`、`chapter2_palace`、`ending_a`、`ending_b`
3. 图片命名规范：`bg_<场景名>`、`char_<角色名>`、`ui_<元素名>`
4. 音频命名规范：`bgm_<片段名>`、`sfx_<效果名>`
5. 禁止使用 `call` 嵌套超过3层
6. 所有 jump 目标必须存在对应 label

## 十、素材占位策略

由于无法生成真实美术素材，采用以下占位策略：
- **背景图**：使用 Python PIL 生成指定色调的纯色/渐变背景 + 场景文字标注
- **角色立绘**：生成指定色调的剪影轮廓 + 角色名标注
- **UI元素**：生成按钮、边框的矢量风格占位图
- **音频**：创建空占位文件或使用 Ren'Py 的静音处理
- 所有占位素材尺寸符合 Ren'Py 标准（背景1920×1080，立绘按比例）
