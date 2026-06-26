# screens.rpy — 风暴中的大顺朝 界面定义
# 主菜单、游戏菜单、存档/读档、设置、文本回放、快捷菜单

## 对话界面（say screen）

screen say(who, what):
    style_prefix "say"

    window:
        id "window"
        background Solid("#D4C5A9C0")

        if who is not None:
            window:
                id "namebox"
                style "namebox"
                background Solid("#8B3A3A40")
                text who id "who" color "#F5F0E8" size 32

        text what id "what" color "#2C2C2C" size 28

    if not renpy.variant("small"):
        use quick_menu

style say_window:
    xalign 0.5
    yalign 1.0
    xsize 1920
    ysize 220

style say_namebox:
    xpos 80
    ypos 0
    xsize 200
    ysize 45

style say_label:
    xalign 0
    font "SourceHanSansLite.ttf"

style say_dialogue:
    xpos 80
    ypos 50
    xsize 1760
    font "SourceHanSansLite.ttf"

## 选项界面（choice screen）

screen choice(items):
    style_prefix "choice"

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 20

        for i in items:
            textbutton i.caption:
                action i.action
                background Solid("#D4C5A980")
                hover_background Solid("#8B3A3A60")
                text_color "#2C2C2C"
                text_hover_color "#F5F0E8"
                text_size 28
                xalign 0.5
                xsize 600
                ysize 60

style choice_vbox:
    xalign 0.5
    yalign 0.5

style choice_button:
    xalign 0.5

## 主菜单界面

screen main_menu():
    style_prefix "main_menu"

    add Solid("#1A1A1A")
    add "images/ui/title_bg.webp"

    vbox:
        xalign 0.5
        yalign 0.3
        spacing 10

        text "风暴中的大顺朝":
            color "#D4C5A9"
            size 64
            xalign 0.5

        text "垂暮":
            color "#8B3A3A"
            size 42
            xalign 0.5

    vbox:
        xalign 0.5
        yalign 0.65
        spacing 15

        textbutton "开始游戏":
            action Start()
            text_color "#D4C5A9"
            text_hover_color "#8B3A3A"
            text_size 32
            xalign 0.5

        textbutton "读取存档":
            action ShowMenu("load")
            text_color "#5B7A8C"
            text_hover_color "#8B3A3A"
            text_size 28
            xalign 0.5

        textbutton "游戏设置":
            action ShowMenu("preferences")
            text_color "#5B7A8C"
            text_hover_color "#8B3A3A"
            text_size 28
            xalign 0.5

        textbutton "退出游戏":
            action Quit(confirm=True)
            text_color "#5B7A8C"
            text_hover_color "#8B3A3A"
            text_size 28
            xalign 0.5

## 游戏菜单界面

screen game_menu(title, scroll=None, yinitial=0.0):
    style_prefix "game_menu"

    add Solid("#1A1A1A")

    frame:
        background Solid("#D4C5A940")
        xfill True
        yfill True

        hbox:
            # 左侧导航
            frame:
                background None
                ysize 1080
                xsize 280
                vbox:
                    xpos 20
                    ypos 120
                    spacing 15

                    textbutton "历史" action ShowMenu("history"):
                        text_color "#5B7A8C"
                        text_hover_color "#8B3A3A"
                        text_size 24

                    textbutton "存档" action ShowMenu("save"):
                        text_color "#5B7A8C"
                        text_hover_color "#8B3A3A"
                        text_size 24

                    textbutton "读档" action ShowMenu("load"):
                        text_color "#5B7A8C"
                        text_hover_color "#8B3A3A"
                        text_size 24

                    textbutton "设置" action ShowMenu("preferences"):
                        text_color "#5B7A8C"
                        text_hover_color "#8B3A3A"
                        text_size 24

                    textbutton "主菜单" action MainMenu():
                        text_color "#5B7A8C"
                        text_hover_color "#8B3A3A"
                        text_size 24

                    textbutton "退出" action Quit():
                        text_color "#5B7A8C"
                        text_hover_color "#8B3A3A"
                        text_size 24

            # 右侧内容区
            frame:
                background None
                xfill True
                yfill True
                vbox:
                    xpos 20
                    ypos 40

                    text title:
                        color "#D4C5A9"
                        size 36

                    null height 20

                    if scroll == "viewport":
                        viewport:
                            yinitial yinitial
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            transclude
                    elif scroll == "vpgrid":
                        vpgrid:
                            cols 1
                            yinitial yinitial
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            transclude
                    else:
                        transclude

## 存档界面

screen save(slot=False):
    use game_menu("存档", scroll="vpgrid")

    fixed:
        vbox:
            xpos 320
            ypos 120
            spacing 15

            grid 2 4:
                spacing 15

                for i in range(1, 9):
                    button:
                        background Solid("#D4C5A960")
                        hover_background Solid("#8B3A3A40")
                        xsize 380
                        ysize 220

                        action FileAction(i)

                        vbox:
                            xpos 10
                            ypos 10

                            add FileSlot(i, 160, 90):
                                xalign 0

                            text FileTime(i, format="存档于 %Y-%m-%d %H:%M", empty="空存档"):
                                color "#5B7A8C"
                                size 16
                                ypos 10

## 读档界面

screen load(slot=False):
    use game_menu("读档", scroll="vpgrid")

    fixed:
        vbox:
            xpos 320
            ypos 120
            spacing 15

            grid 2 4:
                spacing 15

                for i in range(1, 9):
                    button:
                        background Solid("#D4C5A960")
                        hover_background Solid("#8B3A3A40")
                        xsize 380
                        ysize 220

                        action FileAction(i)

                        vbox:
                            xpos 10
                            ypos 10

                            add FileSlot(i, 160, 90):
                                xalign 0

                            text FileTime(i, format="存档于 %Y-%m-%d %H:%M", empty="空存档"):
                                color "#5B7A8C"
                                size 16
                                ypos 10

## 系统设置界面

screen preferences():
    use game_menu("设置")

    fixed:
        vbox:
            xpos 320
            ypos 120
            spacing 20

            # 音量设置
            frame:
                background Solid("#D4C5A930")
                xsize 900
                vbox:
                    xpos 20
                    ypos 15
                    spacing 15

                    text "音量设置":
                        color "#D4C5A9"
                        size 28

                    hbox:
                        spacing 10
                        text "音乐" color "#5B7A8C" size 24 yalign 0.5
                        bar value Preference("music volume"):
                            xsize 300
                            ysize 20
                            left_bar Solid("#8B3A3A")
                            right_bar Solid("#5B7A8C40")

                    hbox:
                        spacing 10
                        text "音效" color "#5B7A8C" size 24 yalign 0.5
                        bar value Preference("sound volume"):
                            xsize 300
                            ysize 20
                            left_bar Solid("#8B3A3A")
                            right_bar Solid("#5B7A8C40")

            # 文字设置
            frame:
                background Solid("#D4C5A930")
                xsize 900
                vbox:
                    xpos 20
                    ypos 15
                    spacing 15

                    text "文字设置":
                        color "#D4C5A9"
                        size 28

                    hbox:
                        spacing 10
                        text "文字速度" color "#5B7A8C" size 24 yalign 0.5
                        bar value Preference("text speed"):
                            xsize 300
                            ysize 20
                            left_bar Solid("#8B3A3A")
                            right_bar Solid("#5B7A8C40")

                    textbutton "自动推进" action Preference("auto-forward", "toggle"):
                        text_color "#5B7A8C"
                        text_hover_color "#8B3A3A"
                        text_size 24

            # 显示设置
            frame:
                background Solid("#D4C5A930")
                xsize 900
                vbox:
                    xpos 20
                    ypos 15
                    spacing 15

                    text "显示设置":
                        color "#D4C5A9"
                        size 28

                    textbutton "窗口模式" action Preference("display", "window"):
                        text_color "#5B7A8C"
                        text_hover_color "#8B3A3A"
                        text_size 24

                    textbutton "全屏模式" action Preference("display", "fullscreen"):
                        text_color "#5B7A8C"
                        text_hover_color "#8B3A3A"
                        text_size 24

## 文本回放界面

screen history():
    use game_menu("历史", scroll="vpgrid")

    fixed:
        viewport:
            xpos 320
            ypos 120
            xsize 1500
            ysize 850
            scrollbars "vertical"
            mousewheel True
            draggable True

            vbox:
                spacing 10

                for h in _history_list:
                    window:
                        background None
                        xsize 1500

                        if h.who:
                            text h.who:
                                color "#8B3A3A"
                                size 26
                                xpos 20

                        text h.what:
                            color "#D4C5A9"
                            size 24
                            xpos 40
                            ypos 30
                            xsize 1460

## 快捷菜单

screen quick_menu():
    hbox:
        xalign 0.5
        yalign 1.0
        yoffset -5
        spacing 10

        textbutton "存档" action ShowMenu("save"):
            text_color "#5B7A8C"
            text_hover_color "#8B3A3A"
            text_size 20
            background Solid("#D4C5A980")
            xsize 80
            ysize 35

        textbutton "读档" action ShowMenu("load"):
            text_color "#5B7A8C"
            text_hover_color "#8B3A3A"
            text_size 20
            background Solid("#D4C5A980")
            xsize 80
            ysize 35

        textbutton "设置" action ShowMenu("preferences"):
            text_color "#5B7A8C"
            text_hover_color "#8B3A3A"
            text_size 20
            background Solid("#D4C5A980")
            xsize 80
            ysize 35

        textbutton "跳过" action Skip():
            text_color "#5B7A8C"
            text_hover_color "#8B3A3A"
            text_size 20
            background Solid("#D4C5A980")
            xsize 80
            ysize 35

        textbutton "自动" action Preference("auto-forward", "toggle"):
            text_color "#5B7A8C"
            text_hover_color "#8B3A3A"
            text_size 20
            background Solid("#D4C5A980")
            xsize 80
            ysize 35

        textbutton "回放" action ShowMenu("history"):
            text_color "#5B7A8C"
            text_hover_color "#8B3A3A"
            text_size 20
            background Solid("#D4C5A980")
            xsize 80
            ysize 35

## 确认对话框

screen confirm(message, yes_action, no_action):
    zorder 200

    add Solid("#00000080")

    frame:
        background Solid("#D4C5A9")
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 200

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 30

            text message:
                color "#2C2C2C"
                size 28
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 50

                textbutton "确定" action yes_action:
                    text_color "#2C2C2C"
                    text_hover_color "#8B3A3A"
                    text_size 24

                textbutton "取消" action no_action:
                    text_color "#2C2C2C"
                    text_hover_color "#8B3A3A"
                    text_size 24

## 跳过指示器

screen skip_indicator():
    zorder 100

    frame:
        background Solid("#2C2C2C")
        xalign 0.5
        yalign 0.1

        text "跳过中":
            color "#F5F0E8"
            size 20

## 通知

screen notify(message):
    zorder 100

    frame:
        background Solid("#2C2C2C90")
        xalign 0.5
        yalign 0.05

        text message:
            color "#F5F0E8"
            size 24

    timer 3.0 action Hide("notify")
