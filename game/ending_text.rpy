# ending_text.rpy — 双结局统一收尾模块
# 固定文案：百姓心中有杆秤 时间会证明一切
# 在结局A/结局B末尾通过 jump unified_ending 调用
# 不侵入原有剧情脚本，独立封装

## 收尾文案文本样式
# 字体：与项目旁白字体统一（SourceHanSansLite）
# 字号：正文28 x 1.5 = 42
# 颜色：绢黄旧纸色 #D4C5A9
# 无描边、无投影
style ending_text_style:
    font "SourceHanSansLite.ttf"
    size 42
    color "#D4C5A9"
    text_align 0.5
    line_leading 10
    line_spacing 20

## 收尾文案位置变换（水平垂直居中，无其他UI遮挡）
transform ending_text_transform:
    xalign 0.5
    yalign 0.5

## 统一收尾标签 — 双结局共用，保证逻辑复用
label unified_ending:
    # 隐藏对话框，确保收尾画面无其他UI元素
    window hide

    # 淡出背景音乐，与渐暗同步
    stop music fadeout 1.5

    # 第一步：结局画面以1.5秒匀速渐暗，切换到收尾画轴背景
    scene bg_ending_text with Dissolve(1.5)

    # 第二步：全黑背景下，文案以2秒逐字书写式淡入浮现
    # 14个汉字（不计换行），每字延迟约0.143秒，总时长2秒
    python:
        line1 = "百姓心中有杆秤"
        line2 = "时间会证明一切"
        full_text = line1 + "\n" + line2
        char_count = 14
        char_delay = 2.0 / char_count

        shown_text = ""
        for ch in full_text:
            shown_text += ch
            if ch != "\n":
                renpy.show("ending_text",
                    what=Text(shown_text, style="ending_text_style"),
                    at_list=[ending_text_transform])
                renpy.pause(char_delay)

    # 第三步：文案完整显示后，静止停留3秒
    $ renpy.pause(3.0)

    # 第四步：文案以1.5秒匀速淡出，画面保持全黑
    hide ending_text with Dissolve(1.5)

    # 第五步：淡出完成后，自动跳转返回游戏主标题界面
    return
