# options.rpy — 风暴中的大顺朝 游戏配置
# Web适配：浏览器环境使用LocalStorage/IndexedDB持久化存储

define config.name = "风暴中的大顺朝"
define config.version = "1.0.0"
define config.save_directory = "dashun_dynasty_1745000000"

define config.window_title = "风暴中的大顺朝 — 垂暮序章"

# 窗口设置
define config.screen_width = 1920
define config.screen_height = 1080

# 标题画面
define config.main_menu_music = None

# 存档设置 — Web环境自动使用浏览器IndexedDB持久化
define config.has_autosave = True
define config.autosave_frequency = 100
define config.has_quicksave = True

# 文本设置（使用 preferences 而非 config）
default preferences.text_cps = 30
default preferences.afm_time = 10

# 跳过设置
define config.allow_skipping = True

# 音量默认值
default preferences.music_volume = 0.6
default preferences.sfx_volume = 0.7
default preferences.voice_volume = 0.8

# 界面设置
define config.window_icon = None
define config.thumbnail_width = 384
define config.thumbnail_height = 216

# 字体设置
define config.font_replacement_map = {}

# 过渡设置
define config.end_splash_transition = None
define config.end_game_transition = Dissolve(1.0)
define config.game_main_transition = Dissolve(0.5)
define config.main_game_transition = Dissolve(0.5)
define config.intra_transition = Dissolve(0.3)
define config.enter_replay_transition = Dissolve(0.5)
define config.exit_replay_transition = Dissolve(0.5)

## Web适配配置
# 浏览器环境禁用不兼容的特性
init python:
    if renpy.emscripten:
        # Web环境：使用浏览器持久化存储，刷新页面后进度不丢失
        config.has_autosave = True
        config.autosave_frequency = 100
        # 禁用桌面端文件系统相关操作
        config.developer = False
