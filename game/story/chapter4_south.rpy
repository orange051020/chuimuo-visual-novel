# chapter4_south.rpy — 片段四：南方行辕
# 权臣复盘大局，乱世终定、新秩序成型

label chapter4_south:
    scene bg_mansion_wide with ink_transition
    show char_liusilian_sit at left_pos
    show char_majing_arms at right_pos with portrait_dim
    play music "audio/bgm/bgm_yamen.mp3" fadein 2.0

    "南方。行辕。"

    "大顺开国十九年。春。"

    "行辕书房里，烛火通明。窗外是南方的夜景——河道上画舫灯火点点，丝竹声隐约可闻。新秩序的虚浮繁华，在这片水乡夜色中徐徐铺展开来。"

    "刘思廉端坐在书案后，脊背笔直如松。面前的案上摊着三样东西：一封通商开埠的奏疏，一份各地民情的密报，一道帝王驾崩的遗诏。"

    "他没有看遗诏。他在看密报。"

    scene bg_mansion_desk with ink_transition

    "密报上写着北方清算的数字。赵铁栓的名字在其中，混在一长串名单里，不过是百余个名字中的一个。"

    "刘思廉将密报合上，放到一旁。他的表情没有变化。"

    liusilian "十年了。"

    "他开口，声音平静得像是在谈论天气。"

    liusilian "从陛下颁《大顺律》那年算起，整整十年。我看着这部律法从利民之器，变成害民之刃。不是律法本身有错——是制度。是人心。是这个盘根错节了两千年的官僚体系。"

    "他站起身，走到窗前。画舫的灯火映在他脸上，明明灭灭。"

    scene bg_mansion_window with ink_transition
    show char_liusilian_back at left_pos with portrait_dim

    liusilian "陛下以为，把刀递给百姓，百姓就能保护自己。可刀是有重量的。百姓握不住，便有人替他们握。豪强握了刀，清洗异己。武将握了刀，私固兵权。到头来，刀成了所有人的凶器，唯独没有保护任何人。"

    "他转过身，目光落在那份遗诏上。"

    liusilian "陛下至死都以为律法还在庇护子民。这不是他的错。深宫的墙太厚了，消息传进去的时候，早就不是原来的模样了。"

    liusilian "可这也不是无辜。一个帝王，如果连自己的帝国在发生什么都不知道——他的理想，便只是理想。"

    "他重新坐下，提笔在通商开埠的奏疏上批了一个“准”字。"

    liusilian "马靖已经在北边稳住了局面。通商开埠之后，百姓有饭吃、有活干，便不会有人再提《大顺律》。三年之内，这部律法会被所有人遗忘。"

    liusilian "这不是最好结局。但这是现实。"

    "他放下笔，沉默了片刻。"

    liusilian "陛下是好人。可好人未必能治好天下。"

    liusilian "我等了十年，忍了十年，不是为了篡位。是因为我亲眼看着那部律法一步步把帝国推向深渊。我必须阻止它。哪怕用的方式——陛下不会原谅。"

    "窗外，画舫上有人在唱曲。软糯的吴侬软语，唱的是太平盛世的新词。"

    "刘思廉没有听。他在想另一件事。"

    "他在想那个北方的老兵——赵铁栓。密报上说，赵铁栓至死都在念“陛下会知道的”。"

    liusilian "他不知道。陛下什么都不知道。"

    "刘思廉闭上眼，长长地叹了一口气。"

    liusilian "这世上最残忍的事，不是有人作恶。是好人用好心铸成悲剧，信徒为信仰赴死却无人知晓，权臣用冷酷拯救苍生却背负骂名。"

    liusilian "没有人是恶人。可所有人都输了。"

    scene bg_mansion_toast with scroll_transition
    show char_majing_toast at right_pos with portrait_enter
    show char_liusilian_sit at left_pos

    "他睁开眼，目光落在遗诏上。"

    liusilian "陛下走了。"

    "行辕外，东方天际泛起了鱼肚白。新的一天开始了。新的秩序，也在这个黎明悄然成型。"

    "通商开埠的商船将从南方出发，驶向大洋。北方的风雪将被遗忘。那部曾让万人殉道的《大顺律》，将在三年之内从所有文书中抹去。"

    "而那个至死不知真相的帝王——"

    "他的最后一刻，是什么样的？"

    stop music fadeout 3.0

    hide char_majing_toast
    hide char_liusilian_sit
    with portrait_fade

    scene bg_black with scroll_transition

    $ renpy.force_autosave()

    jump ending_choice
