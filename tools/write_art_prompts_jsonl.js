#!/usr/bin/env node
// Writes a machine-readable JSONL prompt pack for external image tools. Does not generate images.

const fs = require("fs");
const path = require("path");

const project = path.resolve(__dirname, "..");
const output = path.join(project, "spec", "art_prompts.jsonl");

const positive = "ink wash painting, traditional Chinese art, ancient xuan paper texture, faded aged scroll effect, low saturation, soft ink smudge edges, layered mist atmosphere, minimalist negative space, 2D flat illustration, no 3D rendering, muted vintage tone";
const negative = "photorealistic, realistic human face, detailed facial features, bright saturated colors, cartoon, anime, geometric solid blocks, pure flat color, text, watermark, blurry, deformed, modern elements, plastic texture, vector graphic, sharp hard edges";

const backgroundSpecs = [
  ["bg_teahouse_wide.webp", "top-down wide view of ancient Chinese teahouse, wooden tile roofs, faint silhouettes of people inside, distant imperial city wall hidden in thick fog, sepia faded tone, atmospheric perspective, quiet observer view"],
  ["bg_teahouse_stage.webp", "eye-level interior of ancient Chinese teahouse, storytelling stage on left, wooden gavel and teacup on stage, silhouettes of audience sitting at tables, official script plaque on pillar, warm soft light from side window, negative space on right for character"],
  ["bg_teahouse_audience.webp", "close-up of teahouse audience, silhouettes of 7-8 people sitting at tables, some whispering, teabowls and peanut plates on tables, blurred stage in background, warm ochre gray tone, large blank space on top for text"],
  ["bg_teahouse_window.webp", "close-up of carved wooden lattice window, half cold teacup on windowsill, blurred imperial palace silhouette outside in fog, cool gray and light sepia, sense of distance between folk and court"],
  ["bg_bedchamber_wide.webp", "wide view of empty ancient Chinese emperor's bedroom, simple dragon bed on left, silhouette of old man lying on bed, flickering candlestick beside bed, old saddle hanging on opposite wall, half-open door with a line of cold light, large blank space, dark gold and dark gray tone, lonely desolate atmosphere"],
  ["bg_bedchamber_candle.webp", "close-up of candlestick in dark bedroom, flickering candle flame, shaking light shadows on dark wall, blurred dragon bed silhouette in background, dark vignette on edges, dark gold warm tone, dim hazy atmosphere, large dark area on right for text"],
  ["bg_bedchamber_illusion.webp", "middle view of emperor's bedroom, dragon bed on left, 4 half-transparent human silhouettes floating on right and middle, hazy smoke effect, dreamlike illusions, dim light, cool gray tone, unreal atmosphere"],
  ["bg_study_flashback.webp", "interior of ancient imperial study, desk full of memorials and books, bright candlelight, tall bookshelves on both sides, solemn depressing atmosphere, dark gray with dark cinnabar accents, symmetrical composition, reserved space on left and right for characters"],
  ["bg_court_flashback.webp", "interior of grand imperial court hall, tall vermilion columns on both sides, long stone steps leading to dragon throne on high platform, silhouettes of kneeling officials under steps, strong light from hall door, strong light and shadow contrast, vermilion and deep black tone, deep sense of depth"],
  ["bg_northwest_flashback.webp", "wide view of northwest loess plateau at dusk, several low military tents, faint bonfire light, distant continuous loess hills, vast open sky, bold unrestrained brush strokes, sand yellow and sky blue tone, full of vitality, horizon at lower third"],
  ["bg_bedchamber_end.webp", "close-up of dragon bed in bedroom, candle almost burnt out, dim light, stronger cold light from hall door, silent depressing atmosphere, dark gray cool tone, only faint warm candle light, bed occupies lower half, dark area on top for text"],
  ["bg_village_distant.webp", "distant view of northern Chinese village at night, crescent moon in sky, broken walls and ruined houses, faint burning smoke in distance, dead silence and desolation, cold gray and mud yellow tone, village occupies lower half, depressing atmosphere"],
  ["bg_village_tree.webp", "close-up of old locust tree at village entrance, twisted bare branches, thick trunk, muddy ground under tree, scattered broken farm tools and paper pages, small kneeling human silhouette at bottom, rough dry brush strokes, earth brown and cold gray tone, tree as visual center"],
  ["bg_square_flashback.webp", "sunlit village threshing ground, earthen wall, wheat stacks beside, man standing on stone pier holding a book, silhouettes of villagers sitting in semicircle around, soft daylight, simple warm atmosphere, warm ochre gray tone, speaker in center"],
  ["bg_paper_closeup.webp", "top-down close-up of muddy ground, crumpled torn law book half buried in mud, a muddy hand gently resting on paper edge, depressing atmosphere, symbol of broken ideal, mud yellow and dark gray tone, paper in center of frame"],
  ["bg_mansion_wide.webp", "wide view of southern official residence hall, carved lattice windows, large desk full of account books and documents, blurred jiangnan garden rockery outside window, exquisite but gloomy, warm green and dark gold accents, desk in center, reserved space on left and right for characters"],
  ["bg_mansion_desk.webp", "top-down close-up of official desk, abacus, account books, trade documents scattered, writing brush on inkstone, western clock in corner, blurred hall background, warm green and gold tone, desk occupies lower half, blank space on top for text"],
  ["bg_mansion_window.webp", "close-up of carved hall window, jiangnan night scene outside, scattered eaves, hazy moonlight, corner of table with wine pot and cups inside, calm quiet atmosphere, overall situation settled, cool slate blue and warm yellow glow, window view on right half"],
  ["bg_mansion_toast.webp", "middle view of official hall, wine pot and cups on desk, two silhouettes toasting each other on both sides, warm candlelight, heavy solemn atmosphere, no sense of celebration, warm green and dark gold warm light"],
  ["bg_ending_text.webp", "pure black gradient background, very faint ink wash smudge at bottom, no concrete elements, clean and simple, highlight central text, pure dark tone, minimalist, xuan paper subtle texture"],
  ["bg_mainmenu.webp", "tattered ancient map of Dashun territory, most areas covered by ink wash clouds and mist, only three faint marks visible, large clean blank area in middle lower part for buttons, worn edges, sepia base with ink smudges"],
  ["bg_save.webp", "top-down view of historian's desk, open blank history scroll, writing brush and inkstone beside, faint ink smudge on edges, low visual weight, light sepia tone, does not interfere with text list"],
  ["bg_settings.webp", "pure light ink xuan paper texture background, very faint ink wash smudge traces, no concrete elements, uniform brightness, ensures text readability, light beige yellow tone, minimalist"],
  ["bg_scroll.webp", "vertically unfolded ancient scroll, wooden rollers on top and bottom, natural wear texture on paper, large blank area in middle for timeline text, matches scroll unfold animation, old sepia tone"]
];

const characterFiles = [
  "char_storyteller_half_normal.webp", "char_storyteller_full.webp", "char_li_half_lie.webp", "char_li_half_angry.webp",
  "char_li_half_silent.webp", "char_li_full_young.webp", "char_li_closeup_hand.webp", "char_liu_half_sit.webp",
  "char_liu_half_argue.webp", "char_liu_half_back.webp", "char_liu_closeup_hand.webp", "char_ma_half_armcross.webp",
  "char_ma_half_sword.webp", "char_ma_full_toast.webp", "char_ma_closeup_hand.webp", "char_gu_half_bow.webp",
  "char_gu_half_breakdown.webp", "char_gu_half_kneel.webp", "char_gu_closeup_hand.webp", "char_xu_half_sit.webp",
  "char_xu_half_side.webp", "char_xu_full_illusion.webp", "char_lichengying_half_stand.webp", "char_lichengying_half_hunch.webp",
  "char_lichengying_full_illusion.webp", "char_han_half_carry.webp", "char_han_half_stern.webp", "char_han_full_illusion.webp",
  "char_zhao_half_speak.webp", "char_zhao_half_kneel.webp", "char_zhao_full_fall.webp", "char_zhao_closeup_hand.webp",
  "group_court_officals.webp", "group_villagers.webp", "group_four_people.webp", "group_tea_guests.webp"
];

const records = [];
for (const [filename, prompt] of backgroundSpecs) {
  records.push({ filename, kind: "background", size: "1920x1080", format: "webp", prompt: `${prompt}, ${positive}`, negative });
}
for (const filename of characterFiles) {
  const isCloseup = filename.includes("_closeup_");
  const isFull = filename.includes("_full") || filename.startsWith("group_");
  const size = isCloseup ? "1920x1080" : `height ${isFull ? 1000 : 900}px, width auto`;
  records.push({
    filename,
    kind: filename.startsWith("group_") ? "group-character" : "character",
    size,
    format: "webp",
    transparent_background: !isCloseup,
    prompt: `Generate ${filename.replace(/\.webp$/, "").replace(/_/g, " ")} as a pure ink wash silhouette, no facial features, transparent background for character assets, ${positive}`,
    negative
  });
}

fs.writeFileSync(output, records.map((record) => JSON.stringify(record)).join("\n") + "\n", "utf8");
console.log(`Wrote ${records.length} prompt records to ${output}`);
