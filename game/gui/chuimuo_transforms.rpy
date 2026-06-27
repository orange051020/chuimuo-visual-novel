# 《垂暮》场景转场与立绘动效
# 仅定义代码层动效，不生成任何图片素材。

define ink_fade = Fade(0.45, 0.12, 0.55, color="#17140F")
define slow_dissolve = Dissolve(0.8)

transform vn_right:
    xalign 0.86
    yalign 1.0
    alpha 0.0
    xoffset 38
    ease 0.45 alpha 1.0 xoffset 0

transform vn_left:
    xalign 0.14
    yalign 1.0
    alpha 0.0
    xoffset -38
    ease 0.45 alpha 1.0 xoffset 0

transform memory_faint:
    alpha 0.46
    yalign 1.0

transform breath_idle:
    block:
        ease 2.4 yoffset -4
        ease 2.4 yoffset 0
        repeat
