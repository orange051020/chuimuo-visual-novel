# gui.rpy — 风暴中的大顺朝 GUI配置
# 水墨国风色值体系

## GUI 初始化（设置默认分辨率和样式）

init python:
    gui.init(1920, 1080)

## 全局默认字体（确保所有中文文字可渲染）

style default:
    font "SourceHanSansLite.ttf"

## 字体定义（必须使用支持中文的字体）

define gui.text_font = "SourceHanSansLite.ttf"
define gui.name_text_font = "SourceHanSansLite.ttf"
define gui.interface_text_font = "SourceHanSansLite.ttf"
define gui.title_text_font = "SourceHanSansLite.ttf"
define gui.label_text_font = "SourceHanSansLite.ttf"
define gui.notify_text_font = "SourceHanSansLite.ttf"
define gui.button_text_font = "SourceHanSansLite.ttf"

## 色值定义

define gui.text_color = "#2C2C2C"
define gui.idle_color = "#5B7A8C"
define gui.hover_color = "#8B3A3A"
define gui.selected_color = "#A0524F"
define gui.insensitive_color = "#8B8B7A"
define gui.frame_color = "#D4C5A9"
define gui.background_color = "#1A1A1A"
define gui.muted_color = "#6B6B5A"
define gui.accent_color = "#8B3A3A"

## 文本设置

define gui.text_size = 28
define gui.name_text_size = 32
define gui.interface_text_size = 24
define gui.title_text_size = 48
define gui.label_text_size = 36
define gui.notify_text_size = 24

## 对话框设置

define gui.textbox_height = 220
define gui.textbox_yalign = 1.0
define gui.name_xpos = 80
define gui.name_ypos = 0
define gui.name_xalign = 0
define gui.namebox_width = 200
define gui.namebox_height = 40
define gui.namebox_yalign = 1.0
define gui.text_xpos = 80
define gui.text_ypos = 50
define gui.text_width = 1760
define gui.text_xalign = 0
define gui.text_yalign = 0

## 按钮设置

define gui.button_width = None
define gui.button_height = 40
define gui.button_borders = Borders(10, 10, 10, 10)
define gui.button_text_xalign = 0.5
define gui.button_text_size = 24

## 主菜单按钮

define gui.main_menu_text_xalign = 1.0
define gui.main_menu_text_yalign = 0.5
define gui.main_menu_text_size = 28

## 存档/读档槽位

define gui.slot_slot_width = 414
define gui.slot_slot_height = 309
define gui.slot_slot_borders = Borders(2, 2, 2, 2)
define gui.slot_button_text_size = 18
define gui.slot_button_text_xalign = 0.5
define gui.slot_button_text_idle_color = "#5B7A8C"
define gui.slot_button_text_selected_idle_color = "#F5F0E8"
define gui.slot_button_text_selected_hover_color = "#8B3A3A"
define gui.slot_scrollbar_xpos = 0.5
define gui.slot_scrollbar_ypos = 0.5
define gui.slot_scrollbar_xalign = 1.0
define gui.slot_scrollbar_yalign = 0.0

## 滚动条设置

define gui.scrollbar_size = 12
define gui.scrollbar_borders = Borders(2, 2, 2, 2)
define gui.scrollbar_tile = False
define gui.vbar_borders = Borders(2, 4, 2, 4)
define gui.hbar_borders = Borders(4, 2, 4, 2)

## 滑块设置

define gui.slider_size = 12
define gui.slider_tile = False
define gui.slider_borders = Borders(2, 4, 2, 4)
define gui.vslider_borders = Borders(4, 2, 4, 2)

## 面板设置

define gui.frame_borders = Borders(10, 10, 10, 10)
define gui.confirm_frame_borders = Borders(20, 20, 20, 20)
define gui.skip_frame_borders = Borders(2, 2, 2, 2)
define gui.notify_frame_borders = Borders(20, 10, 20, 10)

## 历史记录设置

define gui.history_height = 140
define gui.history_name_xpos = 80
define gui.history_name_ypos = 0
define gui.history_name_width = 200
define gui.history_name_xalign = 0
define gui.history_text_xpos = 80
define gui.history_text_ypos = 30
define gui.history_text_width = 1760
define gui.history_text_xalign = 0

## 导航设置

define gui.navigation_xpos = 40
define gui.navigation_ypos = 120
define gui.navigation_spacing = 10
define gui.navigation_button_width = 200

## 对话框样式

define gui.dialoguebox_background = "#D4C5A9"
define gui.dialoguebox_opacity = 0.9

## 确认对话框

define gui.confirm_background = "#D4C5A9"
define gui.confirm_text_color = "#2C2C2C"

## 通知

define gui.notify_background = "#2C2C2C"
define gui.notify_text_color = "#F5F0E8"

## Web响应式适配
# 桌面端和移动端浏览器窗口中均正常显示不溢出
init python:
    if renpy.emscripten:
        # Web环境：启用虚拟分辨率缩放，自动适配窗口大小
        config.physical_height = 1080
        config.physical_width = 1920
        # 禁用鼠标光标自定义（浏览器兼容）
        config.mouse = None
