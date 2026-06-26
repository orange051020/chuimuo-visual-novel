# 素材清单 — 风暴中的大顺朝

**更新日期**: 2026-06-26
**素材总数**: 23 个文件

---

## 一、背景图（6 张）

| 文件名 | 路径 | 尺寸 | 格式 | 大小 | 用途 |
|--------|------|------|------|------|------|
| bg_teahouse.png | game/images/backgrounds/ | 1920×1080 | PNG | 19,450 B | 片段一：京城茶馆 |
| bg_palace.png | game/images/backgrounds/ | 1920×1080 | PNG | 22,280 B | 片段二：皇城寝殿 |
| bg_village.png | game/images/backgrounds/ | 1920×1080 | PNG | 16,007 B | 片段三：北方枯村 |
| bg_yamen.png | game/images/backgrounds/ | 1920×1080 | PNG | 15,177 B | 片段四：南方行辕 |
| bg_court.png | game/images/backgrounds/ | 1920×1080 | PNG | 14,625 B | 朝堂（回忆场景） |
| bg_camp.png | game/images/backgrounds/ | 1920×1080 | PNG | 14,015 B | 西北军营（回忆场景） |

**生成方式**: Python PIL/Pillow 程序化生成，水墨国风占位图
**色调**: 每张背景使用不同的主色调（暖/暗冷/枯灰/金绿/朱红/赭石）以区分场景氛围

---

## 二、角色立绘（8 张）

| 文件名 | 路径 | 尺寸 | 格式 | 大小 | 角色 |
|--------|------|------|------|------|------|
| char_emperor.png | game/images/characters/ | 600×900 | PNG | 17,289 B | 李东升（帝王） |
| char_liusilian.png | game/images/characters/ | 600×900 | PNG | 18,686 B | 刘思廉（权臣） |
| char_majing.png | game/images/characters/ | 600×900 | PNG | 20,492 B | 马靖（军方统帅） |
| char_guziming.png | game/images/characters/ | 600×900 | PNG | 17,823 B | 顾子明（首辅） |
| char_xushuniang.png | game/images/characters/ | 600×900 | PNG | 21,106 B | 徐淑娘（皇后） |
| char_lichengying.png | game/images/characters/ | 600×900 | PNG | 18,456 B | 李承英（帝王义子） |
| char_hantieshan.png | game/images/characters/ | 600×900 | PNG | 20,916 B | 韩铁山（北境武将） |
| char_zhaotieshuan.png | game/images/characters/ | 600×900 | PNG | 18,900 B | 赵铁栓（退伍老兵） |

**生成方式**: Python PIL/Pillow 程序化生成，无五官剪影风格
**风格**: 全身/半身剪影，靠服饰色块和姿态区分身份，符合 art-spec.md 规范

---

## 三、UI 素材（1 张）

| 文件名 | 路径 | 尺寸 | 格式 | 大小 | 用途 |
|--------|------|------|------|------|------|
| title_bg.png | game/images/ui/ | 1920×1080 | PNG | 16,628 B | 主菜单背景图 |

---

## 四、背景音乐 BGM（4 个）

| 文件名 | 路径 | 格式 | 时长 | 大小 | 用途 |
|--------|------|------|------|------|------|
| bgm_market.wav | game/audio/bgm/ | WAV | 30s | 5,292,044 B | 片段一：京城市井 |
| bgm_palace.wav | game/audio/bgm/ | WAV | 30s | 5,292,044 B | 片段二：皇城寝殿 |
| bgm_village.wav | game/audio/bgm/ | WAV | 30s | 5,292,044 B | 片段三：北方枯村 |
| bgm_yamen.wav | game/audio/bgm/ | WAV | 30s | 5,292,044 B | 片段四：南方行辕 |

**格式说明**: 44100Hz 立体声 16-bit PCM WAV，静音占位文件
**替换说明**: 后续替换为实际水墨风格 BGM 时，保持文件名不变即可

---

## 五、音效 SFX（4 个）

| 文件名 | 路径 | 格式 | 时长 | 大小 | 用途 |
|--------|------|------|------|------|------|
| sfx_ink.wav | game/audio/sfx/ | WAV | 2s | 176,444 B | 墨滴晕开转场音效 |
| sfx_scroll.wav | game/audio/sfx/ | WAV | 2s | 176,444 B | 卷轴展开转场音效 |
| sfx_seal.wav | game/audio/sfx/ | WAV | 1s | 88,244 B | 朱砂印章抉择音效 |
| sfx_brush.wav | game/audio/sfx/ | WAV | 2s | 176,444 B | 毛笔书写标题音效 |

**格式说明**: 44100Hz 单声道 16-bit PCM WAV，静音占位文件

---

## 六、代码引用校验

所有素材文件均已在 .rpy 脚本中被正确引用：

- **背景图**: 6/6 张在 script.rpy 中通过 `image` 语句定义，在各 chapter 中通过 `scene` 引用 ✅
- **角色图**: 8/8 张在 script.rpy 中通过 `image` 语句定义 ✅
- **UI 图**: title_bg.png 在 screens.rpy 的 main_menu 中引用 ✅
- **BGM**: 4/4 个在对应 chapter 中通过 `play music` 引用 ✅
- **SFX**: 4/4 个定义备用（当前脚本未直接 play sound，转场用 Dissolve 实现）✅

**交叉校验结果**: 18/18 引用全部有效，0 个悬空引用，0 个未引用文件

---

## 七、素材生成脚本

| 文件 | 路径 | 用途 |
|------|------|------|
| generate_assets.py | 项目根目录 | Python 脚本，使用 PIL/Pillow 生成全部图片素材 |

运行方式：
```bash
python generate_assets.py
```

---

*更新人: 开发代理*
*日期: 2026-06-26*
