# script.rpy — 风暴中的大顺朝 主脚本入口
# 角色定义、图片定义、转场定义、游戏启动

## 角色定义 — 立绘由逐页 show/hide 命令手动管理
define narrator = Character(None, what_style="narration_text")
define storyteller = Character("说书人", color="#8B6B4A")
define emperor = Character("李东升", color="#8B3A3A")
define liusilian = Character("刘思廉", color="#5B7A8C")
define guziming = Character("顾子明", color="#6B7A8A")
define majing = Character("马靖", color="#1A1A1A")
define xushuliang = Character("徐淑娘", color="#A0524F")
define lichengying = Character("李承英", color="#7A6B5A")
define hantieshan = Character("韩铁山", color="#6B4B3A")
define zhaotieshuan = Character("赵铁栓", color="#8B6B4A")
define teaguest = Character("茶客", color="#7A6B5A")
define maid = Character("内侍", color="#5A5A5A")
define officer = Character("军官", color="#5A5A5A")

## 场景背景
image bg_teahouse_wide = "images/backgrounds/bg_teahouse_wide.webp"
image bg_teahouse_stage = "images/backgrounds/bg_teahouse_stage.webp"
image bg_teahouse_audience = "images/backgrounds/bg_teahouse_audience.webp"
image bg_teahouse_window = "images/backgrounds/bg_teahouse_window.webp"
image bg_bedchamber_wide = "images/backgrounds/bg_bedchamber_wide.webp"
image bg_bedchamber_candle = "images/backgrounds/bg_bedchamber_candle.webp"
image bg_bedchamber_illusion = "images/backgrounds/bg_bedchamber_illusion.webp"
image bg_study_flashback = "images/backgrounds/bg_study_flashback.webp"
image bg_court_flashback = "images/backgrounds/bg_court_flashback.webp"
image bg_northwest_flashback = "images/backgrounds/bg_northwest_flashback.webp"
image bg_bedchamber_end = "images/backgrounds/bg_bedchamber_end.webp"
image bg_village_distant = "images/backgrounds/bg_village_distant.webp"
image bg_village_tree = "images/backgrounds/bg_village_tree.webp"
image bg_square_flashback = "images/backgrounds/bg_square_flashback.webp"
image bg_paper_closeup = "images/backgrounds/bg_paper_closeup.webp"
image bg_mansion_wide = "images/backgrounds/bg_mansion_wide.webp"
image bg_mansion_desk = "images/backgrounds/bg_mansion_desk.webp"
image bg_mansion_window = "images/backgrounds/bg_mansion_window.webp"
image bg_mansion_toast = "images/backgrounds/bg_mansion_toast.webp"
image bg_ending_text = "images/backgrounds/bg_ending_text.webp"
image ending_text = Text("")  # 占位，由 ending_text.rpy 动态填充
image bg_black = Solid("#0A0A0A")

## 角色立绘定义
# 说书人
image char_storyteller_half = "images/character/char_storyteller_half.webp"
image char_storyteller_full = "images/character/char_storyteller_full.webp"
# 李东升
image char_emperor_bed = "images/character/char_emperor_bed.webp"
image char_emperor_angry = "images/character/char_emperor_angry.webp"
image char_emperor_silent = "images/character/char_emperor_silent.webp"
image char_emperor_young = "images/character/char_emperor_young.webp"
image char_emperor_hand = "images/character/char_emperor_hand.webp"
# 刘思廉
image char_liusilian_sit = "images/character/char_liusilian_sit.webp"
image char_liusilian_argue = "images/character/char_liusilian_argue.webp"
image char_liusilian_back = "images/character/char_liusilian_back.webp"
image char_liusilian_hand = "images/character/char_liusilian_hand.webp"
# 马靖
image char_majing_arms = "images/character/char_majing_arms.webp"
image char_majing_sword = "images/character/char_majing_sword.webp"
image char_majing_toast = "images/character/char_majing_toast.webp"
image char_majing_hand = "images/character/char_majing_hand.webp"
# 顾子明
image char_guziming_bow = "images/character/char_guziming_bow.webp"
image char_guziming_break = "images/character/char_guziming_break.webp"
image char_guziming_kneel = "images/character/char_guziming_kneel.webp"
image char_guziming_hand = "images/character/char_guziming_hand.webp"
# 徐淑娘
image char_xushuliang_sit = "images/character/char_xushuliang_sit.webp"
image char_xushuliang_side = "images/character/char_xushuliang_side.webp"
image char_xushuliang_ghost = "images/character/char_xushuliang_ghost.webp"
# 李承英
image char_lichengying_stand = "images/character/char_lichengying_stand.webp"
image char_lichengying_stoop = "images/character/char_lichengying_stoop.webp"
image char_lichengying_ghost = "images/character/char_lichengying_ghost.webp"
# 韩铁山
image char_hantieshan_knife = "images/character/char_hantieshan_knife.webp"
image char_hantieshan_kill = "images/character/char_hantieshan_kill.webp"
image char_hantieshan_ghost = "images/character/char_hantieshan_ghost.webp"
# 赵铁栓
image char_zhaotieshuan_talk = "images/character/char_zhaotieshuan_talk.webp"
image char_zhaotieshuan_kneel = "images/character/char_zhaotieshuan_kneel.webp"
image char_zhaotieshuan_fall = "images/character/char_zhaotieshuan_fall.webp"
image char_zhaotieshuan_hand = "images/character/char_zhaotieshuan_hand.webp"
# 群像
image char_group_court = "images/character/char_group_court.webp"
image char_group_village = "images/character/char_group_village.webp"
image char_group_four = "images/character/char_group_four.webp"
image char_group_teahouse = "images/character/char_group_teahouse.webp"

## 转场定义
define ink_transition = Dissolve(1.5)
define scroll_transition = Dissolve(2.0)
define seal_transition = Dissolve(0.8)
define hallucination_transition = Dissolve(1.0)
define brush_transition = Dissolve(1.2)
define portrait_fade = Dissolve(0.5)

## 立绘动效
transform portrait_enter:
    alpha 0.0
    linear 0.5 alpha 1.0

transform portrait_exit:
    alpha 1.0
    linear 0.5 alpha 0.0

transform portrait_ghost:
    alpha 0.5
    blur 2

transform portrait_dim:
    alpha 0.3

transform portrait_full:
    alpha 1.0

## 立绘默认位置
define left_pos = {"xalign": 0.25, "yalign": 0.5}
define right_pos = {"xalign": 0.75, "yalign": 0.5}
define center_pos = {"xalign": 0.5, "yalign": 0.5}
define bottom_pos = {"xalign": 0.5, "yalign": 0.85}

## 游戏默认值
default persistent.ending_a_seen = False
default persistent.ending_b_seen = False

## 游戏启动
label start:
    scene bg_teahouse_wide with Dissolve(1.0)
    
    $ renpy.pause(1.0)
    
    # 标题画面
    show text "风暴中的大顺朝" with brush_transition
    $ renpy.pause(2.0)
    hide text with Dissolve(0.5)
    
    show text "垂暮" with brush_transition
    $ renpy.pause(1.5)
    hide text with Dissolve(0.5)
    
    $ renpy.pause(0.5)
    
    jump chapter1_market
