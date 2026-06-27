#!/usr/bin/env node
// Writes external high-quality art delivery files. Does not generate images.

const fs = require("fs");
const path = require("path");

const project = path.resolve(__dirname, "..");
const root = path.resolve(project, "..");
const dropDir = path.join(root, "external-art-drop");
const txtOut = path.join(dropDir, "批量生图指引_高清版.txt");
const mdOut = path.join(dropDir, "投放说明.md");
const jsonlOut = path.join(project, "spec", "art_prompts.jsonl");

fs.mkdirSync(dropDir, { recursive: true });

const positive = "high resolution, sharp details, fine ink texture, ink wash painting, traditional Chinese art, ancient xuan paper texture, faded aged scroll effect, low saturation, soft ink smudge edges, layered mist atmosphere, minimalist negative space, 2D flat illustration, no 3D rendering, muted vintage tone, crisp smooth edges";
const negative = "photorealistic, realistic human face, detailed facial features, bright saturated colors, cartoon, anime, geometric solid blocks, pure flat color, text, watermark, blurry, pixelated, jagged edges, deformed, modern elements, plastic texture, vector graphic, sharp hard edges, low quality, grainy";

const backgrounds = [
  ["bg_teahouse_wide.webp", "top-down wide view of ancient Chinese teahouse, wooden tile roofs, faint silhouettes of people inside, distant imperial city wall hidden in thick fog, sepia faded tone, quiet observer view, rich ink layers"],
  ["bg_teahouse_stage.webp", "eye-level interior of ancient Chinese teahouse, storytelling stage on left, wooden gavel and teacup on stage, silhouettes of audience sitting at tables, official script plaque on pillar, warm soft light from side window, negative space on right for character, fine wood texture"],
  ["bg_teahouse_audience.webp", "close-up of teahouse audience, silhouettes of 7-8 people sitting at tables, some whispering, teabowls and peanut plates on tables, blurred stage in background, warm ochre gray tone, large blank space on top for text, soft atmosphere"],
  ["bg_teahouse_window.webp", "close-up of carved wooden lattice window, half cold teacup on windowsill, blurred imperial palace silhouette outside in fog, distant and detached atmosphere, cool gray and light sepia, sense of distance between folk and court, delicate window carving"],
  ["bg_bedchamber_wide.webp", "wide view of empty ancient Chinese emperor's bedroom, simple dragon bed on left, silhouette of old man lying on bed, flickering candlestick beside bed, old saddle hanging on opposite wall, half-open door with a line of cold light, large blank space, dark gold and dark gray tone, lonely desolate atmosphere, deep ink gradient"],
  ["bg_bedchamber_candle.webp", "close-up of candlestick in dark bedroom, flickering candle flame, shaking light shadows on dark wall, blurred dragon bed silhouette in background, dark vignette on edges, dark gold warm tone, dim hazy atmosphere, large dark area on right for text, realistic flame glow"],
  ["bg_bedchamber_illusion.webp", "middle view of emperor's bedroom, dragon bed on left, 4 half-transparent human silhouettes floating on right and middle, hazy smoke effect, dreamlike illusions, dim light, cool gray tone, unreal atmosphere, soft mist layers"],
  ["bg_study_flashback.webp", "interior of ancient imperial study, desk full of memorials and books, bright candlelight, tall bookshelves on both sides, solemn depressing atmosphere, dark gray with dark cinnabar accents, symmetrical composition, reserved space on left and right for characters, detailed book spines"],
  ["bg_court_flashback.webp", "interior of grand imperial court hall, tall vermilion columns on both sides, long stone steps leading to dragon throne on high platform, silhouettes of kneeling officials under steps, strong light from hall door, strong light and shadow contrast, vermilion and deep black tone, deep sense of depth, majestic structure"],
  ["bg_northwest_flashback.webp", "wide view of northwest loess plateau at dusk, several low military tents, faint bonfire light, distant continuous loess hills, vast open sky, bold unrestrained brush strokes, sand yellow and sky blue tone, full of vitality, horizon at lower third, rich landscape layers"],
  ["bg_bedchamber_end.webp", "close-up of dragon bed in bedroom, candle almost burnt out, dim light, stronger cold light from hall door, silent depressing atmosphere, dark gray cool tone, only faint warm candle light, bed occupies lower half, dark area on top for text, fading atmosphere"],
  ["bg_village_distant.webp", "distant view of northern Chinese village at night, crescent moon in sky, broken walls and ruined houses, faint burning smoke in distance, dead silence and desolation, cold gray and mud yellow tone, village occupies lower half, depressing atmosphere, deep night gradient"],
  ["bg_village_tree.webp", "close-up of old locust tree at village entrance, twisted bare branches, thick trunk, muddy ground under tree, scattered broken farm tools and paper pages, small kneeling human silhouette at bottom, rough dry brush strokes, earth brown and cold gray tone, tree as visual center, rough bark texture"],
  ["bg_square_flashback.webp", "sunlit village threshing ground, earthen wall, wheat stacks beside, man standing on stone pier holding a book, silhouettes of villagers sitting in semicircle around, soft daylight, simple warm atmosphere, warm ochre gray tone, speaker in center, peaceful countryside feel"],
  ["bg_paper_closeup.webp", "top-down close-up of muddy ground, crumpled torn law book half buried in mud, a muddy hand gently resting on paper edge, depressing atmosphere, symbol of broken ideal, mud yellow and dark gray tone, paper in center of frame, detailed paper fiber texture"],
  ["bg_mansion_wide.webp", "wide view of southern official residence hall, carved lattice windows, large desk full of account books and documents, blurred jiangnan garden rockery outside window, exquisite but gloomy, warm green and dark gold accents, desk in center, reserved space on left and right for characters, elegant woodwork"],
  ["bg_mansion_desk.webp", "top-down close-up of official desk, abacus, account books, trade documents scattered, writing brush on inkstone, western clock in corner, blurred hall background, warm green and gold tone, desk occupies lower half, blank space on top for text, detailed desk items"],
  ["bg_mansion_window.webp", "close-up of carved hall window, jiangnan night scene outside, scattered eaves, hazy moonlight, corner of table with wine pot and cups inside, calm quiet atmosphere, overall situation settled, cool slate blue and warm yellow glow, window view on right half, soft moonlight"],
  ["bg_mansion_toast.webp", "middle view of official hall, wine pot and cups on desk, two silhouettes toasting each other on both sides, warm candlelight, heavy solemn atmosphere, no sense of celebration, warm green and dark gold warm light, deep atmosphere"],
  ["bg_ending_text.webp", "pure black gradient background, very faint ink wash smudge at bottom, no concrete elements, clean and simple, highlight central text, pure dark tone, minimalist, xuan paper subtle texture, smooth gradient"],
  ["bg_mainmenu.webp", "tattered ancient map of Dashun territory, most areas covered by ink wash clouds and mist, only three faint marks visible, large clean blank area in middle lower part for buttons, worn edges, xuan paper texture, sepia base with ink smudges, detailed map lines"],
  ["bg_save.webp", "top-down view of historian's desk, open blank history scroll, writing brush and inkstone beside, faint ink smudge on edges, low visual weight, light sepia tone, does not interfere with text list, delicate paper texture"],
  ["bg_settings.webp", "pure light ink xuan paper texture background, very faint ink wash smudge traces, no concrete elements, uniform brightness, ensures text readability, light beige yellow tone, minimalist, fine paper grain"],
  ["bg_scroll.webp", "vertically unfolded ancient scroll, wooden rollers on top and bottom, natural wear texture on paper, large blank area in middle for timeline text, matches scroll unfold animation, old sepia tone, detailed scroll edges"]
];

const characters = [
  ["char_storyteller_half_normal.webp", 900, "half body silhouette of ancient Chinese storyteller standing behind stage, one hand raised as if patting gavel, relaxed posture, ochre brown ink wash, soft ink edges, no facial features, smooth silhouette outline"],
  ["char_storyteller_full.webp", 1000, "full body silhouette of storyteller standing on stage, ochre brown ink wash, no face, clear proportion, soft edge blur"],
  ["char_li_half_lie.webp", 900, "half body silhouette of old emperor lying on bed, side view, upper body slightly raised, holding a document, tired and old, dark cinnabar ink wash, soft edges, no facial features, accurate body proportion"],
  ["char_li_half_angry.webp", 900, "half body silhouette of emperor leaning forward, one hand supporting on bed, angry and tense posture, dark cinnabar ink wash, no face, strong body language"],
  ["char_li_half_silent.webp", 900, "half body silhouette of emperor with head down, hunched shoulders, silent and hopeless, dark cinnabar ink wash, no face, depressed posture"],
  ["char_li_full_young.webp", 1000, "full body silhouette of young emperor in military uniform, straight posture, sabre at waist, high spirited, dark cinnabar ink wash, no face, tall and straight figure"],
  ["char_li_closeup_hand.webp", 1080, "close-up of old hand with old scars, pinching a page of law book, candlelight reflection, dark cinnabar ink wash style, detailed skin texture, clear paper fiber"],
  ["char_liu_half_sit.webp", 900, "half body silhouette of civil official sitting upright at desk, hand on account book, calm and steady, slate blue gray ink wash, no face, dignified posture"],
  ["char_liu_half_argue.webp", 900, "half body silhouette of civil official slightly leaning forward, writing brush hovering in air, forbearing and tense, slate blue gray ink wash, no face, restrained emotion"],
  ["char_liu_half_back.webp", 900, "back view half body silhouette of civil official, one hand behind back, thinking and decisive, slate blue gray ink wash, no face, deep thinking state"],
  ["char_liu_closeup_hand.webp", 1080, "close-up of hand with distinct knuckles, moving abacus beads, slate blue gray ink wash style, clear abacus details, natural hand shape"],
  ["char_ma_half_armcross.webp", 900, "half body silhouette of general standing with arms crossed, sabre at waist, broad and steady, deep black with ochre texture ink wash, no face, strong build"],
  ["char_ma_half_sword.webp", 900, "half body silhouette of general with one hand on sabre hilt, leaning forward slightly, serious and pressing, deep black ink wash, no face, solemn momentum"],
  ["char_ma_full_toast.webp", 1000, "full body silhouette of general toasting sideways, relaxed and slightly drunk, deep black ink wash, no face, natural posture"],
  ["char_ma_closeup_hand.webp", 1080, "close-up of rough calloused hand holding bronze wine cup, deep black ink wash style, clear cup outline, rough hand texture"],
  ["char_gu_half_bow.webp", 900, "half body silhouette of chief assistant bowing slightly, holding document in arms, respectful and silent, cool gray ink wash, no face, humble posture"],
  ["char_gu_half_breakdown.webp", 900, "half body silhouette of man bending over desk, shoulders trembling, painful and broken down, cool gray ink wash, no face, intense emotional state"],
  ["char_gu_half_kneel.webp", 900, "half body silhouette of man kneeling on both knees, hands on ground, head low, resolute, cool gray ink wash, no face, kneeling posture accurate"],
  ["char_gu_closeup_hand.webp", 1080, "close-up of trembling fingertips holding crumpled secret memorial, cool gray ink wash style, crumpled paper texture, trembling hand details"],
  ["char_xu_half_sit.webp", 900, "half body silhouette of empress sitting upright, holding a bowl of porridge, gentle and calm, dark cinnabar ink wash, no face, soft posture"],
  ["char_xu_half_side.webp", 900, "side view half body silhouette of empress holding weaving shuttle, body slightly tense, worried, dark cinnabar ink wash, no face, anxious state"],
  ["char_xu_full_illusion.webp", 1000, "full body half transparent silhouette of empress, hazy and blurred, illusion effect, dark cinnabar ink wash, no face, soft translucent effect"],
  ["char_lichengying_half_stand.webp", 900, "half body silhouette of young man in old cloak, straight posture, high spirited, gray brown ink wash, no face, youthful vibe"],
  ["char_lichengying_half_hunch.webp", 900, "half body silhouette of young man with slightly hunched back, standing with hands down, heavy and gloomy, gray brown ink wash, no face, depressed state"],
  ["char_lichengying_full_illusion.webp", 1000, "full body half transparent silhouette of young man with head down, silent, gray brown ink wash, no face, translucent hazy effect"],
  ["char_han_half_carry.webp", 900, "half body silhouette of military officer carrying sabre on shoulder, slanting posture but steady as rock, deep ochre ink wash, no face, bold posture"],
  ["char_han_half_stern.webp", 900, "half body silhouette of military officer with hand on sabre, straight posture, cold and harsh, deep ochre ink wash, no face, stern momentum"],
  ["char_han_full_illusion.webp", 1000, "full body half transparent silhouette of military officer, sabre resting on ground, deep ochre ink wash, no face, translucent illusion effect"],
  ["char_zhao_half_speak.webp", 900, "half body silhouette of peasant standing on stone pier, holding law book in one hand, other hand open, passionate and earnest, earth brown ink wash, no face, impassioned posture"],
  ["char_zhao_half_kneel.webp", 900, "half body silhouette of peasant kneeling on both knees, head down, clutching torn book pages, desperate and helpless, earth brown ink wash, no face, desperate state"],
  ["char_zhao_full_fall.webp", 1000, "full body silhouette of peasant lying on side, torn law pages scattered beside him, earth brown ink wash, no face, fallen posture accurate"],
  ["char_zhao_closeup_hand.webp", 1080, "close-up of muddy hand tightly clutching crumpled law pages, earth brown ink wash style, mud texture clear, paper crumpled details"],
  ["group_court_officals.webp", 1000, "group silhouettes of many kneeling officials in court, no individual distinction, only show group scale, ink wash style, dark gray, neat group arrangement"],
  ["group_villagers.webp", 1000, "group silhouettes of villagers sitting in semicircle, scattered heights, ink wash, earth brown, natural postures"],
  ["group_four_people.webp", 1000, "four full body silhouettes side by side, half transparent soft light effect, ink wash style, mixed tones, distinct height difference"],
  ["group_tea_guests.webp", 1000, "group silhouettes of tea guests scattered, different postures, ink wash style, ochre brown, casual atmosphere"]
];

const records = [];
const lines = [];
lines.push("【全局统一要求】");
lines.push(`生图模型：优先使用 GPT 最高阶生图能力 / 专业国风模型，保证画质高清、细节细腻`);
lines.push(`全局正向关键词：${positive}`);
lines.push(`全局负面关键词：${negative}`);
lines.push("输出格式：WebP，质量 90%，文件名零误差，统一输出到 external-art-drop/ 根目录");
lines.push("");
lines.push("【第一类：背景图与UI底图 共24张 | 统一尺寸1920×1080 | 无透明通道】");
lines.push("序号 | 精确文件名 | 完整Prompt");
backgrounds.forEach(([filename, prompt], i) => {
  const full = `${positive}, ${prompt}`;
  lines.push(`${i + 1} | ${filename} | ${full}`);
  records.push({ filename, category: "background", width: 1920, height: 1080, transparent: false, prompt_positive: full, prompt_negative: negative, max_size_mb: 2 });
});
lines.push("");
lines.push("【第二类：角色立绘/特写/群像 共36张 | 尺寸见单条标注 | 立绘必须带透明通道】");
lines.push("序号 | 精确文件名 | 尺寸要求 | 完整Prompt");
characters.forEach(([filename, height, prompt], i) => {
  const isCloseup = height === 1080;
  const width = isCloseup ? 1920 : null;
  const full = `${positive}, ${prompt}`;
  const sizeText = isCloseup ? "1920×1080，无透明通道" : `高度${height}px，宽度自适应，透明背景通道`;
  lines.push(`${i + 25} | ${filename} | ${sizeText} | ${full}`);
  records.push({ filename, category: isCloseup ? "closeup" : "character", width, height, transparent: !isCloseup, prompt_positive: full, prompt_negative: negative, max_size_mb: isCloseup ? 2 : 0.5 });
});

fs.writeFileSync(txtOut, lines.join("\n"), "utf8");
fs.writeFileSync(jsonlOut, records.map((record) => JSON.stringify(record)).join("\n") + "\n", "utf8");
fs.writeFileSync(mdOut, [
  "# 投放说明",
  "",
  "1. 将本目录下所有 prompt 提交给外部生图工具生成对应 WebP 图片。",
  "2. 生成后的 60 张 .webp 文件直接放回本目录，不需要建子文件夹。",
  "3. 文件名必须与清单完全一致，否则导入脚本无法识别。",
  "4. 全部投放完成后，Codex 会自动执行导入-校验-编译-部署全流程。",
  "",
  "导入前检查：",
  "",
  "```bash",
  "node chuimuo-visual-novel/tools/import_external_assets.js --dry-run",
  "```",
  ""
].join("\n"), "utf8");

console.log(`Wrote HD delivery pack: ${txtOut}`);
console.log(`Updated JSONL: ${jsonlOut}`);
console.log(`Wrote drop instructions: ${mdOut}`);
