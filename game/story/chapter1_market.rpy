# chapter1_market.rpy — 片段一：京城市井
# 后世定论，说书人盖棺

label chapter1_market:
    scene bg_teahouse_wide with ink_transition
    play music "audio/bgm/bgm_market.mp3" fadein 2.0

    "大顺开国二十三年。京城西市，一间老茶馆。"

    "午后的日头斜斜照进来，尘埃在光柱里缓缓浮动。茶客们歪在竹椅上，有人嗑着瓜子，有人半阖着眼打盹。角落里的铜壶咕嘟咕嘟冒着热气，茶香混着市井的烟火味道，懒洋洋地弥散开。"

    "说书人上了台。一张方桌，一把折扇，一块醒木。"

    "醒木一拍。堂下渐静。"

    scene bg_teahouse_stage with ink_transition
    show char_storyteller_half at right_pos with portrait_enter

    storyteller "列位，今儿说的这段不算新鲜。可有些事啊，越搁越沉，不说不行。"

    storyteller "话说大顺开国那会儿，李东升皇帝分了田、废了科举，叫百姓集体耕作。头几年风调雨顺，人人有饭吃，户户称颂。街头巷尾都说，圣天子在位，千古难逢。"

    "说书人顿了顿，扫了一眼堂下。茶客们微微坐直了身子。"

    storyteller "可好景不长。地方上阳奉阴违，举荐制滋生腐败，旧秩序死灰复燃。皇帝坐在深宫里，看着奏折上写的太平盛世，心里却越来越慌。"

    storyteller "到了第六年——皇帝急了。他一怒之下，颁了《大顺律》。"

    "堂下有人低声议论。说书人折扇一合，声音压低了几分。"

    scene bg_teahouse_audience with ink_transition
    show char_group_teahouse at bottom_pos with portrait_dim

    storyteller "这律法厉害。许百姓告官，许百姓审官。古往今来，哪朝哪代敢这么干？这是把刀递到了百姓手里啊。"

    "角落里一个茶客插嘴。"

    teaguest "那不是好事吗？"

    storyteller "好事？开头确实是好事。可诸位想想——刀给了百姓，百姓握得住吗？"

    "说书人将折扇往桌上轻轻一搁。"

    storyteller "握不住，便有人替他们握。十年不到，地方豪强借律法清洗异己。忠良被构陷，百姓求告无门。到头来，《大顺律》成了刀俎，百姓反倒成了鱼肉。"

    "堂下沉默了。有人低头喝茶，有人望着窗外发怔。茶馆外的叫卖声依旧，可这屋里头，安静得有些不像话。"

    storyteller "那皇帝呢？诸位要问了。"

    storyteller "深宫之中，消息一层层递上去，早变了味。奏报说天下太平，律法大行。皇帝信了。至死都信。"

    storyteller "他至死都以为，他的律法还在护着子民。殊不知——"

    "说书人顿了顿，收起折扇，目光从堂下茶客脸上缓缓扫过。"

    storyteller "北边那些为他殉道的人，早已化作了枯骨。消息传不进皇城。传不进去。"

    "茶馆外一阵风吹过，卷起几片落叶。日头西斜了些，光柱里的尘埃暗了半分。"

    scene bg_teahouse_window with ink_transition

    storyteller "后世定论——《大顺律》，祸国之法。"

    storyteller "至于真相如何……"

    "说书人微微一笑，不说了。"

    "茶客们散了。没有人追问。日头西沉，茶馆的灯笼一盏盏亮起来，映着市井的喧嚣。"

    "没有人知道，这故事才刚刚开始。"

    "真正的悲剧，从不在茶馆里——而在那些沉默的、传不出消息的角落。在那座孤零零的皇城里，在北风呼号的枯村里，在南方灯红酒绿的行辕中。"

    "那里的人，有的至死不知真相，有的知道真相却无法说出，有的说出真相却无人相信。"

    "这便是一切悲剧的源头。"

    stop music fadeout 3.0

    hide char_storyteller_half
    hide char_group_teahouse
    with portrait_fade

    scene bg_black with ink_transition

    $ renpy.force_autosave()

    jump chapter2_palace
