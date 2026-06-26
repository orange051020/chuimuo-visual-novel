#!/usr/bin/env python3
"""
generate_portraits.py — 风暴中的大顺朝 全套水墨剪影立绘生成
风格：纯2D水墨剪影，无五官，低饱和，自然晕染，做旧褪色
输出：WebP(主) + PNG(备)，带完整透明通道
"""
import os
import random
import math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps

random.seed(42)

OUTPUT_DIR = "game/images/character"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# 色彩体系 — 每个角色专属主色 + 辅色
# ============================================================
PALETTES = {
    'lidongsheng':  {'primary': (139, 58, 58),  'secondary': (44, 44, 44),  'glow': (120, 50, 50)},
    'liusilian':    {'primary': (91, 122, 140), 'secondary': (58, 80, 96),  'glow': (75, 100, 120)},
    'majing':       {'primary': (26, 26, 26),   'secondary': (139, 107, 74),'glow': (50, 45, 35)},
    'guziming':     {'primary': (107, 122, 138),'secondary': (80, 95, 110), 'glow': (90, 105, 120)},
    'xushuniang':   {'primary': (160, 82, 79),  'secondary': (245, 240, 232),'glow': (140, 70, 67)},
    'lichengying':  {'primary': (122, 107, 90), 'secondary': (90, 80, 65),  'glow': (105, 92, 78)},
    'hantieshan':   {'primary': (107, 75, 58),  'secondary': (80, 55, 40),  'glow': (90, 65, 48)},
    'zhaotieshuan': {'primary': (139, 107, 74), 'secondary': (154, 139, 106),'glow': (120, 92, 64)},
    'shuoshuren':   {'primary': (139, 107, 74), 'secondary': (100, 80, 55), 'glow': (120, 92, 64)},
}

# ============================================================
# 工具函数
# ============================================================
def lerp(a, b, t):
    return a + (b - a) * t

def lerp_color(c1, c2, t):
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))

def jitter(val, amount):
    return val + random.randint(-amount, amount)

# ============================================================
# 水墨晕染效果引擎
# ============================================================
def create_noise_layer(width, height, intensity=20, blur_radius=3):
    """生成噪点纹理层，用于模拟宣纸质感"""
    small_w = max(1, width // 4)
    small_h = max(1, height // 4)
    small = Image.new('L', (small_w, small_h))
    pixels = small.load()
    for y in range(small_h):
        for x in range(small_w):
            pixels[x, y] = random.randint(0, 255)
    noise = small.resize((width, height), Image.BILINEAR)
    noise = noise.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    # 归一化到 intensity 范围
    noise = ImageOps.autocontrast(noise)
    return noise

def apply_ink_wash(mask, color, width, height,
                   edge_blur=5, noise_intensity=15,
                   splatter_count=30, splatter_max_r=8,
                   gradient_top=255, gradient_bottom=200,
                   desaturate=0.75, warmth=0.08):
    """
    将灰度遮罩转化为水墨剪影：
    - 柔化边缘（水墨晕染）
    - 添加噪点纹理（宣纸质感）
    - 添加墨点飞溅（自然笔触）
    - 垂直渐变（上淡下浓）
    - 做旧褪色
    """
    # 1. 边缘柔化 — 多层模糊叠加
    alpha = mask.filter(ImageFilter.GaussianBlur(radius=edge_blur))

    # 2. 噪点纹理 — 模拟宣纸吸收不均匀
    noise = create_noise_layer(width, height, intensity=noise_intensity, blur_radius=2)
    alpha_pixels = alpha.load()
    noise_pixels = noise.load()
    for y in range(0, height, 2):
        for x in range(0, width, 2):
            orig = alpha_pixels[x, y]
            if orig > 20:
                n = noise_pixels[x, y]
                adj = int((n - 128) * noise_intensity / 128)
                alpha_pixels[x, y] = max(0, min(255, orig + adj))

    # 3. 墨点飞溅 — 边缘附近随机墨点
    draw = ImageDraw.Draw(alpha)
    edge_points = []
    ap = alpha.load()
    step = 4
    for y in range(0, height, step):
        for x in range(0, width, step):
            v = ap[x, y]
            if v > 80:
                is_edge = False
                for dx, dy in [(-step, 0), (step, 0), (0, -step), (0, step)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if ap[nx, ny] < 40:
                            is_edge = True
                            break
                if is_edge:
                    edge_points.append((x, y))
    for _ in range(min(splatter_count, len(edge_points))):
        if edge_points:
            ex, ey = random.choice(edge_points)
            sx = ex + random.randint(-20, 20)
            sy = ey + random.randint(-20, 20)
            sr = random.randint(1, splatter_max_r)
            sa = random.randint(60, 180)
            draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=sa)

    # 4. 垂直渐变 — 上淡下浓（墨色下沉感）
    for y in range(height):
        t = y / max(1, height - 1)
        g = int(lerp(gradient_top, gradient_bottom, t))
        for x in range(0, width, 3):
            v = alpha_pixels[x, y]
            if v > 0:
                alpha_pixels[x, y] = min(v, int(v * g / 255))

    # 5. 填充角色主色
    color_img = Image.new('RGBA', (width, height), (*color, 255))

    # 6. 组合
    result = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    result.paste(color_img, (0, 0))
    result.putalpha(alpha)

    # 7. 做旧 — 降低饱和度
    enhancer = ImageEnhance.Color(result)
    result = enhancer.enhance(desaturate)

    # 8. 暖色调偏移 — 古卷质感
    if warmth > 0:
        r, g, b, a = result.split()
        r = r.point(lambda v: min(255, int(v + warmth * 20)))
        b = b.point(lambda v: max(0, int(v - warmth * 10)))
        result = Image.merge('RGBA', (r, g, b, a))

    return result

def make_ghost(img, opacity=0.4):
    """将立绘转为半透明幻觉效果"""
    r, g, b, a = img.split()
    a = a.point(lambda v: int(v * opacity))
    # 添加柔光模糊
    a = a.filter(ImageFilter.GaussianBlur(radius=8))
    return Image.merge('RGBA', (r, g, b, a))

def make_flashback(img):
    """回忆闪回效果 — 柔光模糊 + 暖色调"""
    r, g, b, a = img.split()
    a = a.filter(ImageFilter.GaussianBlur(radius=4))
    a = a.point(lambda v: int(v * 0.85))
    r = r.point(lambda v: min(255, int(v * 1.1 + 15)))
    g = g.point(lambda v: min(255, int(v * 1.0 + 5)))
    b = b.point(lambda v: max(0, int(v * 0.85 - 10)))
    return Image.merge('RGBA', (r, g, b, a))

# ============================================================
# 灰度遮罩绘制 — 在 mask 上用白色绘制剪影形状
# ============================================================
def new_mask(width, height):
    return Image.new('L', (width, height), 0)

def draw_half_body(draw, cx, top_y, body_type='medium',
                   head_tilt=0, lean=0, arm_left='down', arm_right='down',
                   robe='formal', hunch=0):
    """
    在灰度遮罩上绘制半身剪影
    body_type: thin / medium / stocky / old / graceful
    """
    # 身体参数 — 按体型调整
    body_params = {
        'thin':      {'head_w': 70, 'head_h': 95, 'shoulder_w': 200, 'torso_w': 170, 'torso_h': 320},
        'medium':    {'head_w': 80, 'head_h': 100, 'shoulder_w': 240, 'torso_w': 200, 'torso_h': 340},
        'stocky':    {'head_w': 90, 'head_h': 105, 'shoulder_w': 290, 'torso_w': 250, 'torso_h': 340},
        'old':       {'head_w': 72, 'head_h': 92, 'shoulder_w': 190, 'torso_w': 160, 'torso_h': 310},
        'graceful':  {'head_w': 75, 'head_h': 98, 'shoulder_w': 210, 'torso_w': 180, 'torso_h': 340},
    }
    p = body_params.get(body_type, body_params['medium'])

    sw = p['shoulder_w']
    tw = p['torso_w']
    hh = p['head_h']
    hw = p['head_w']
    th = p['torso_h']

    # 应用倾斜
    lean_offset = int(lean * 2)
    cx_adj = cx + lean_offset
    top_y_adj = top_y + hunch

    # 头部
    head_cx = cx_adj + head_tilt
    head_cy = top_y_adj + hh // 2
    draw.ellipse([head_cx - hw//2, top_y_adj, head_cx + hw//2, top_y_adj + hh], fill=255)

    # 颈部
    neck_w = hw // 2
    neck_top = top_y_adj + hh - 5
    neck_bot = neck_top + 25
    draw.rectangle([head_cx - neck_w//2, neck_top, head_cx + neck_w//2, neck_bot], fill=255)

    # 肩部
    shoulder_y = neck_bot
    shoulder_h = 40
    draw.ellipse([cx_adj - sw//2, shoulder_y, cx_adj + sw//2, shoulder_y + shoulder_h], fill=255)

    # 躯干（梯形）
    torso_top = shoulder_y + 20
    torso_bot = torso_top + th
    torso_pts = [
        (cx_adj - sw//2 + 10, torso_top),
        (cx_adj + sw//2 - 10, torso_top),
        (cx_adj + tw//2, torso_bot),
        (cx_adj - tw//2, torso_bot),
    ]
    draw.polygon(torso_pts, fill=255)

    # 衣袍扩展（底部更宽）
    if robe == 'formal':
        robe_w = int(sw * 1.3)
        robe_pts = [
            (cx_adj - tw//2, torso_bot - 20),
            (cx_adj + tw//2, torso_bot - 20),
            (cx_adj + robe_w//2, torso_bot + 80),
            (cx_adj - robe_w//2, torso_bot + 80),
        ]
        draw.polygon(robe_pts, fill=255)
    elif robe == 'simple':
        robe_w = int(sw * 1.1)
        robe_pts = [
            (cx_adj - tw//2, torso_bot - 10),
            (cx_adj + tw//2, torso_bot - 10),
            (cx_adj + robe_w//2, torso_bot + 60),
            (cx_adj - robe_w//2, torso_bot + 60),
        ]
        draw.polygon(robe_pts, fill=255)

    # 左臂
    _draw_arm(draw, cx_adj - sw//2 + 5, shoulder_y + 10, arm_left, 'left', body_type)
    # 右臂
    _draw_arm(draw, cx_adj + sw//2 - 5, shoulder_y + 10, arm_right, 'right', body_type)

    return torso_bot  # 返回躯干底部 y 坐标

def _draw_arm(draw, sx, sy, pose, side, body_type):
    """绘制手臂"""
    arm_len = 200 if body_type in ('stocky',) else 180
    arm_w = 35 if body_type == 'stocky' else 28

    if pose == 'down':
        ex = sx + (15 if side == 'right' else -15)
        ey = sy + arm_len
        draw.polygon([
            (sx - arm_w//2, sy),
            (sx + arm_w//2, sy),
            (ex + arm_w//2, ey),
            (ex - arm_w//2, ey),
        ], fill=255)
        # 手
        draw.ellipse([ex - 18, ey - 5, ex + 18, ey + 25], fill=255)

    elif pose == 'crossed':
        # 双臂交叉于胸前
        cx_offset = 40 if side == 'right' else -40
        ex = sx + cx_offset
        ey = sy + 80
        draw.polygon([
            (sx - arm_w//2, sy),
            (sx + arm_w//2, sy),
            (ex + arm_w//2, ey),
            (ex - arm_w//2, ey),
        ], fill=255)
        draw.ellipse([ex - 20, ey - 10, ex + 20, ey + 20], fill=255)

    elif pose == 'raised':
        ex = sx + (40 if side == 'right' else -40)
        ey = sy - 30
        draw.polygon([
            (sx - arm_w//2, sy),
            (sx + arm_w//2, sy),
            (ex + arm_w//2, ey),
            (ex - arm_w//2, ey),
        ], fill=255)
        draw.ellipse([ex - 20, ey - 20, ex + 20, ey + 10], fill=255)

    elif pose == 'extended':
        ex = sx + (80 if side == 'right' else -80)
        ey = sy + 60
        draw.polygon([
            (sx - arm_w//2, sy),
            (sx + arm_w//2, sy),
            (ex + arm_w//2, ey),
            (ex - arm_w//2, ey),
        ], fill=255)
        draw.ellipse([ex - 20, ey - 10, ex + 20, ey + 20], fill=255)

    elif pose == 'on_desk':
        ex = sx + (30 if side == 'right' else -30)
        ey = sy + 100
        draw.polygon([
            (sx - arm_w//2, sy),
            (sx + arm_w//2, sy),
            (ex + arm_w//2, ey),
            (ex - arm_w//2, ey),
        ], fill=255)
        draw.ellipse([ex - 18, ey - 5, ex + 18, ey + 20], fill=255)

    elif pose == 'forward':
        ex = sx + (50 if side == 'right' else -50)
        ey = sy + 120
        draw.polygon([
            (sx - arm_w//2, sy),
            (sx + arm_w//2, sy),
            (ex + arm_w//2, ey),
            (ex - arm_w//2, ey),
        ], fill=255)
        draw.ellipse([ex - 20, ey - 10, ex + 20, ey + 20], fill=255)

    elif pose == 'hidden':
        pass  # 手臂隐藏在袖中

def draw_full_body(draw, cx, top_y, body_type='medium',
                   head_tilt=0, lean=0, stance='standing',
                   robe='formal', arm_left='down', arm_right='down'):
    """在灰度遮罩上绘制全身剪影"""
    body_params = {
        'thin':      {'head_w': 55, 'head_h': 75, 'shoulder_w': 170, 'torso_w': 140, 'leg_w': 80, 'total_h': 850},
        'medium':    {'head_w': 65, 'head_h': 82, 'shoulder_w': 200, 'torso_w': 170, 'leg_w': 95, 'total_h': 900},
        'stocky':    {'head_w': 75, 'head_h': 88, 'shoulder_w': 240, 'torso_w': 210, 'leg_w': 110, 'total_h': 880},
        'old':       {'head_w': 58, 'head_h': 75, 'shoulder_w': 160, 'torso_w': 135, 'leg_w': 75, 'total_h': 820},
        'graceful':  {'head_w': 60, 'head_h': 80, 'shoulder_w': 180, 'torso_w': 155, 'leg_w': 85, 'total_h': 880},
    }
    p = body_params.get(body_type, body_params['medium'])
    sw, tw, hw, hh = p['shoulder_w'], p['torso_w'], p['head_w'], p['head_h']
    lw = p['leg_w']

    cx_adj = cx + int(lean * 2)

    # 头部
    head_cx = cx_adj + head_tilt
    draw.ellipse([head_cx - hw//2, top_y, head_cx + hw//2, top_y + hh], fill=255)

    # 颈部
    neck_top = top_y + hh - 3
    neck_bot = neck_top + 20
    draw.rectangle([head_cx - 14, neck_top, head_cx + 14, neck_bot], fill=255)

    # 肩部
    shoulder_y = neck_bot
    draw.ellipse([cx_adj - sw//2, shoulder_y, cx_adj + sw//2, shoulder_y + 35], fill=255)

    # 躯干
    torso_top = shoulder_y + 15
    torso_bot = torso_top + 280
    draw.polygon([
        (cx_adj - sw//2 + 8, torso_top),
        (cx_adj + sw//2 - 8, torso_top),
        (cx_adj + tw//2, torso_bot),
        (cx_adj - tw//2, torso_bot),
    ], fill=255)

    if stance == 'standing':
        # 双腿
        leg_top = torso_bot - 20
        leg_bot = top_y + p['total_h']
        # 左腿
        draw.polygon([
            (cx_adj - tw//2 + 10, leg_top),
            (cx_adj - 5, leg_top),
            (cx_adj - 5, leg_bot),
            (cx_adj - lw//2 - 10, leg_bot),
        ], fill=255)
        # 右腿
        draw.polygon([
            (cx_adj + 5, leg_top),
            (cx_adj + tw//2 - 10, leg_top),
            (cx_adj + lw//2 + 10, leg_bot),
            (cx_adj + 5, leg_bot),
        ], fill=255)

        # 衣袍下摆
        if robe in ('formal', 'military'):
            hem_w = int(sw * 1.4)
            draw.polygon([
                (cx_adj - tw//2, torso_bot - 30),
                (cx_adj + tw//2, torso_bot - 30),
                (cx_adj + hem_w//2, leg_bot - 10),
                (cx_adj - hem_w//2, leg_bot - 10),
            ], fill=255)

    elif stance == 'leaning':
        # 斜靠姿势
        leg_top = torso_bot - 20
        leg_bot = top_y + p['total_h']
        # 单腿交叉
        draw.polygon([
            (cx_adj - tw//2 + 10, leg_top),
            (cx_adj + 10, leg_top),
            (cx_adj + 30, leg_bot),
            (cx_adj - lw//2 - 5, leg_bot),
        ], fill=255)
        draw.polygon([
            (cx_adj + 10, leg_top),
            (cx_adj + tw//2 - 10, leg_top),
            (cx_adj + lw//2 + 20, leg_bot),
            (cx_adj + 30, leg_bot),
        ], fill=255)

    # 手臂
    _draw_arm(draw, cx_adj - sw//2 + 3, shoulder_y + 8, arm_left, 'left', body_type)
    _draw_arm(draw, cx_adj + sw//2 - 3, shoulder_y + 8, arm_right, 'right', body_type)

    return top_y + p['total_h']

def draw_prop_scroll(draw, cx, cy, w=80, h=120, angle=0):
    """绘制文书/卷轴道具"""
    pts = []
    for i in range(4):
        a = math.radians(angle + i * 90)
        if i in (0, 2):
            px = cx + (w//2) * math.cos(a)
            py = cy + (h//2) * math.sin(a)
        else:
            px = cx + (w//2) * math.cos(a)
            py = cy + (h//2) * math.sin(a)
        pts.append((px, py))
    draw.polygon([
        (cx - w//2, cy - h//2),
        (cx + w//2, cy - h//2),
        (cx + w//2, cy + h//2),
        (cx - w//2, cy + h//2),
    ], fill=255)
    # 卷轴两端
    draw.ellipse([cx - w//2 - 5, cy - h//2 - 8, cx + w//2 + 5, cy - h//2 + 8], fill=255)
    draw.ellipse([cx - w//2 - 5, cy + h//2 - 8, cx + w//2 + 5, cy + h//2 + 8], fill=255)

def draw_prop_sword(draw, sx, sy, length=300, angle=0, at_waist=False):
    """绘制长刀道具"""
    if at_waist:
        # 腰间佩刀 — 水平
        draw.rectangle([sx, sy - 4, sx + length, sy + 4], fill=255)
        # 刀柄
        draw.rectangle([sx - 30, sy - 8, sx, sy + 8], fill=255)
    else:
        # 竖直长刀
        rad = math.radians(angle)
        ex = sx + length * math.sin(rad)
        ey = sy + length * math.cos(rad)
        draw.line([(sx, sy), (ex, ey)], fill=255, width=12)
        # 刀柄
        draw.rectangle([sx - 10, sy, sx + 10, sy + 40], fill=255)

def draw_prop_book(draw, cx, cy, w=100, h=140):
    """绘制书册/律法册道具"""
    draw.rectangle([cx - w//2, cy - h//2, cx + w//2, cy + h//2], fill=255)
    # 书页线
    draw.line([(cx, cy - h//2), (cx, cy + h//2)], fill=200, width=2)

def draw_prop_abacus(draw, cx, cy, w=120, h=80):
    """绘制算盘道具"""
    draw.rectangle([cx - w//2, cy - h//2, cx + w//2, cy + h//2], fill=255)
    # 算盘珠 — 水平线
    for i in range(4):
        y = cy - h//2 + 15 + i * 18
        draw.line([(cx - w//2 + 5, y), (cx + w//2 - 5, y)], fill=180, width=2)

def draw_prop_bowl(draw, cx, cy, w=80, h=50):
    """绘制碗道具"""
    draw.pieslice([cx - w//2, cy - h, cx + w//2, cy + h], 0, 180, fill=255)

def draw_prop_cup(draw, cx, cy, w=40, h=50):
    """绘制酒杯道具"""
    draw.polygon([
        (cx - w//2, cy - h//2),
        (cx + w//2, cy - h//2),
        (cx + w//3, cy + h//2),
        (cx - w//3, cy + h//2),
    ], fill=255)

def draw_prop_shuttle(draw, cx, cy, w=50, h=100):
    """绘制织布梭道具"""
    draw.polygon([
        (cx, cy - h//2),
        (cx + w//2, cy),
        (cx, cy + h//2),
        (cx - w//2, cy),
    ], fill=255)

def draw_prop_woodblock(draw, cx, cy, w=50, h=30):
    """绘制醒木道具"""
    draw.rectangle([cx - w//2, cy - h//2, cx + w//2, cy + h//2], fill=255)

def draw_table(draw, cx, cy, w=300, h=40):
    """绘制桌面"""
    draw.rectangle([cx - w//2, cy, cx + w//2, cy + h], fill=255)
    # 桌腿
    draw.rectangle([cx - w//2, cy, cx - w//2 + 15, cy + 120], fill=255)
    draw.rectangle([cx + w//2 - 15, cy, cx + w//2, cy + 120], fill=255)

# ============================================================
# 各角色立绘生成函数
# 每个函数返回 (mask, width, height, color_key)
# ============================================================

# ---- 李东升 (lidongsheng) ----
def gen_lidongsheng_normal():
    """半身常态 — 侧卧床榻，手持文书，疲惫松弛"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    # 上身微抬，靠在枕上
    draw_half_body(draw, 300, 100, body_type='old', lean=5, hunch=15,
                   arm_left='on_desk', arm_right='extended', robe='formal')
    # 手中文书
    draw_prop_scroll(draw, 380, 350, 70, 100)
    return mask, w, h, 'lidongsheng'

def gen_lidongsheng_anger():
    """半身情绪1 — 前倾激动，手撑榻边"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_half_body(draw, 300, 80, body_type='old', lean=15,
                   arm_left='forward', arm_right='on_desk', robe='formal')
    return mask, w, h, 'lidongsheng'

def gen_lidongsheng_despair():
    """半身情绪2 — 垂首低头，肩背佝偻"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_half_body(draw, 300, 120, body_type='old', lean=-5, hunch=40,
                   head_tilt=-5, arm_left='down', arm_right='down', robe='formal')
    return mask, w, h, 'lidongsheng'

def gen_lidongsheng_young():
    """全身回忆 — 年轻军装站姿，腰间佩刀"""
    w, h = 600, 1000
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_full_body(draw, 300, 50, body_type='medium', robe='military',
                   arm_left='down', arm_right='down', stance='standing')
    # 腰间佩刀
    draw_prop_sword(draw, 380, 450, length=180, at_waist=True)
    return mask, w, h, 'lidongsheng'

def gen_lidongsheng_closeup():
    """局部特写 — 苍老带伤疤的手，捏着律法书页"""
    w, h = 1920, 1080
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    # 大手
    draw.ellipse([600, 300, 1100, 700], fill=255)  # 手掌
    draw.ellipse([1050, 350, 1300, 600], fill=255)  # 手指延伸
    # 律法书页
    draw.rectangle([800, 500, 1500, 900], fill=255)
    # 烛火光晕
    draw.ellipse([1400, 100, 1700, 400], fill=180)
    return mask, w, h, 'lidongsheng'

# ---- 刘思廉 (liusilian) ----
def gen_liusilian_normal():
    """半身常态 — 端坐案前，手搭账册"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_half_body(draw, 300, 80, body_type='medium', lean=0,
                   arm_left='on_desk', arm_right='on_desk', robe='formal')
    # 账册
    draw_prop_book(draw, 300, 500, 120, 80)
    return mask, w, h, 'liusilian'

def gen_liusilian_argue():
    """半身情绪1 — 微抬，笔悬半空"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_half_body(draw, 300, 60, body_type='medium', lean=8,
                   arm_left='on_desk', arm_right='raised', robe='formal')
    # 悬停的笔
    draw.rectangle([420, 120, 428, 200], fill=255)  # 毛笔杆
    draw.ellipse([415, 195, 435, 220], fill=255)  # 笔头
    return mask, w, h, 'liusilian'

def gen_liusilian_decide():
    """半身情绪2 — 背对镜头，面向窗外"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    # 背影 — 头部较小，肩部突出
    draw.ellipse([260, 80, 340, 170], fill=255)  # 头（背面）
    draw.rectangle([280, 160, 320, 190], fill=255)  # 颈
    draw.ellipse([180, 180, 420, 230], fill=255)  # 肩
    draw.polygon([(190, 210), (410, 210), (380, 550), (220, 550)], fill=255)  # 背
    # 手负身后
    draw.ellipse([250, 400, 310, 450], fill=255)  # 负手
    return mask, w, h, 'liusilian'

def gen_liusilian_closeup():
    """局部特写 — 手拨算盘珠，旁有通商文书"""
    w, h = 1920, 1080
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    # 手
    draw.ellipse([500, 400, 900, 750], fill=255)
    draw.ellipse([800, 450, 1050, 700], fill=255)
    # 算盘
    draw_prop_abacus(draw, 1200, 600, 300, 200)
    # 文书
    draw.rectangle([1000, 300, 1600, 550], fill=200)
    return mask, w, h, 'liusilian'

# ---- 马靖 (majing) ----
def gen_majing_normal():
    """半身常态 — 抱臂站立，腰间长刀"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_half_body(draw, 300, 60, body_type='stocky', lean=3,
                   arm_left='crossed', arm_right='crossed', robe='military')
    # 腰间刀柄
    draw_prop_sword(draw, 400, 500, length=150, at_waist=True)
    return mask, w, h, 'majing'

def gen_majing_press():
    """半身情绪 — 单手按刀柄，前倾"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_half_body(draw, 300, 50, body_type='stocky', lean=10,
                   arm_left='crossed', arm_right='forward', robe='military')
    # 刀柄
    draw.rectangle([380, 400, 420, 500], fill=255)
    draw.ellipse([370, 380, 430, 440], fill=255)
    return mask, w, h, 'majing'

def gen_majing_drink():
    """全身场景 — 举杯侧身站立"""
    w, h = 600, 1000
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_full_body(draw, 300, 30, body_type='stocky', lean=8,
                   stance='leaning', robe='military',
                   arm_left='down', arm_right='raised')
    # 酒杯
    draw_prop_cup(draw, 400, 150, 40, 50)
    return mask, w, h, 'majing'

def gen_majing_closeup():
    """局部特写 — 粗糙带老茧的手握青铜酒杯"""
    w, h = 1920, 1080
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    # 手
    draw.ellipse([550, 350, 1000, 700], fill=255)
    draw.ellipse([950, 400, 1200, 650], fill=255)
    # 酒杯
    draw.polygon([
        (1100, 400), (1300, 400), (1270, 600), (1130, 600)
    ], fill=255)
    draw.ellipse([1100, 380, 1300, 430], fill=255)
    return mask, w, h, 'majing'

# ---- 顾子明 (guziming) ----
def gen_guziming_normal():
    """半身常态 — 垂手躬身，抱文书"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_half_body(draw, 300, 90, body_type='thin', lean=-3, hunch=10,
                   arm_left='down', arm_right='down', robe='formal')
    # 怀中文书
    draw_prop_scroll(draw, 300, 480, 70, 120)
    return mask, w, h, 'guziming'

def gen_guziming_breakdown():
    """半身情绪1 — 伏案低头，双肩颤抖"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    # 伏案姿态 — 大幅前倾
    draw_half_body(draw, 300, 150, body_type='thin', lean=25, hunch=30,
                   arm_left='forward', arm_right='forward', robe='formal')
    # 桌面
    draw.rectangle([100, 550, 500, 580], fill=200)
    return mask, w, h, 'guziming'

def gen_guziming_kneel():
    """半身情绪2 — 跪地叩首"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    # 跪姿 — 头低垂，身体前倾
    draw.ellipse([260, 300, 340, 380], fill=255)  # 低垂的头
    draw.rectangle([280, 370, 320, 400], fill=255)  # 颈
    # 弯曲的背
    draw.polygon([
        (220, 390), (380, 390), (400, 600), (200, 600)
    ], fill=255)
    # 手撑地
    draw.ellipse([200, 580, 270, 640], fill=255)
    draw.ellipse([330, 580, 400, 640], fill=255)
    # 袍服下摆
    draw.polygon([(180, 600), (420, 600), (440, 800), (160, 800)], fill=255)
    return mask, w, h, 'guziming'

def gen_guziming_closeup():
    """局部特写 — 颤抖指尖捏密奏"""
    w, h = 1920, 1080
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    # 手指
    draw.ellipse([600, 400, 800, 550], fill=255)
    draw.ellipse([750, 380, 950, 530], fill=255)
    draw.ellipse([900, 400, 1100, 560], fill=255)
    # 密奏
    draw.rectangle([800, 500, 1400, 850], fill=255)
    # 褶皱效果
    draw.line([(850, 600), (1350, 620)], fill=180, width=3)
    draw.line([(850, 700), (1350, 680)], fill=180, width=3)
    return mask, w, h, 'guziming'

# ---- 徐淑娘 (xushuniang) ----
def gen_xushuniang_normal():
    """半身常态 — 端坐捧粥碗"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_half_body(draw, 300, 80, body_type='graceful', lean=0,
                   arm_left='on_desk', arm_right='on_desk', robe='formal')
    # 粥碗
    draw_prop_bowl(draw, 300, 480, 80, 50)
    return mask, w, h, 'xushuniang'

def gen_xushuniang_worry():
    """半身情绪 — 侧身持梭，微绷紧"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_half_body(draw, 280, 70, body_type='graceful', lean=-5,
                   arm_left='down', arm_right='raised', robe='formal')
    # 织布梭
    draw_prop_shuttle(draw, 370, 200, 40, 80)
    return mask, w, h, 'xushuniang'

def gen_xushuniang_ghost():
    """全身幻觉 — 半透明全身剪影"""
    w, h = 600, 1000
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_full_body(draw, 300, 40, body_type='graceful', robe='formal',
                   stance='standing', arm_left='down', arm_right='down')
    return mask, w, h, 'xushuniang'

def gen_xushuniang_closeup():
    """局部特写 — 纤细手抚律法书页"""
    w, h = 1920, 1080
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    # 纤细手
    draw.ellipse([650, 380, 950, 600], fill=255)
    draw.ellipse([900, 350, 1150, 570], fill=255)
    # 书页
    draw.rectangle([750, 500, 1500, 900], fill=255)
    return mask, w, h, 'xushuniang'

# ---- 李承英 (lichengying) ----
def gen_lichengying_young():
    """半身年轻 — 挺拔披风，意气风发"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_half_body(draw, 300, 60, body_type='thin', lean=-3,
                   arm_left='down', arm_right='down', robe='formal')
    # 披风 — 肩部更宽
    draw.polygon([
        (150, 200), (180, 200), (200, 600), (120, 600)
    ], fill=255)
    draw.polygon([
        (420, 200), (450, 200), (480, 600), (400, 600)
    ], fill=255)
    return mask, w, h, 'lichengying'

def gen_lichengying_later():
    """半身后期 — 肩背佝偻，沉重晦暗"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_half_body(draw, 300, 110, body_type='thin', lean=5, hunch=25,
                   arm_left='down', arm_right='down', robe='formal')
    # 破旧披风
    draw.polygon([
        (160, 230), (185, 230), (195, 600), (130, 600)
    ], fill=200)
    draw.polygon([
        (415, 230), (440, 230), (470, 600), (405, 600)
    ], fill=200)
    return mask, w, h, 'lichengying'

def gen_lichengying_ghost():
    """全身幻觉 — 半透明低头站立"""
    w, h = 600, 1000
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_full_body(draw, 300, 40, body_type='thin', robe='formal',
                   stance='standing', arm_left='down', arm_right='down',
                   head_tilt=-3)
    return mask, w, h, 'lichengying'

# ---- 韩铁山 (hantieshan) ----
def gen_hantieshan_normal():
    """半身常态 — 扛刀歪斜站立"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_half_body(draw, 290, 50, body_type='stocky', lean=8,
                   arm_left='crossed', arm_right='raised', robe='military')
    # 扛在肩上的长刀
    draw.line([(200, 180), (450, 120)], fill=255, width=14)
    draw.rectangle([180, 170, 220, 210], fill=255)  # 刀柄
    return mask, w, h, 'hantieshan'

def gen_hantieshan_kill():
    """半身肃杀 — 按刀挺直，周身冷硬"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_half_body(draw, 300, 50, body_type='stocky', lean=0,
                   arm_left='down', arm_right='forward', robe='military')
    # 按刀
    draw.rectangle([370, 380, 410, 500], fill=255)
    draw.ellipse([360, 360, 420, 420], fill=255)
    draw.line([(390, 500), (390, 750)], fill=255, width=10)
    return mask, w, h, 'hantieshan'

def gen_hantieshan_ghost():
    """全身幻觉 — 半透明长刀拄地"""
    w, h = 600, 1000
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_full_body(draw, 300, 30, body_type='stocky', robe='military',
                   stance='standing', arm_left='down', arm_right='down')
    # 拄地长刀
    draw.line([(400, 100), (400, 950)], fill=255, width=12)
    draw.rectangle([385, 90, 415, 130], fill=255)
    return mask, w, h, 'hantieshan'

# ---- 赵铁栓 (zhaotieshuan) ----
def gen_zhaotieshuan_preach():
    """半身宣讲 — 站石墩上举律法册"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_half_body(draw, 300, 50, body_type='stocky', lean=-3,
                   arm_left='raised', arm_right='raised', robe='simple')
    # 举着的律法册
    draw_prop_book(draw, 300, 180, 100, 140)
    return mask, w, h, 'zhaotieshuan'

def gen_zhaotieshuan_despair():
    """半身绝望 — 跪地垂头攥残页"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    # 跪姿
    draw.ellipse([260, 320, 340, 400], fill=255)  # 低垂的头
    draw.rectangle([280, 390, 320, 420], fill=255)  # 颈
    draw.polygon([(230, 410), (370, 410), (390, 600), (210, 600)], fill=255)  # 背
    # 手攥东西
    draw.ellipse([250, 570, 320, 630], fill=255)
    draw.ellipse([280, 570, 350, 630], fill=255)
    # 袍服下摆
    draw.polygon([(190, 600), (410, 600), (430, 820), (170, 820)], fill=255)
    return mask, w, h, 'zhaotieshuan'

def gen_zhaotieshuan_fall():
    """全身倒下 — 侧卧散页"""
    w, h = 600, 1000
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    # 侧倒的全身
    draw.ellipse([100, 500, 200, 600], fill=255)  # 头
    draw.polygon([
        (180, 530), (500, 480), (520, 560), (180, 600)
    ], fill=255)  # 身体横躺
    # 腿
    draw.polygon([(450, 480), (550, 450), (560, 520), (480, 540)], fill=255)
    # 散落的律法残页
    for i in range(5):
        px = 150 + i * 80
        py = 650 + random.randint(-20, 20)
        draw.rectangle([px, py, px + 50, py + 30], fill=200)
    return mask, w, h, 'zhaotieshuan'

def gen_zhaotieshuan_closeup():
    """局部特写 — 沾泥手攥皱巴巴律法残页"""
    w, h = 1920, 1080
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    # 手
    draw.ellipse([550, 380, 1000, 680], fill=255)
    draw.ellipse([950, 400, 1200, 630], fill=255)
    # 皱巴巴的残页
    draw.polygon([
        (800, 500), (1400, 480), (1420, 700), (1380, 850),
        (820, 870), (790, 650)
    ], fill=255)
    # 褶皱线
    for i in range(5):
        y = 550 + i * 60
        draw.line([(820, y), (1380, y - 10)], fill=180, width=2)
    return mask, w, h, 'zhaotieshuan'

# ---- 说书人 (shuoshuren) ----
def gen_shuoshuren_normal():
    """半身常态 — 说书台后拍醒木"""
    w, h = 600, 900
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_half_body(draw, 300, 60, body_type='medium', lean=0,
                   arm_left='on_desk', arm_right='raised', robe='simple')
    # 说书台
    draw_table(draw, 300, 500, 350, 35)
    # 醒木
    draw_prop_woodblock(draw, 350, 490, 40, 25)
    return mask, w, h, 'shuoshuren'

def gen_shuoshuren_full():
    """全身场景 — 说书台上全身剪影，台下模糊茶客"""
    w, h = 600, 1000
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    draw_full_body(draw, 300, 30, body_type='medium', robe='simple',
                   stance='standing', arm_left='down', arm_right='raised')
    # 说书台
    draw_table(draw, 300, 650, 350, 35)
    # 台下模糊茶客剪影 — 半透明小圆
    for i in range(6):
        cx = 80 + i * 90
        cy = 880
        draw.ellipse([cx - 25, cy - 40, cx + 25, cy + 10], fill=100)
        draw.ellipse([cx - 20, cy - 60, cx + 20, cy - 20], fill=100)
    return mask, w, h, 'shuoshuren'

# ============================================================
# 群像立绘
# ============================================================
def gen_group_court_officials():
    """朝堂群臣 — 成片跪地/站立官员剪影"""
    w, h = 1920, 1080
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    # 多排官员剪影
    for row in range(4):
        row_y = 300 + row * 180
        count = 8 + row * 2
        spacing = 1600 // count
        for i in range(count):
            cx = 160 + i * spacing + random.randint(-15, 15)
            cy = row_y + random.randint(-10, 10)
            scale = 0.6 + row * 0.1
            # 简化人形
            draw.ellipse([cx - 30*scale, cy, cx + 30*scale, cy + 80*scale], fill=255)  # 头
            draw.polygon([
                (cx - 60*scale, cy + 70*scale),
                (cx + 60*scale, cy + 70*scale),
                (cx + 80*scale, cy + 250*scale),
                (cx - 80*scale, cy + 250*scale),
            ], fill=255)  # 袍
    return mask, w, h, 'guziming'  # 用灰色调

def gen_group_villagers():
    """村民群像 — 围坐半圆形"""
    w, h = 1920, 1080
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    # 半圆形排列
    center_x, center_y = 960, 900
    radius = 700
    for i in range(12):
        angle = math.pi * (0.15 + i * 0.06)
        cx = int(center_x - radius * math.cos(angle))
        cy = int(center_y - radius * math.sin(angle) * 0.5)
        scale = 0.5 + random.uniform(-0.1, 0.15)
        # 坐姿人形
        draw.ellipse([cx - 25*scale, cy, cx + 25*scale, cy + 55*scale], fill=255)  # 头
        draw.polygon([
            (cx - 50*scale, cy + 50*scale),
            (cx + 50*scale, cy + 50*scale),
            (cx + 60*scale, cy + 180*scale),
            (cx - 60*scale, cy + 180*scale),
        ], fill=255)  # 身体
    return mask, w, h, 'zhaotieshuan'

def gen_group_four_conspiracy():
    """四人集团同框 — 徐淑娘/李承英/韩铁山/顾子明全身剪影并排"""
    w, h = 1920, 1080
    mask = new_mask(w, h)
    draw = ImageDraw.Draw(mask)
    positions = [300, 750, 1170, 1620]
    body_types = ['graceful', 'thin', 'stocky', 'thin']
    for i, (px, bt) in enumerate(zip(positions, body_types)):
        draw_full_body(draw, px, 100, body_type=bt, robe='formal',
                       stance='standing', arm_left='down', arm_right='down',
                       lean=random.randint(-5, 5))
    return mask, w, h, 'guziming'

# ============================================================
# 主生成流程
# ============================================================
GENERATORS = [
    # (filename, generator_func, is_ghost, is_flashback)
    # 李东升
    ('char_lidongsheng_normal',    gen_lidongsheng_normal,    False, False),
    ('char_lidongsheng_anger',     gen_lidongsheng_anger,     False, False),
    ('char_lidongsheng_despair',   gen_lidongsheng_despair,   False, False),
    ('char_lidongsheng_young',     gen_lidongsheng_young,     False, True),  # 回忆
    ('char_lidongsheng_closeup_1', gen_lidongsheng_closeup,   False, False),
    # 刘思廉
    ('char_liusilian_normal',      gen_liusilian_normal,      False, False),
    ('char_liusilian_argue',       gen_liusilian_argue,       False, False),
    ('char_liusilian_decide',      gen_liusilian_decide,      False, False),
    ('char_liusilian_closeup_1',   gen_liusilian_closeup,     False, False),
    # 马靖
    ('char_majing_normal',         gen_majing_normal,         False, False),
    ('char_majing_press',          gen_majing_press,          False, False),
    ('char_majing_drink',          gen_majing_drink,          False, False),
    ('char_majing_closeup_1',      gen_majing_closeup,        False, False),
    # 顾子明
    ('char_guziming_normal',       gen_guziming_normal,       False, False),
    ('char_guziming_breakdown',    gen_guziming_breakdown,    False, False),
    ('char_guziming_kneel',        gen_guziming_kneel,        False, False),
    ('char_guziming_closeup_1',    gen_guziming_closeup,      False, False),
    # 徐淑娘
    ('char_xushuniang_normal',     gen_xushuniang_normal,     False, False),
    ('char_xushuniang_worry',      gen_xushuniang_worry,      False, False),
    ('char_xushuniang_ghost',      gen_xushuniang_ghost,      True,  False),  # 幻觉
    ('char_xushuniang_closeup_1',  gen_xushuniang_closeup,    False, False),
    # 李承英
    ('char_lichengying_young',     gen_lichengying_young,     False, False),
    ('char_lichengying_later',     gen_lichengying_later,     False, False),
    ('char_lichengying_ghost',     gen_lichengying_ghost,     True,  False),  # 幻觉
    # 韩铁山
    ('char_hantieshan_normal',     gen_hantieshan_normal,     False, False),
    ('char_hantieshan_kill',       gen_hantieshan_kill,       False, False),
    ('char_hantieshan_ghost',      gen_hantieshan_ghost,      True,  False),  # 幻觉
    # 赵铁栓
    ('char_zhaotieshuan_preach',   gen_zhaotieshuan_preach,   False, False),
    ('char_zhaotieshuan_despair',  gen_zhaotieshuan_despair,  False, False),
    ('char_zhaotieshuan_fall',     gen_zhaotieshuan_fall,     False, False),
    ('char_zhaotieshuan_closeup_1',gen_zhaotieshuan_closeup,  False, False),
    # 说书人
    ('char_shuoshuren_normal',     gen_shuoshuren_normal,     False, False),
    ('char_shuoshuren_full',       gen_shuoshuren_full,       False, False),
    # 群像
    ('group_court_officials',      gen_group_court_officials, False, False),
    ('group_villagers',            gen_group_villagers,       False, False),
    ('group_four_conspiracy',      gen_group_four_conspiracy, True,  False),  # 幻觉半透明
]

def generate_all():
    print("=" * 60)
    print("风暴中的大顺朝 — 水墨剪影立绘生成")
    print("=" * 60)

    success = 0
    failed = 0

    for filename, gen_func, is_ghost, is_flashback in GENERATORS:
        try:
            mask, w, h, color_key = gen_func()
            color = PALETTES[color_key]['primary']

            # 应用水墨晕染
            img = apply_ink_wash(mask, color, w, h,
                                edge_blur=5,
                                noise_intensity=12,
                                splatter_count=25,
                                desaturate=0.75,
                                warmth=0.08)

            # 幻觉效果
            if is_ghost:
                img = make_ghost(img, opacity=0.35)
            # 回忆效果
            if is_flashback:
                img = make_flashback(img)

            # 保存 WebP（主格式）
            webp_path = os.path.join(OUTPUT_DIR, f"{filename}.webp")
            img.save(webp_path, "WEBP", quality=85, lossless=False, method=4)
            webp_size = os.path.getsize(webp_path)

            # 保存 PNG（备用格式）
            png_path = os.path.join(OUTPUT_DIR, f"{filename}.png")
            img.save(png_path, "PNG", optimize=True)
            png_size = os.path.getsize(png_path)

            size_str = f"{webp_size/1024:.0f}KB" if webp_size < 500*1024 else f"{webp_size/1024:.0f}KB [>500KB!]"
            print(f"  [OK] {filename}.webp ({w}x{h}) {size_str} | PNG {png_size/1024:.0f}KB")
            success += 1
        except Exception as e:
            print(f"  [FAIL] {filename}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("=" * 60)
    print(f"完成: {success} 成功, {failed} 失败, 共 {len(GENERATORS)} 张")
    print(f"输出目录: {OUTPUT_DIR}/")
    print("=" * 60)

if __name__ == "__main__":
    generate_all()
