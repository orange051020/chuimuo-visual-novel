# 最终验收报告

## 剧情验收

- 李东升开口结局遗言必须为“老百姓以后会怎么样，只有天知道。”
- 默然结局不得出现李东升临终台词
- 十二年时间线、御书房争执、顾子明悬疑、赵铁栓殉道必须落地

## 美术素材验收

- 背景图与UI底图：24 张
- 角色立绘、特写、群像：36 张
- 总计：60 张 WebP 文件
- 所有素材必须通过 `node work/tests/validate_assets_ready.js`

## 功能验收

- Ren'Py 入口 `label start` 可进入 `chapter_prologue`
- 文字样式、对话框样式、选择菜单、转场定义存在
- 素材路径全部来自 `game/images/asset_list.md`

## 部署验收

- renpyweb 输出存在于 `build-web/`
- `web-meta.html` 已注入 `build-web/index.html`
- GitHub Pages workflow 使用 `build-web/` 作为发布目录
- 匿名浏览器可打开最终 URL

## 自动化检查输出

### C:\Program Files\nodejs\node.exe work/tests/validate_project.js

Exit code: 0

```text
Project validation passed.
```

### C:\Program Files\nodejs\node.exe work/tests/validate_assets_ready.js

Exit code: 1

```text
Missing assets:
bg_teahouse_wide.webp
bg_teahouse_stage.webp
bg_teahouse_audience.webp
bg_teahouse_window.webp
bg_bedchamber_wide.webp
bg_bedchamber_candle.webp
bg_bedchamber_illusion.webp
bg_study_flashback.webp
bg_court_flashback.webp
bg_northwest_flashback.webp
bg_bedchamber_end.webp
bg_village_distant.webp
bg_village_tree.webp
bg_square_flashback.webp
bg_paper_closeup.webp
bg_mansion_wide.webp
bg_mansion_desk.webp
bg_mansion_window.webp
bg_mansion_toast.webp
bg_ending_text.webp
bg_mainmenu.webp
bg_save.webp
bg_settings.webp
bg_scroll.webp
char_storyteller_half_normal.webp
char_storyteller_full.webp
char_li_half_lie.webp
char_li_half_angry.webp
char_li_half_silent.webp
char_li_full_young.webp
char_li_closeup_hand.webp
char_liu_half_sit.webp
char_liu_half_argue.webp
char_liu_half_back.webp
char_liu_closeup_hand.webp
char_ma_half_armcross.webp
char_ma_half_sword.webp
char_ma_full_toast.webp
char_ma_closeup_hand.webp
char_gu_half_bow.webp
char_gu_half_breakdown.webp
char_gu_half_kneel.webp
char_gu_closeup_hand.webp
char_xu_half_sit.webp
char_xu_half_side.webp
char_xu_full_illusion.webp
char_lichengying_half_stand.webp
char_lichengying_half_hunch.webp
char_lichengying_full_illusion.webp
char_han_half_carry.webp
char_han_half_stern.webp
char_han_full_illusion.webp
char_zhao_half_speak.webp
char_zhao_half_kneel.webp
char_zhao_full_fall.webp
char_zhao_closeup_hand.webp
group_court_officals.webp
group_villagers.webp
group_four_people.webp
group_tea_guests.webp
```
