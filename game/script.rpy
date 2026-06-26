# script.rpy — 风暴中的大顺朝 主脚本入口
# 角色定义、图片定义、转场定义、游戏启动

## 角色定义

define narrator = Character(None)
define storyteller = Character("说书人", color="#8B3A3A")
define emperor = Character("李东升", color="#5B7A8C")
define liusilian = Character("刘思廉", color="#8B6B4A")
define guziming = Character("顾子明", color="#6B4B3A")
define zhaotieshuan = Character("赵铁栓", color="#6B6B5A")
define teaguest = Character("茶客", color="#7A6B5A")
define maid = Character("内侍", color="#5A5A5A")
define officer = Character("军官", color="#5A5A5A")

## 图片定义

# 场景背景
image bg_teahouse = "images/backgrounds/bg_teahouse.webp"
image bg_palace = "images/backgrounds/bg_palace.webp"
image bg_village = "images/backgrounds/bg_village.webp"
image bg_yamen = "images/backgrounds/bg_yamen.webp"
image bg_court = "images/backgrounds/bg_court.webp"
image bg_camp = "images/backgrounds/bg_camp.webp"
image bg_black = Solid("#1A1A1A")

# 角色立绘
image char_emperor = "images/characters/char_emperor.webp"
image char_liusilian = "images/characters/char_liusilian.webp"
image char_majing = "images/characters/char_majing.webp"
image char_guziming = "images/characters/char_guziming.webp"
image char_xushuniang = "images/characters/char_xushuniang.webp"
image char_lichengying = "images/characters/char_lichengying.webp"
image char_hantieshan = "images/characters/char_hantieshan.webp"
image char_zhaotieshuan = "images/characters/char_zhaotieshuan.webp"

## 转场定义

# 墨滴晕开 — 回忆与现实切换
define ink_transition = Dissolve(1.5)
# 卷轴展开 — 时间跳转
define scroll_transition = Dissolve(2.0)
# 朱砂印章 — 抉择弹出
define seal_transition = Dissolve(0.8)
# 暗角幻觉 — 帝王幻觉
define hallucination_transition = Dissolve(1.0)
# 毛笔逐字 — 标题显示
define brush_transition = Dissolve(1.2)

## 游戏默认值

default persistent.ending_a_seen = False
default persistent.ending_b_seen = False

## 游戏启动

label start:
    scene bg_black with Dissolve(1.0)
    
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
