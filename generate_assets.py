#!/usr/bin/env python3
"""
generate_assets.py — 风暴中的大顺朝 占位素材生成
生成场景背景、角色剪影、UI元素的占位图
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# 项目路径
BASE = os.path.dirname(os.path.abspath(__file__))

# 色值体系
COLORS = {
    "ink_black": (44, 44, 44),
    "ink_black_deep": (26, 26, 26),
    "silk_yellow": (212, 197, 169),
    "silk_yellow_dark": (194, 178, 138),
    "cinnabar": (139, 58, 58),
    "cinnabar_light": (160, 82, 79),
    "stone_blue": (91, 122, 140),
    "stone_blue_dark": (74, 106, 122),
    "ochre": (139, 107, 74),
    "ochre_dark": (107, 75, 58),
    "rice_white": (245, 240, 232),
    "withered_gray": (139, 139, 122),
    "false_green": (74, 90, 58),
    "false_gold": (139, 122, 58),
}

def create_gradient(width, height, color1, color2, vertical=True):
    """创建渐变背景"""
    img = Image.new("RGB", (width, height), color1)
    draw = ImageDraw.Draw(img)
    if vertical:
        for y in range(height):
            ratio = y / height
            r = int(color1[0] + (color2[0] - color1[0]) * ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * ratio)
            b = int(color1[2] + (color2[2] - color1[2]) * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    else:
        for x in range(width):
            ratio = x / width
            r = int(color1[0] + (color2[0] - color1[0]) * ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * ratio)
            b = int(color1[2] + (color2[2] - color1[2]) * ratio)
            draw.line([(x, 0), (x, height)], fill=(r, g, b))
    return img

def add_text_centered(draw, text, y, width, color, size=36):
    """在图片中央添加文字"""
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", size)
    except:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", size)
        except:
            font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, y), text, fill=color, font=font)

def add_scene_elements(img, scene_type):
    """为场景背景添加简单元素"""
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = img.size

    if scene_type == "teahouse":
        # 茶馆：暖色调，添加灯笼和桌椅剪影
        # 灯笼
        for lx in [200, 1600]:
            draw.ellipse([lx-30, 100, lx+30, 180], fill=(139, 58, 58, 120))
            draw.line([lx, 80, lx, 100], fill=(107, 75, 58, 150), width=2)
        # 桌子剪影
        draw.rectangle([400, 700, 700, 750], fill=(107, 75, 58, 80))
        draw.rectangle([1200, 700, 1500, 750], fill=(107, 75, 58, 80))
        # 说书台
        draw.rectangle([850, 650, 1070, 800], fill=(107, 75, 58, 100))

    elif scene_type == "palace":
        # 寝殿：暗冷调，添加柱子和帷幔
        # 柱子
        for px in [100, 500, 1420, 1820]:
            draw.rectangle([px-20, 0, px+20, h], fill=(26, 26, 26, 180))
        # 帷幔
        draw.rectangle([600, 0, 1320, 300], fill=(44, 44, 44, 100))
        # 烛光
        draw.ellipse([920, 850, 1000, 930], fill=(212, 197, 169, 60))

    elif scene_type == "village":
        # 枯村：枯灰调，添加断壁和枯树
        # 枯树
        for tx in [200, 300, 1500, 1700]:
            draw.line([tx, 400, tx, 800], fill=(107, 75, 58, 100), width=8)
            draw.line([tx, 500, tx-40, 450], fill=(107, 75, 58, 80), width=4)
            draw.line([tx, 520, tx+35, 470], fill=(107, 75, 58, 80), width=4)
        # 断壁
        draw.rectangle([500, 600, 800, 700], fill=(139, 139, 122, 60))
        draw.rectangle[1100, 580, 1400, 690] if False else draw.rectangle([1100, 580, 1400, 690], fill=(139, 139, 122, 50))

    elif scene_type == "yamen":
        # 行辕：虚浮金绿调，添加书案和卷轴
        # 书案
        draw.rectangle([300, 700, 1620, 800], fill=(139, 122, 58, 80))
        # 卷轴
        for cx in [400, 600, 800]:
            draw.rectangle([cx, 650, cx+80, 700], fill=(194, 178, 138, 60))
        # 窗外灯火
        draw.ellipse[1700, 200, 1800, 300] if False else draw.ellipse([1700, 200, 1800, 300], fill=(139, 122, 58, 40))

    elif scene_type == "court":
        # 朝堂：庄严暗调，添加龙椅和朝柱
        # 龙椅（空）
        draw.rectangle([810, 500, 1110, 750], fill=(139, 58, 58, 50))
        # 朝柱
        for px in [200, 500, 1420, 1720]:
            draw.rectangle([px-25, 0, px+25, h], fill=(139, 58, 58, 60))

    elif scene_type == "camp":
        # 军营：苍凉黄褐调，添加帐篷和旗帜
        # 帐篷
        for tx in [300, 960, 1620]:
            draw.polygon([(tx-80, 800), (tx+80, 800), (tx, 650)], fill=(139, 107, 74, 70))
        # 旗帜
        draw.line[600, 300, 600, 600] if False else draw.line([(600, 300), (600, 600)], fill=(139, 58, 58, 80), width=3)
        draw.rectangle([600, 300, 700, 380], fill=(139, 58, 58, 60))

def generate_backgrounds():
    """生成6大场景背景"""
    bg_dir = os.path.join(BASE, "game", "images", "backgrounds")
    os.makedirs(bg_dir, exist_ok=True)

    scenes = [
        ("bg_teahouse", "teahouse", COLORS["silk_yellow"], COLORS["silk_yellow_dark"], "京城茶馆"),
        ("bg_palace", "palace", COLORS["ink_black_deep"], COLORS["stone_blue_dark"], "皇城寝殿"),
        ("bg_village", "village", COLORS["withered_gray"], COLORS["ochre_dark"], "北方枯村"),
        ("bg_yamen", "yamen", COLORS["false_green"], COLORS["false_gold"], "南方行辕"),
        ("bg_court", "court", COLORS["ink_black_deep"], COLORS["cinnabar"], "朝堂"),
        ("bg_camp", "camp", COLORS["ochre"], COLORS["ochre_dark"], "西北军营"),
    ]

    for name, scene_type, color1, color2, label in scenes:
        img = create_gradient(1920, 1080, color1, color2)
        add_scene_elements(img, scene_type)
        img = img.filter(ImageFilter.GaussianBlur(radius=3))

        draw = ImageDraw.Draw(img, "RGBA")
        # 暗角效果
        overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rectangle([0, 0, 1920, 1080], fill=(0, 0, 0, 40))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

        draw = ImageDraw.Draw(img, "RGBA")
        add_text_centered(draw, label, 980, 1920, (245, 240, 232, 120), size=28)

        path = os.path.join(bg_dir, f"{name}.png")
        img.save(path, "PNG")
        print(f"  [BG] {name}.png")

def generate_characters():
    """生成8角色剪影立绘"""
    char_dir = os.path.join(BASE, "game", "images", "characters")
    os.makedirs(char_dir, exist_ok=True)

    characters = [
        ("char_emperor", COLORS["cinnabar"], "李东升", "龙袍宽袖"),
        ("char_liusilian", COLORS["ochre"], "刘思廉", "官服紧束"),
        ("char_majing", COLORS["stone_blue_dark"], "马靖", "铠甲肩甲"),
        ("char_guziming", COLORS["ochre_dark"], "顾子明", "文官常服"),
        ("char_xushuniang", COLORS["cinnabar_light"], "徐淑娘", "凤袍飘逸"),
        ("char_lichengying", COLORS["stone_blue"], "李承英", "青年武官"),
        ("char_hantieshan", COLORS["ochre_dark"], "韩铁山", "北境厚甲"),
        ("char_zhaotieshuan", COLORS["withered_gray"], "赵铁栓", "粗布老兵衣"),
    ]

    for name, color, char_name, desc in characters:
        img = Image.new("RGBA", (600, 900), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img, "RGBA")

        # 头部（圆形剪影）
        draw.ellipse([230, 80, 370, 220], fill=color + (200,))

        # 身体（梯形剪影 — 服饰轮廓）
        if "宽袖" in desc:
            # 宽袖龙袍
            points = [(200, 240), (400, 240), (480, 600), (120, 600)]
            draw.polygon(points, fill=color + (180,))
        elif "铠甲" in desc or "厚甲" in desc:
            # 铠甲（更宽更方）
            points = [(180, 240), (420, 240), (450, 650), (150, 650)]
            draw.polygon(points, fill=color + (200,))
            # 肩甲
            draw.ellipse([150, 230, 250, 330], fill=color + (220,))
            draw.ellipse([350, 230, 450, 330], fill=color + (220,))
        elif "飘逸" in desc:
            # 凤袍飘逸（更宽的下摆）
            points = [(210, 240), (390, 240), (500, 750), (100, 750)]
            draw.polygon(points, fill=color + (160,))
        elif "褴褛" in desc or "粗布" in desc:
            # 粗布衣（不规则边缘）
            points = [(220, 240), (380, 240), (410, 580), (190, 580)]
            draw.polygon(points, fill=color + (170,))
            # 补丁效果
            draw.rectangle([250, 350, 300, 400], fill=color + (120,))
            draw.rectangle[320, 450, 360, 490] if False else draw.rectangle([320, 450, 360, 490], fill=color + (100,))
        else:
            # 默认官服
            points = [(210, 240), (390, 240), (420, 620), (180, 620)]
            draw.polygon(points, fill=color + (180,))

        # 手臂
        draw.rectangle([150, 280, 200, 550], fill=color + (150,))
        draw.rectangle([400, 280, 450, 550], fill=color + (150,))

        # 模糊处理 — 剪影感
        img = img.filter(ImageFilter.GaussianBlur(radius=2))

        # 添加角色名标注
        draw = ImageDraw.Draw(img, "RGBA")
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)
        except:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), char_name, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((600 - tw) // 2, 820), char_name, fill=(245, 240, 232, 180), font=font)

        path = os.path.join(char_dir, f"{name}.png")
        img.save(path, "PNG")
        print(f"  [CHAR] {name}.png")

def generate_ui():
    """生成UI元素"""
    ui_dir = os.path.join(BASE, "game", "images", "ui")
    os.makedirs(ui_dir, exist_ok=True)

    # 标题背景
    img = create_gradient(1920, 1080, COLORS["ink_black_deep"], COLORS["ink_black"])
    draw = ImageDraw.Draw(img, "RGBA")

    # 水墨纹理效果
    for _ in range(30):
        import random
        x = random.randint(0, 1920)
        y = random.randint(0, 1080)
        r = random.randint(20, 80)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(44, 44, 44, random.randint(10, 30)))

    img = img.filter(ImageFilter.GaussianBlur(radius=5))

    # 添加装饰边框
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rectangle([50, 50, 1870, 1030], outline=COLORS["cinnabar"] + (100,), width=2)
    draw.rectangle([60, 60, 1860, 1020], outline=COLORS["ochre"] + (60,), width=1)

    path = os.path.join(ui_dir, "title_bg.png")
    img.save(path, "PNG")
    print(f"  [UI] title_bg.png")

def generate_audio_placeholders():
    """生成音频占位文件"""
    audio_dirs = [
        os.path.join(BASE, "game", "audio", "bgm"),
        os.path.join(BASE, "game", "audio", "sfx"),
    ]

    bgm_files = ["bgm_market", "bgm_palace", "bgm_village", "bgm_yamen"]
    sfx_files = ["sfx_ink", "sfx_scroll", "sfx_seal", "sfx_brush"]

    for d in audio_dirs:
        os.makedirs(d, exist_ok=True)

    # 生成空占位文件
    import struct
    for f in bgm_files:
        path = os.path.join(audio_dirs[0], f"{f}.mp3")
        with open(path, "wb") as fp:
            fp.write(b"")  # 空占位
        print(f"  [BGM] {f}.mp3 (placeholder)")

    for f in sfx_files:
        path = os.path.join(audio_dirs[1], f"{f}.ogg")
        with open(path, "wb") as fp:
            fp.write(b"")
        print(f"  [SFX] {f}.ogg (placeholder)")

if __name__ == "__main__":
    print("=== 风暴中的大顺朝 素材生成 ===\n")

    print("[1/4] 生成场景背景...")
    generate_backgrounds()

    print("\n[2/4] 生成角色剪影...")
    generate_characters()

    print("\n[3/4] 生成UI元素...")
    generate_ui()

    print("\n[4/4] 生成音频占位...")
    generate_audio_placeholders()

    print("\n=== 素材生成完成 ===")
    print(f"背景图: 6张 | 角色立绘: 8张 | UI: 1张 | 音频占位: 8个")
