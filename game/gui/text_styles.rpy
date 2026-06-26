# text_styles.rpy — 全场景文字样式配置
# 对标《无悔华夏》古朴厚重调性
# 8类文本样式 + 对话框改造

init offset = -2

## ============================================================
## 全局基础规则
## 所有文字无描边、无发光特效，保持古朴印刷/书写质感
## 行间距 1.5 倍，字间距标准
## ============================================================

## 对白正文 — 仿宋风格，略带笔锋，古朴清晰
style dialogue_text:
    font "SourceHanSansLite.ttf"
    size 24
    color "#1A1A1A"
    line_spacing 12
    text_align 0.0
    kerning 1

## 内心独白 — 行书手写风格，笔画流畅略带潦草
style monologue_text:
    font "SourceHanSansLite.ttf"
    size 22
    color "#5B7A8C"
    line_spacing 10
    text_align 0.0
    first_indent 48
    kerning 1
    italic True

## 史官旁白 — 楷体风格，端正工整，客观冷静
style narration_text:
    font "SourceHanSansLite.ttf"
    size 20
    color "#2C2C2C"
    line_spacing 8
    text_align 0.5
    kerning 2

## 章节标题 — 隶书碑刻风格，厚重苍劲有岁月感
style chapter_title:
    font "SourceHanSansLite.ttf"
    size 48
    color "#8B3A3A"
    text_align 0.5
    bold True

## 选项文字 — 篆刻印章风格，笔画方正古朴厚重
style choice_text:
    font "SourceHanSansLite.ttf"
    size 28
    color "#A0524F"
    text_align 0.5
    hover_color "#8B3A3A"
    bold True

style choice_button:
    background Frame("gui/button/choice_idle_background.png", 10, 10)
    hover_background Frame("gui/button/choice_hover_background.png", 10, 10)
    xpadding 30
    ypadding 12
    xalign 0.5

## 历史年表文字 — 小楷风格，工整细密
style timeline_text:
    font "SourceHanSansLite.ttf"
    size 18
    color "#2C2C2C"
    line_spacing 6
    text_align 0.0
    kerning 1

## UI 界面文字
style menu_button_text:
    font "SourceHanSansLite.ttf"
    size 28
    color "#D4C5A9"
    text_align 0.5
    hover_color "#F5F0E8"

style list_text:
    font "SourceHanSansLite.ttf"
    size 22
    color "#2C2C2C"
    text_align 0.0
    kerning 1

## 收尾点题文案 — 毛笔楷书风格，舒展大气
style ending_poem:
    font "SourceHanSansLite.ttf"
    size 36
    color "#D4C5A9"
    text_align 0.5
    yalign 0.5

## ============================================================
## 对话框样式配套改造
## ============================================================

## 基础对白对话框 — 水墨晕染毛边效果，半透明绢黄底色
style say_window:
    background Frame("gui/textbox/dialogue_box.png", 30, 30, 30, 30)
    xalign 0.5
    yalign 1.0
    xsize 1060
    ysize 240
    xpadding 40
    ypadding 20

## 独白对话框 — 半透明石青色，边缘更柔和
style monologue_window:
    background Frame("gui/textbox/monologue_box.png", 30, 30, 30, 30)
    xalign 0.5
    yalign 1.0
    xsize 1060
    ysize 220
    xpadding 50
    ypadding 25

## 旁白文本 — 无对话框，直接叠加背景，上下淡墨横线装饰
style narration_window:
    background None
    xalign 0.5
    yalign 0.5
    xsize 900
    ysize None

## 角色名标签 — 对话框左上角，隶书小号，朱砂色
style name_label:
    font "SourceHanSansLite.ttf"
    size 20
    color "#8B3A3A"
    xalign 0.0
    yalign 0.0
    xpos 50
    ypos -10
    bold True

## ============================================================
## 文本动效定义
## ============================================================

# 逐字显示 — 对白正文，速度中等
transform typewriter_effect:
    alpha 0.0
    linear 0.05 alpha 1.0

# 逐字淡入 — 内心独白，速度略慢
transform slow_fade_in:
    alpha 0.0
    linear 0.08 alpha 1.0

# 整体淡入 — 史官旁白，无逐字效果
transform full_fade_in:
    alpha 0.0
    linear 0.8 alpha 1.0

# 毛笔书写 — 章节标题，从浓到淡
transform brush_write:
    alpha 0.0
    xoffset -20
    parallel:
        linear 0.6 alpha 1.0
    parallel:
        linear 0.6 xoffset 0

# 印章落下 — 选项文字，带按压反馈
transform seal_stamp:
    alpha 0.0
    yoffset -30
    zoom 1.3
    parallel:
        linear 0.3 alpha 1.0
    parallel:
        easeout_back 0.4 yoffset 0
    parallel:
        easeout_back 0.4 zoom 1.0

# 逐行淡入 — 历史年表
transform line_fade_in:
    alpha 0.0
    linear 0.5 alpha 1.0

# 逐字书写浮现 — 收尾文案
transform poem_write:
    alpha 0.0
    parallel:
        linear 2.0 alpha 1.0
    parallel:
        linear 2.0 xoffset 0
