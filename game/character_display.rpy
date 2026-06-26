# character_display.rpy — 角色立绘对话显示系统
# 自动管理立绘显示/高亮/弱化/隐藏/回忆滤镜
# 通过 Character callback 实现自动化，不侵入原有剧情脚本
# 规则：说话→高亮 | 在场非说话→30%弱化 | 旁白→全部隐藏 | 回忆→柔光85% | 场景切换→清空

## === 立绘图像定义（与新素材系统同步）===

# 李东升（开国帝王）
image char_lidongsheng_normal = "images/character/char_emperor_bed.webp"
image char_lidongsheng_anger = "images/character/char_emperor_angry.webp"
image char_lidongsheng_despair = "images/character/char_emperor_silent.webp"
image char_lidongsheng_young = "images/character/char_emperor_young.webp"
image char_lidongsheng_closeup_1 = "images/character/char_emperor_hand.webp"

# 刘思廉（户部尚书）
image char_liusilian_normal = "images/character/char_liusilian_sit.webp"
image char_liusilian_argue = "images/character/char_liusilian_argue.webp"
image char_liusilian_decide = "images/character/char_liusilian_back.webp"
image char_liusilian_closeup_1 = "images/character/char_liusilian_hand.webp"

# 马靖（大将军）
image char_majing_normal = "images/character/char_majing_arms.webp"
image char_majing_press = "images/character/char_majing_sword.webp"
image char_majing_drink = "images/character/char_majing_toast.webp"
image char_majing_closeup_1 = "images/character/char_majing_hand.webp"

# 顾子明（内阁首辅）
image char_guziming_normal = "images/character/char_guziming_bow.webp"
image char_guziming_breakdown = "images/character/char_guziming_break.webp"
image char_guziming_kneel = "images/character/char_guziming_kneel.webp"
image char_guziming_closeup_1 = "images/character/char_guziming_hand.webp"

# 徐淑娘（皇后）
image char_xushuniang_normal = "images/character/char_xushuliang_sit.webp"
image char_xushuniang_worry = "images/character/char_xushuliang_side.webp"
image char_xushuniang_ghost = "images/character/char_xushuliang_ghost.webp"
image char_xushuniang_closeup_1 = "images/character/char_xushuliang_side.webp"

# 李承英（帝王义子）
image char_lichengying_young = "images/character/char_lichengying_stand.webp"
image char_lichengying_later = "images/character/char_lichengying_stoop.webp"
image char_lichengying_ghost = "images/character/char_lichengying_ghost.webp"

# 韩铁山（北境武将）
image char_hantieshan_normal = "images/character/char_hantieshan_knife.webp"
image char_hantieshan_kill = "images/character/char_hantieshan_kill.webp"
image char_hantieshan_ghost = "images/character/char_hantieshan_ghost.webp"

# 赵铁栓（退伍老兵）
image char_zhaotieshuan_preach = "images/character/char_zhaotieshuan_talk.webp"
image char_zhaotieshuan_despair = "images/character/char_zhaotieshuan_kneel.webp"
image char_zhaotieshuan_fall = "images/character/char_zhaotieshuan_fall.webp"
image char_zhaotieshuan_closeup_1 = "images/character/char_zhaotieshuan_hand.webp"

# 说书人
image char_shuoshuren_normal = "images/character/char_storyteller_half.webp"
image char_shuoshuren_full = "images/character/char_storyteller_full.webp"

# 群像
image group_court_officials = "images/character/char_group_court.webp"
image group_villagers = "images/character/char_group_village.webp"
image group_four_conspiracy = "images/character/char_group_four.webp"


## === 变换定义 ===

# 位置变换 — 立绘锚定画面底部，左右两侧或居中
transform portrait_left:
    xanchor 0.5 yanchor 1.0
    xpos 0.22 ypos 1.0

transform portrait_right:
    xanchor 0.5 yanchor 1.0
    xpos 0.78 ypos 1.0

transform portrait_center:
    xanchor 0.5 yanchor 1.0
    xpos 0.5 ypos 1.0

# 状态变换 — 高亮（当前说话者）
transform p_highlight:
    ease 0.3 alpha 1.0

# 状态变换 — 弱化（在场非说话者，30%透明度）
transform p_dim:
    ease 0.3 alpha 0.3

# 首次登场 — 淡入
transform p_fade_in:
    alpha 0.0
    ease 0.5 alpha 1.0

# 回忆闪回 — 柔光模糊 + 85%透明度
transform p_flashback:
    ease 0.3 alpha 0.85
    blur 5

# 回忆闪回首次登场
transform p_flashback_fade_in:
    alpha 0.0
    ease 0.5 alpha 0.85
    blur 5

# 幻觉角色 — 预渲染半透明，显示时不再额外弱化
transform p_ghost_show:
    alpha 1.0

# 全屏变换 — 特写/群像
transform portrait_fullscreen:
    xanchor 0.5 yanchor 0.5
    xalign 0.5 yalign 0.5


## === 立绘管理核心系统 ===

init -10 python:
    # 每个角色的立绘配置：默认姿态、画面位置、全部姿态图像名
    _portrait_config = {
        'emperor': {
            'default': 'normal',
            'pos': 'left',
            'poses': {
                'normal':  'char_lidongsheng_normal',
                'anger':   'char_lidongsheng_anger',
                'despair': 'char_lidongsheng_despair',
                'young':   'char_lidongsheng_young',
            }
        },
        'storyteller': {
            'default': 'normal',
            'pos': 'center',
            'poses': {
                'normal': 'char_shuoshuren_normal',
                'full':   'char_shuoshuren_full',
            }
        },
        'liusilian': {
            'default': 'normal',
            'pos': 'right',
            'poses': {
                'normal': 'char_liusilian_normal',
                'argue':  'char_liusilian_argue',
                'decide': 'char_liusilian_decide',
            }
        },
        'guziming': {
            'default': 'normal',
            'pos': 'left',
            'poses': {
                'normal':    'char_guziming_normal',
                'breakdown': 'char_guziming_breakdown',
                'kneel':     'char_guziming_kneel',
            }
        },
        'zhaotieshuan': {
            'default': 'preach',
            'pos': 'center',
            'poses': {
                'preach':   'char_zhaotieshuan_preach',
                'despair':  'char_zhaotieshuan_despair',
            }
        },
        'majing': {
            'default': 'normal',
            'pos': 'right',
            'poses': {
                'normal': 'char_majing_normal',
                'press':  'char_majing_press',
            }
        },
        'xushuniang': {
            'default': 'normal',
            'pos': 'left',
            'poses': {
                'normal': 'char_xushuniang_normal',
                'worry':  'char_xushuniang_worry',
                'ghost':  'char_xushuniang_ghost',
            }
        },
        'lichengying': {
            'default': 'young',
            'pos': 'right',
            'poses': {
                'young': 'char_lichengying_young',
                'later': 'char_lichengying_later',
                'ghost': 'char_lichengying_ghost',
            }
        },
        'hantieshan': {
            'default': 'normal',
            'pos': 'left',
            'poses': {
                'normal': 'char_hantieshan_normal',
                'kill':   'char_hantieshan_kill',
                'ghost':  'char_hantieshan_ghost',
            }
        },
    }

    # 运行时状态
    _on_stage = {}       # char_id -> {'pose': str}
    _is_flashback = False # 回忆闪回模式开关

    def _get_pos_transform(pos_name):
        """根据位置名获取位置变换"""
        if pos_name == 'left':
            return store.portrait_left
        elif pos_name == 'right':
            return store.portrait_right
        else:
            return store.portrait_center

    def _resolve_pose(config, pose):
        """解析姿态名，返回有效姿态键"""
        if pose and pose in config['poses']:
            return pose
        return config['default']

    def _is_ghost_pose(config, pose_key):
        """判断是否为幻觉姿态"""
        return pose_key == 'ghost'

    def _show_portrait(char_id, pose=None):
        """
        显示角色立绘：
        - 新角色 → 淡入（0.5秒）
        - 当前说话者 → 100%高亮
        - 在场非说话者 → 30%弱化（0.3秒过渡）
        - 回忆模式 → 全部85%透明度 + 模糊
        - 幻觉姿态 → 保持预渲染半透明，不额外弱化
        """
        config = _portrait_config.get(char_id)
        if not config:
            return

        pose_key = _resolve_pose(config, pose)
        image_name = config['poses'][pose_key]
        tag = "portrait_" + char_id
        pos_t = _get_pos_transform(config['pos'])
        is_new = char_id not in _on_stage
        is_ghost = _is_ghost_pose(config, pose_key)

        # 显示当前角色
        if is_ghost:
            # 幻觉角色 — 预渲染半透明，直接显示
            if is_new:
                renpy.show(tag, what=renpy.displayable(image_name),
                          at_list=[pos_t, store.p_fade_in])
            else:
                renpy.show(tag, what=renpy.displayable(image_name),
                          at_list=[pos_t, store.p_ghost_show])
        elif _is_flashback:
            # 回忆模式 — 柔光模糊 + 85%透明度
            if is_new:
                renpy.show(tag, what=renpy.displayable(image_name),
                          at_list=[pos_t, store.p_flashback_fade_in])
            else:
                renpy.show(tag, what=renpy.displayable(image_name),
                          at_list=[pos_t, store.p_flashback])
        else:
            # 正常模式 — 高亮当前说话者
            if is_new:
                renpy.show(tag, what=renpy.displayable(image_name),
                          at_list=[pos_t, store.p_fade_in])
            else:
                renpy.show(tag, what=renpy.displayable(image_name),
                          at_list=[pos_t, store.p_highlight])

        # 弱化其他在场角色（幻觉角色和回忆模式除外）
        if not is_ghost and not _is_flashback:
            for other_id in list(_on_stage.keys()):
                if other_id != char_id:
                    other_config = _portrait_config.get(other_id)
                    if other_config:
                        other_tag = "portrait_" + other_id
                        other_pose = _resolve_pose(other_config,
                                                    _on_stage[other_id].get('pose'))
                        other_image = other_config['poses'][other_pose]
                        other_pos = _get_pos_transform(other_config['pos'])
                        # 幻觉角色不被弱化
                        if not _is_ghost_pose(other_config, other_pose):
                            renpy.show(other_tag,
                                      what=renpy.displayable(other_image),
                                      at_list=[other_pos, store.p_dim])

        # 记录在场状态
        _on_stage[char_id] = {'pose': pose_key}

    def _hide_all_portraits():
        """隐藏所有立绘 — 旁白段落/场景切换时调用"""
        for char_id in list(_on_stage.keys()):
            renpy.hide("portrait_" + char_id)
        _on_stage.clear()

    def _on_scene_change(*args, **kwargs):
        """场景切换回调 — 清空立绘状态"""
        _hide_all_portraits()

    def make_portrait_callback(char_id):
        """创建角色立绘回调 — 角色说话时自动触发"""
        def callback(event, interact=True, **kwargs):
            if not interact:
                return
            if event == "begin":
                _show_portrait(char_id)
        return callback

    def make_narration_callback():
        """创建旁白回调 — 旁白时自动隐藏所有立绘"""
        def callback(event, interact=True, **kwargs):
            if not interact:
                return
            if event == "begin":
                _hide_all_portraits()
        return callback

    # 注册场景切换回调 — scene 语句执行时自动清空立绘
    if _on_scene_change not in config.scene_callbacks:
        config.scene_callbacks.append(_on_scene_change)


## === 便捷函数 — 可在剧情脚本中通过 $ 语句手动调用 ===

init python:
    def set_character_pose(char_id, pose):
        """手动切换角色立绘姿态
        例: $ set_character_pose('emperor', 'anger')
        """
        _show_portrait(char_id, pose)

    def set_flashback(state):
        """开启/关闭回忆闪回模式
        例: $ set_flashback(True)  → 进入回忆
            $ set_flashback(False) → 回到现实
        """
        store._is_flashback = state
        # 刷新所有在场角色的显示效果
        for cid in list(_on_stage.keys()):
            info = _on_stage[cid]
            _show_portrait(cid, info.get('pose'))

    def clear_portrait_stage():
        """手动清空所有立绘
        例: $ clear_portrait_stage()
        """
        _hide_all_portraits()

    def show_closeup(image_name):
        """显示全屏特写立绘
        例: $ show_closeup('char_lidongsheng_closeup_1')
        """
        renpy.show("portrait_closeup",
                   what=renpy.displayable(image_name),
                   at_list=[store.portrait_fullscreen, store.p_fade_in])

    def hide_closeup():
        """隐藏特写立绘"""
        renpy.hide("portrait_closeup")

    def show_group(image_name):
        """显示全屏群像立绘
        例: $ show_group('group_court_officials')
        """
        renpy.show("portrait_group",
                   what=renpy.displayable(image_name),
                   at_list=[store.portrait_fullscreen, store.p_fade_in])

    def hide_group():
        """隐藏群像立绘"""
        renpy.hide("portrait_group")

    def show_ghost_portrait(char_id, pose='ghost'):
        """显示幻觉角色立绘 — 用于临终幻觉场景
        例: $ show_ghost_portrait('xushuniang')
        """
        _show_portrait(char_id, pose)

    def hide_portrait(char_id):
        """隐藏单个角色立绘
        例: $ hide_portrait('emperor')
        """
        if char_id in _on_stage:
            renpy.hide("portrait_" + char_id)
            del _on_stage[char_id]
