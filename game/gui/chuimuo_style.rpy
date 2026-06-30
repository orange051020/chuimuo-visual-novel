# 《垂暮》文字与界面样式配置
# 仅负责 Ren'Py UI 样式，不生成任何图片素材。

define gui.text_font = "fonts/NotoSansSC-Regular.subset.otf"
define gui.name_text_font = "fonts/NotoSansSC-Bold.subset.otf"
define gui.interface_text_font = "fonts/NotoSansSC-Regular.subset.otf"
define gui.text_size = 30
define gui.name_text_size = 28
define gui.interface_text_size = 24
define gui.dialogue_width = 1180
define gui.dialogue_xpos = 370
define gui.dialogue_ypos = 790
define gui.name_xpos = 180
define gui.name_ypos = 730

define gui.text_color = "#2A2118"
define gui.name_text_color = "#8B3A3A"
define gui.interface_text_color = "#E8DFCC"
define gui.hover_color = "#A0524F"
define gui.insensitive_color = "#6B6253"

style default:
    font gui.text_font
    language "unicode"

style centered_text:
    font gui.text_font
    language "unicode"

style button_text:
    font gui.interface_text_font
    language "unicode"

style window:
    xalign 0.5
    yalign 1.0
    xsize 1320
    yminimum 220
    left_padding 54
    right_padding 54
    top_padding 34
    bottom_padding 34
    background Solid("#EEE5D1DD")

style say_label:
    color "#8B3A3A"
    bold True
    outlines [ (1, "#E8DFCCAA", 0, 0) ]

style say_dialogue:
    color "#2A2118"
    line_spacing 10
    outlines [ (1, "#FFF8E688", 0, 0) ]

style choice_button:
    xalign 0.5
    xminimum 520
    yminimum 64
    background Solid("#EEE5D1DD")
    hover_background Solid("#F5E8CCD9")

style choice_button_text:
    color "#2A2118"
    hover_color "#8B3A3A"
    size 28
