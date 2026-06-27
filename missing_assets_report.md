# Missing External Art Assets

Codex must not generate images. The following files must be produced by the external text-to-image pipeline and placed in `external-art-drop/`.

Total required: 60
Present in external-art-drop: 0
Missing: 60

## Missing Background/UI Assets

- bg_teahouse_wide.webp
- bg_teahouse_stage.webp
- bg_teahouse_audience.webp
- bg_teahouse_window.webp
- bg_bedchamber_wide.webp
- bg_bedchamber_candle.webp
- bg_bedchamber_illusion.webp
- bg_study_flashback.webp
- bg_court_flashback.webp
- bg_northwest_flashback.webp
- bg_bedchamber_end.webp
- bg_village_distant.webp
- bg_village_tree.webp
- bg_square_flashback.webp
- bg_paper_closeup.webp
- bg_mansion_wide.webp
- bg_mansion_desk.webp
- bg_mansion_window.webp
- bg_mansion_toast.webp
- bg_ending_text.webp
- bg_mainmenu.webp
- bg_save.webp
- bg_settings.webp
- bg_scroll.webp

## Missing Character/Group Assets

- char_storyteller_half_normal.webp
- char_storyteller_full.webp
- char_li_half_lie.webp
- char_li_half_angry.webp
- char_li_half_silent.webp
- char_li_full_young.webp
- char_li_closeup_hand.webp
- char_liu_half_sit.webp
- char_liu_half_argue.webp
- char_liu_half_back.webp
- char_liu_closeup_hand.webp
- char_ma_half_armcross.webp
- char_ma_half_sword.webp
- char_ma_full_toast.webp
- char_ma_closeup_hand.webp
- char_gu_half_bow.webp
- char_gu_half_breakdown.webp
- char_gu_half_kneel.webp
- char_gu_closeup_hand.webp
- char_xu_half_sit.webp
- char_xu_half_side.webp
- char_xu_full_illusion.webp
- char_lichengying_half_stand.webp
- char_lichengying_half_hunch.webp
- char_lichengying_full_illusion.webp
- char_han_half_carry.webp
- char_han_half_stern.webp
- char_han_full_illusion.webp
- char_zhao_half_speak.webp
- char_zhao_half_kneel.webp
- char_zhao_full_fall.webp
- char_zhao_closeup_hand.webp
- group_court_officals.webp
- group_villagers.webp
- group_four_people.webp
- group_tea_guests.webp

## Next Commands

```bash
node chuimuo-visual-novel/tools/import_external_assets.js --dry-run
node chuimuo-visual-novel/tools/import_external_assets.js
node work/tests/validate_assets_ready.js
node chuimuo-visual-novel/tools/prebuild_check.js
```
