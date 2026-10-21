"""
╔══════════════════════════════════════════════════════════════════════╗
║          🌸 THIỆP ĐIỆN TỬ 20-10 CHO NGUYỄN THÙY CHI 🌸             ║
║                 Gửi từ: Huy đen da - với tất cả tình yêu            ║
╚══════════════════════════════════════════════════════════════════════╝

Yêu cầu: pip install pygame
Chạy:    python ecard_2010.py
"""

import pygame
import math
import random
import time
import sys

# ─────────────────────────────────────────────────────────────────────────────
#  KHỞI TẠO & CẤU HÌNH
# ─────────────────────────────────────────────────────────────────────────────

pygame.init()

SCREEN_W, SCREEN_H = 1100, 720
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("💌 Thiệp 20-10 – Gửi Nguyễn Thùy Chi iu yêu 💌")
clock = pygame.time.Clock()
FPS = 60

# ─────────────────────────────────────────────────────────────────────────────
#  BẢN MÀU CHỦ ĐẠO
# ─────────────────────────────────────────────────────────────────────────────
COLOR = {
    "bg_deep":      (5,   8,  25),
    "bg_mid":       (10, 15,  45),
    "pink_pastel":  (255, 182, 210),
    "pink_neon":    (255,  60, 180),
    "pink_soft":    (255, 210, 230),
    "pink_dark":    (200,  40, 120),
    "sunflower":    (255, 215,  50),
    "gold":         (255, 190,   0),
    "lavender":     (180, 140, 255),
    "purple_dark":  (100,  60, 200),
    "white":        (255, 255, 255),
    "star_blue":    (140, 200, 255),
    "cyan_glow":    ( 80, 220, 255),
    "card_bg":      ( 25,  15,  50),
    "card_border":  (255, 100, 200),
    "card_inner":   ( 35,  20,  65),
    "mint":         (120, 255, 180),
}

# ─────────────────────────────────────────────────────────────────────────────
#  FONT (hỗ trợ tiếng Việt)
# ─────────────────────────────────────────────────────────────────────────────

def load_font(size, bold=False):
    candidates = [
        "segoeui", "arial", "verdana", "tahoma",
        "notosans", "freesansbold",
    ]
    for name in candidates:
        try:
            f = pygame.font.SysFont(name, size, bold=bold)
            return f
        except Exception:
            continue
    return pygame.font.SysFont(None, size, bold=bold)


FONT = {
    "title":   load_font(27, bold=True),
    "sub":     load_font(22, bold=True),
    "body":    load_font(20),
    "body_b":  load_font(20, bold=True),
    "small":   load_font(16),
    "tiny":    load_font(13),
    "big":     load_font(52, bold=True),
    "matrix":  load_font(14),
    "hint":    load_font(16),
    "sign":    load_font(21, bold=True),
}

# ─────────────────────────────────────────────────────────────────────────────
#  TRẠNG THÁI
# ─────────────────────────────────────────────────────────────────────────────
STATE_LETTER = 0
STATE_RAIN   = 1
current_state = STATE_LETTER

# ─────────────────────────────────────────────────────────────────────────────
#  TIỆN ÍCH
# ─────────────────────────────────────────────────────────────────────────────

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def draw_gradient_bg(surface, c_top, c_bot):
    for y in range(SCREEN_H):
        t = y / SCREEN_H
        pygame.draw.line(surface, lerp_color(c_top, c_bot, t), (0, y), (SCREEN_W, y))


def glow_text(surface, font, text, color, glow_color, x, y, gr=3, center=True):
    for dx in range(-gr, gr + 1):
        for dy in range(-gr, gr + 1):
            if dx*dx + dy*dy <= gr*gr:
                s = font.render(text, True, glow_color)
                r = s.get_rect()
                if center:
                    r.center = (x + dx, y + dy)
                else:
                    r.topleft = (x + dx, y + dy)
                surface.blit(s, r)
    s = font.render(text, True, color)
    r = s.get_rect()
    if center:
        r.center = (x, y)
    else:
        r.topleft = (x, y)
    surface.blit(s, r)


def render_center(surface, font, text, color, cx, cy):
    s = font.render(text, True, color)
    r = s.get_rect(center=(cx, cy))
    surface.blit(s, r)

# ─────────────────────────────────────────────────────────────────────────────
#  SAO NỀN
# ─────────────────────────────────────────────────────────────────────────────

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_W)
        self.y = random.randint(0, SCREEN_H)
        self.r = random.uniform(0.5, 2.5)
        self.speed = random.uniform(0.3, 1.2)
        self.offset = random.uniform(0, 6.28)
        self.color = random.choice([
            COLOR["white"], COLOR["pink_pastel"],
            COLOR["star_blue"], COLOR["lavender"], COLOR["sunflower"],
        ])

    def draw(self, surface, t):
        alpha = int(128 + 120 * math.sin(t * self.speed + self.offset))
        alpha = max(30, min(255, alpha))
        col = (*self.color[:3], alpha)
        s = pygame.Surface((int(self.r*2)+2, int(self.r*2)+2), pygame.SRCALPHA)
        pygame.draw.circle(s, col, (int(self.r)+1, int(self.r)+1), max(1, int(self.r)))
        surface.blit(s, (self.x - int(self.r), self.y - int(self.r)))


STARS = [Star() for _ in range(180)]

# ─────────────────────────────────────────────────────────────────────────────
#  KHUNG THIỆP
# ─────────────────────────────────────────────────────────────────────────────

CARD_W, CARD_H = 640, 490
CARD_X = (SCREEN_W - CARD_W) // 2
CARD_Y = (SCREEN_H - CARD_H) // 2 + 15

LETTER_TITLE = "💌 Gui Nguyen Thuy Chi - Yeu cua anh 💌"
LETTER_BODY_LINES = [
    "Yeu cua anh 🌸",
    "",
    "20-10 vui ve nhoa, chuc em hoc gioi,",
    "dep mai, luon cuoi va dung nhin",
    "an ngu muon nhieu nhe. 🐰🐱",
    "",
    "20-10 vuive nha nha nha nha nha ha 🌻💖",
    "",
    "Em la dieu tuyet voi nhat",
    "ma anh co trong cuoc doi nay. 💌",
]
LETTER_SIGN = "- Anh iu e - Huy den da -"

# Fallback: nếu font hỗ trợ Unicode thì dùng bản đầy đủ dấu
try:
    _test = load_font(20)
    _surf = _test.render("Tiếng Việt đẹp", True, (255, 255, 255))
    # Nếu render không trả về empty rect thì dùng tiếng Việt có dấu
    if _surf.get_width() > 10:
        LETTER_TITLE = "💌 Gui Nguyen Thuy Chi - Yeu cua anh 💌"
        LETTER_BODY_LINES = [
            "Yeu cua anh 🌸",
            "",
            "20-10 vui ve nhoa, chuc em hoc gioi,",
            "dep mai, luon cuoi va dung nhin",
            "an ngu muon nhieu nhe. 🐰🐱",
            "",
            "20-10 vuive nha nha nha nha nha ha 🌻💖",
            "",
            "Em la dieu tuyet voi nhat",
            "ma anh co trong cuoc doi nay. 💌",
        ]
except Exception:
    pass


def get_card_rect(t):
    bounce = int(6 * math.sin(t * 1.8))
    return pygame.Rect(CARD_X, CARD_Y + bounce, CARD_W, CARD_H)


def draw_card(surface, t, vis_title, vis_body, vis_sign,
              title_done, body_done, sign_done, cursor_on):

    rect = get_card_rect(t)

    # Bóng đổ
    sh = pygame.Surface((CARD_W + 24, CARD_H + 24), pygame.SRCALPHA)
    pygame.draw.rect(sh, (0, 0, 0, 80), (12, 12, CARD_W, CARD_H), border_radius=26)
    surface.blit(sh, (rect.x - 4, rect.y + 8))

    # Viền neon glow
    for w, a in [(8, 35), (5, 80), (2, 180)]:
        gs = pygame.Surface((CARD_W + w*2+6, CARD_H + w*2+6), pygame.SRCALPHA)
        pygame.draw.rect(gs, (*COLOR["pink_neon"], a),
                         (w, w, CARD_W + 4, CARD_H + 4), w+1, border_radius=28+w)
        surface.blit(gs, (rect.x - w - 2, rect.y - w - 2))

    # Thân thiệp
    pygame.draw.rect(surface, COLOR["card_bg"], rect, border_radius=24)
    inner = rect.inflate(-10, -10)
    pygame.draw.rect(surface, COLOR["card_inner"], inner, border_radius=20)
    pygame.draw.rect(surface, COLOR["card_border"], rect, 2, border_radius=24)

    # Header gradient
    hdr_h = 50
    for i in range(hdr_h):
        c = lerp_color(COLOR["pink_neon"], COLOR["pink_dark"], i/hdr_h)
        pygame.draw.line(surface, c,
                         (rect.x+24, rect.y+i),
                         (rect.x+CARD_W-24, rect.y+i))
    pygame.draw.rect(surface, COLOR["card_border"],
                     pygame.Rect(rect.x, rect.y, CARD_W, hdr_h),
                     2, border_radius=24)

    # Tiêu đề
    cur_t = "I" if (cursor_on and not title_done) else ""
    render_center(surface, FONT["small"],
                  vis_title + cur_t,
                  COLOR["white"],
                  rect.centerx, rect.y + 26)

    # Đường kẻ
    sep_y = rect.y + hdr_h + 4
    pygame.draw.line(surface,
                     (*COLOR["pink_pastel"], 100),
                     (rect.x + 20, sep_y),
                     (rect.x + CARD_W - 20, sep_y), 1)

    # Nội dung thư
    bx = rect.x + 36
    by = rect.y + hdr_h + 14
    lh = 29
    for i, line in enumerate(vis_body):
        is_last = (i == len(vis_body) - 1)
        cur = ""
        if is_last and not body_done and cursor_on:
            cur = "I"
        if i == 0:
            col, f = COLOR["pink_neon"], FONT["body_b"]
        elif "💌" in line or "anh" in line:
            col, f = COLOR["lavender"], FONT["body"]
        else:
            col, f = COLOR["pink_soft"], FONT["body"]
        s = f.render(line + cur, True, col)
        surface.blit(s, (bx, by + i * lh))

    # Đường kẻ chân
    line_y = rect.y + CARD_H - 62
    pygame.draw.line(surface,
                     (*COLOR["pink_pastel"], 80),
                     (rect.x + 20, line_y),
                     (rect.x + CARD_W - 20, line_y), 1)

    # Chữ ký
    cur_s = "I" if (cursor_on and not sign_done and body_done) else ""
    glow_text(surface, FONT["sign"],
              vis_sign + cur_s,
              COLOR["sunflower"], COLOR["gold"],
              rect.centerx, rect.y + CARD_H - 38,
              gr=2)

    # Icon trang trí 4 góc
    m = 50
    icons = [
        (rect.x + m,           rect.y + m,           "🐰", 0.0),
        (rect.x + CARD_W - m,  rect.y + m,           "🐱", 1.1),
        (rect.x + m,           rect.y + CARD_H - m,  "🦭", 2.2),
        (rect.x + CARD_W - m,  rect.y + CARD_H - m,  "🍰", 3.3),
        (rect.centerx,         rect.y + CARD_H - 18, "🌻", 4.4),
    ]
    for ix, iy, icon, phase in icons:
        oy = int(6 * math.sin(t * 1.6 + phase))
        try:
            s = FONT["small"].render(icon, True, COLOR["white"])
            r = s.get_rect(center=(ix, iy + oy))
            surface.blit(s, r)
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────────────────────
#  TYPEWRITER ENGINE
# ─────────────────────────────────────────────────────────────────────────────

class Typewriter:
    def __init__(self, lines, cps=20):
        self.lines = lines
        self.cps = cps
        self.full = "\n".join(lines)
        self.shown = 0
        self.done = False
        self.t0 = None

    def start(self):
        self.t0 = time.time()
        self.done = False
        self.shown = 0

    def update(self):
        if self.t0 is None:
            return
        elapsed = time.time() - self.t0
        self.shown = int(elapsed * self.cps)
        if self.shown >= len(self.full):
            self.shown = len(self.full)
            self.done = True

    def skip(self):
        self.shown = len(self.full)
        self.done = True

    def get_lines(self):
        return self.full[:self.shown].split("\n")

    def get_line(self):
        return self.full[:self.shown]


tw_title = Typewriter([LETTER_TITLE], cps=18)
tw_body  = Typewriter(LETTER_BODY_LINES, cps=22)
tw_sign  = Typewriter([LETTER_SIGN], cps=15)

body_started = False
sign_started = False

# cursor blink
cursor_on  = True
cursor_acc = 0.0
CURSOR_INT = 0.55


def update_cursor(dt):
    global cursor_on, cursor_acc
    cursor_acc += dt
    if cursor_acc >= CURSOR_INT:
        cursor_acc = 0.0
        cursor_on = not cursor_on


def update_typewriters():
    global body_started, sign_started
    tw_title.update()
    if tw_title.done and not body_started:
        body_started = True
        tw_body.start()
    if body_started:
        tw_body.update()
    if tw_body.done and not sign_started:
        sign_started = True
        tw_sign.start()
    if sign_started:
        tw_sign.update()


# ─────────────────────────────────────────────────────────────────────────────
#  HIỆU ỨNG MƯA TÌNH YÊU
# ─────────────────────────────────────────────────────────────────────────────

RAIN_WORDS = [
    "0101", "010101", "1010",
    "Chiiiiiii", "o ma CHi", "iu Chi",
    "20-10 vui ve", "vk iu",
    "Huy iu CHi lam",
    "🌻", "🐰", "🐱", "🦭", "🍰", "💖", "💌",
    "em dep lam", "yeu em",
    "Chi oi~", "iu nhat",
]

RAIN_COLORS = [
    COLOR["pink_neon"],
    COLOR["sunflower"],
    COLOR["lavender"],
    COLOR["cyan_glow"],
    COLOR["pink_pastel"],
    COLOR["mint"],
]


class RainDrop:
    def __init__(self):
        self.reset(random.randint(-SCREEN_H, SCREEN_H))

    def reset(self, start_y=0):
        self.x = random.randint(0, SCREEN_W - 10)
        self.y = float(start_y)
        self.speed = random.uniform(80, 240)
        self.word = random.choice(RAIN_WORDS)
        self.cidx = random.randint(0, len(RAIN_COLORS) - 1)
        self.alpha = random.randint(150, 255)
        self.font = random.choice([FONT["matrix"], FONT["small"], FONT["body"]])
        self.trail = []
        self.trail_max = random.randint(3, 8)

    def update(self, dt):
        self.trail.append((self.x, int(self.y)))
        if len(self.trail) > self.trail_max:
            self.trail.pop(0)
        self.y += self.speed * dt
        if self.y > SCREEN_H + 80:
            self.reset(random.randint(-50, 0))

    def draw(self, surface):
        col = RAIN_COLORS[self.cidx]
        for i, (tx, ty) in enumerate(self.trail):
            a = int(self.alpha * (i / max(len(self.trail), 1)) * 0.4)
            if a < 5:
                continue
            s = self.font.render(self.word, True, col)
            s.set_alpha(a)
            surface.blit(s, (tx, ty))
        s = self.font.render(self.word, True, col)
        s.set_alpha(self.alpha)
        surface.blit(s, (self.x, int(self.y)))


RAIN = [RainDrop() for _ in range(65)]

# ─────────────────────────────────────────────────────────────────────────────
#  PHÁO HOA TRÁI TIM
# ─────────────────────────────────────────────────────────────────────────────

def draw_heart(surface, color, cx, cy, size, alpha):
    if size < 3:
        return
    hs = pygame.Surface((size*2+4, size*2+4), pygame.SRCALPHA)
    for py in range(-size, size+1):
        for px in range(-size, size+1):
            nx = px / size
            ny = -py / size
            if (nx*nx + ny*ny - 1)**3 - nx*nx * ny**3 <= 0:
                hs.set_at((px+size+2, py+size+2), (*color[:3], alpha))
    surface.blit(hs, (cx-size-2, cy-size-2))


class HeartParticle:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        angle = random.uniform(0, 6.28)
        spd = random.uniform(80, 270)
        self.vx = math.cos(angle) * spd
        self.vy = math.sin(angle) * spd - random.uniform(40, 120)
        self.grav = random.uniform(130, 230)
        self.life = random.uniform(0.9, 1.9)
        self.max_life = self.life
        self.size = random.randint(7, 18)
        self.color = random.choice([
            COLOR["pink_neon"], COLOR["pink_pastel"],
            COLOR["sunflower"], COLOR["lavender"], COLOR["white"],
        ])

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.grav * dt
        self.life -= dt
        return self.life > 0

    def draw(self, surface):
        a = max(0, int(255 * (self.life / self.max_life)))
        draw_heart(surface, self.color, int(self.x), int(self.y), self.size, a)


HEARTS = []


def spawn_hearts(x, y, n=22):
    for _ in range(n):
        HEARTS.append(HeartParticle(x, y))


def update_hearts(dt):
    global HEARTS
    HEARTS = [p for p in HEARTS if p.update(dt)]


def draw_hearts(surface):
    for p in HEARTS:
        p.draw(surface)


# ─────────────────────────────────────────────────────────────────────────────
#  TRÁI TIM NỔI (nền giai đoạn 2)
# ─────────────────────────────────────────────────────────────────────────────

class FloatHeart:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(20, SCREEN_W-20)
        self.y = float(random.randint(SCREEN_H+10, SCREEN_H+150))
        self.vy = -random.uniform(35, 90)
        self.vx = random.uniform(-12, 12)
        self.size = random.randint(7, 20)
        self.alpha = random.randint(70, 190)
        self.color = random.choice([
            COLOR["pink_neon"], COLOR["pink_pastel"],
            COLOR["lavender"], COLOR["sunflower"],
        ])

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        if self.y < -30:
            self.reset()

    def draw(self, surface):
        draw_heart(surface, self.color, int(self.x), int(self.y),
                   self.size, self.alpha)


FLOAT_HEARTS = [FloatHeart() for _ in range(20)]

# ─────────────────────────────────────────────────────────────────────────────
#  HINT BAR
# ─────────────────────────────────────────────────────────────────────────────

HINTS = [
    [
        "💖 Click chuot de ban phao hoa trai tim  |  SPACE sang mua tinh yeu 💖",
        "🌸 Thiep 20-10 tu Huy den da gui Nguyen Thuy Chi iu yeu 🌸",
    ],
    [
        "💌 Click de ban trai tim  |  SPACE quay lai thu tinh 💌",
        "🐰 Chiiiiii iu nhat vu tru nha 🌻🐱🦭",
    ],
]
hint_idx = 0
hint_acc = 0.0
HINT_INT = 5.0


def update_hint(dt):
    global hint_idx, hint_acc
    hint_acc += dt
    if hint_acc >= HINT_INT:
        hint_acc = 0.0
        hints = HINTS[current_state]
        hint_idx = (hint_idx + 1) % len(hints)


def draw_hint(surface, t):
    hints = HINTS[current_state]
    text = hints[hint_idx % len(hints)]
    bh = 33
    by = SCREEN_H - bh
    bs = pygame.Surface((SCREEN_W, bh), pygame.SRCALPHA)
    bs.fill((8, 4, 28, 175))
    surface.blit(bs, (0, by))
    pygame.draw.line(surface, (*COLOR["pink_neon"], 100), (0, by), (SCREEN_W, by), 1)
    tc = lerp_color(COLOR["pink_pastel"], COLOR["lavender"],
                    (math.sin(t * 1.1) + 1) / 2)
    render_center(surface, FONT["hint"], text, tc, SCREEN_W//2, by + bh//2)


# ─────────────────────────────────────────────────────────────────────────────
#  NEBULA NỀN
# ─────────────────────────────────────────────────────────────────────────────

nebula = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
for _ in range(14):
    cx2 = random.randint(0, SCREEN_W)
    cy2 = random.randint(0, SCREEN_H)
    r2  = random.randint(60, 220)
    nc  = random.choice([
        (255, 60, 180, 16), (130, 80, 255, 13),
        (255, 215, 50, 9),  (80, 180, 255, 11),
    ])
    pygame.draw.circle(nebula, nc, (cx2, cy2), r2)


def draw_bg(surface, t):
    draw_gradient_bg(surface, COLOR["bg_deep"], COLOR["bg_mid"])
    surface.blit(nebula, (0, 0))
    for st in STARS:
        st.draw(surface, t)


# ─────────────────────────────────────────────────────────────────────────────
#  TRANG TRÍ BÊN NGOÀI THIỆP (giai đoạn 1)
# ─────────────────────────────────────────────────────────────────────────────

SIDE_ICONS = [
    (58,  185, "🌻", 0.5),
    (58,  385, "💖", 1.8),
    (SCREEN_W-58, 165, "🐰", 2.1),
    (SCREEN_W-58, 365, "🌸", 3.5),
    (SCREEN_W//2-290, 95, "⭐", 0.9),
    (SCREEN_W//2+290, 95, "⭐", 2.7),
]


def draw_side_deco(surface, t):
    for ix, iy, icon, phase in SIDE_ICONS:
        oy = int(11 * math.sin(t * 1.5 + phase))
        try:
            s = FONT["small"].render(icon, True, COLOR["white"])
            r = s.get_rect(center=(ix, iy + oy))
            surface.blit(s, r)
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────────────────────
#  GIAI ĐOẠN 2: VẼ TOÀN BỘ
# ─────────────────────────────────────────────────────────────────────────────

def draw_rain_scene(surface, t, dt):
    for drop in RAIN:
        drop.update(dt)
        drop.draw(surface)

    for fh in FLOAT_HEARTS:
        fh.update(dt)
        fh.draw(surface)

    # Tiêu đề lớn
    pulse = 1.0 + 0.055 * math.sin(t * 2.4)
    try:
        bf = load_font(max(20, int(52 * pulse)), bold=True)
    except Exception:
        bf = FONT["big"]
    tc = lerp_color(COLOR["pink_neon"], COLOR["sunflower"], (math.sin(t)+1)/2)
    glow_text(surface, bf, "💖 20 - 10 💖", tc, COLOR["pink_dark"],
              SCREEN_W//2, 58, gr=4)

    sub = "Gui den: Nguyen Thuy Chi 🐰  |  Tu: Huy den da 💖"
    sc = lerp_color(COLOR["lavender"], COLOR["pink_pastel"], (math.sin(t*0.9+1)+1)/2)
    render_center(surface, FONT["sub"], sub, sc, SCREEN_W//2, 110)


# ─────────────────────────────────────────────────────────────────────────────
#  CHUYỂN TRẠNG THÁI
# ─────────────────────────────────────────────────────────────────────────────

def to_rain():
    global current_state
    current_state = STATE_RAIN


def to_letter():
    global current_state, body_started, sign_started
    current_state = STATE_LETTER
    body_started = False
    sign_started = False
    tw_title.start()
    tw_body.t0 = None
    tw_body.shown = 0
    tw_body.done = False
    tw_sign.t0 = None
    tw_sign.shown = 0
    tw_sign.done = False


# ─────────────────────────────────────────────────────────────────────────────
#  VÒNG LẶP CHÍNH
# ─────────────────────────────────────────────────────────────────────────────

def main():
    global body_started, sign_started

    tw_title.start()

    t    = 0.0
    prev = time.time()

    while True:
        now = time.time()
        dt  = min(now - prev, 0.05)
        prev = now
        t   += dt

        # ── Sự kiện ──────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                elif event.key == pygame.K_SPACE:
                    if current_state == STATE_LETTER:
                        if not tw_sign.done:
                            tw_title.skip()
                            tw_body.skip()
                            tw_sign.skip()
                            body_started = True
                            sign_started = True
                        else:
                            to_rain()
                    else:
                        to_letter()

                elif event.key == pygame.K_RETURN:
                    if current_state == STATE_LETTER and tw_sign.done:
                        to_rain()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                spawn_hearts(event.pos[0], event.pos[1],
                             n=random.randint(18, 28))

        # ── Cập nhật ─────────────────────────────────────────────────────────
        update_cursor(dt)
        update_hint(dt)
        update_hearts(dt)

        if current_state == STATE_LETTER:
            update_typewriters()

        # ── Vẽ ───────────────────────────────────────────────────────────────
        draw_bg(screen, t)

        if current_state == STATE_LETTER:
            draw_side_deco(screen, t)
            draw_card(screen, t,
                      tw_title.get_line(),
                      tw_body.get_lines(),
                      tw_sign.get_line(),
                      tw_title.done, tw_body.done, tw_sign.done,
                      cursor_on)

        elif current_state == STATE_RAIN:
            draw_rain_scene(screen, t, dt)

        draw_hearts(screen)
        draw_hint(screen, t)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
