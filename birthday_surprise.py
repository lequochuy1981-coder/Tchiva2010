import pygame
import sys
import math
import random
import time

# ============================================================
#  BIRTHDAY SURPRISE - "Sinh nhật Thùy Chi"
#  A sweet candy-themed virtual birthday world in Python/Pygame
# ============================================================

pygame.init()

# --- Screen Setup ---
SCREEN_W, SCREEN_H = 1000, 700
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("🎂 Sinh nhật Thùy Chi 🎂")
clock = pygame.time.Clock()

# --- Color Palette ---
CANDY_PINK      = (255, 105, 180)
CANDY_LIGHT_PINK= (255, 182, 213)
CANDY_HOT_PINK  = (255, 20, 147)
CANDY_WHITE     = (255, 245, 250)
CANDY_YELLOW    = (255, 223, 70)
CANDY_ORANGE    = (255, 165, 80)
CANDY_MINT      = (152, 255, 200)
CANDY_LAVENDER  = (200, 162, 255)
CANDY_BLUE      = (135, 206, 255)
CANDY_RED       = (255, 100, 100)
CANDY_CORAL     = (255, 127, 80)
GOLD            = (255, 215, 0)
WHITE           = (255, 255, 255)
BLACK           = (0, 0, 0)
DARK_PINK       = (180, 50, 100)
SOFT_WHITE      = (255, 250, 255)

# Meadow colors
SKY_TOP         = (135, 206, 250)
SKY_BOTTOM      = (200, 230, 255)
GRASS_GREEN     = (100, 180, 60)
GRASS_DARK      = (70, 140, 40)
GRASS_LIGHT     = (130, 200, 80)
DIRT_BROWN      = (139, 119, 80)
CLOUD_WHITE     = (255, 255, 255)
SUN_YELLOW      = (255, 230, 80)
ENVELOPE_CREAM  = (255, 245, 220)
ENVELOPE_FLAP   = (240, 220, 180)
SEAL_RED        = (220, 50, 50)

# --- Background Gradient Colors (sweet pastel) ---
BG_TOP    = (255, 182, 213)
BG_MIDDLE = (255, 210, 230)
BG_BOTTOM = (200, 162, 255)

# --- Fonts ---
def get_font(size, bold=False):
    """Try to load a nice font, fallback to default."""
    font_names = ["Segoe UI", "Arial", "Tahoma", "Verdana"]
    for name in font_names:
        try:
            path = pygame.font.match_font(name, bold=bold)
            if path:
                return pygame.font.Font(path, size)
        except:
            pass
    return pygame.font.Font(None, size)

font_title    = get_font(72, bold=True)
font_subtitle = get_font(28, bold=False)
font_loading  = get_font(22, bold=True)
font_play     = get_font(36, bold=True)
font_small    = get_font(18)
font_big      = get_font(90, bold=True)
font_medium   = get_font(40, bold=True)
font_emoji    = get_font(32)
font_matrix   = get_font(16, bold=True)
font_open_btn = get_font(30, bold=True)

# ============================================================
#  UTILITY: Draw gradient background (candy theme)
# ============================================================
def draw_gradient_bg(surface, t):
    """Draw a dreamy animated gradient background."""
    for y in range(SCREEN_H):
        ratio = y / SCREEN_H
        shift = math.sin(t * 0.3 + ratio * 2) * 15
        if ratio < 0.5:
            r2 = ratio * 2
            r = int(BG_TOP[0] + (BG_MIDDLE[0] - BG_TOP[0]) * r2 + shift)
            g = int(BG_TOP[1] + (BG_MIDDLE[1] - BG_TOP[1]) * r2 + shift * 0.5)
            b = int(BG_TOP[2] + (BG_MIDDLE[2] - BG_TOP[2]) * r2)
        else:
            r2 = (ratio - 0.5) * 2
            r = int(BG_MIDDLE[0] + (BG_BOTTOM[0] - BG_MIDDLE[0]) * r2 + shift)
            g = int(BG_MIDDLE[1] + (BG_BOTTOM[1] - BG_MIDDLE[1]) * r2)
            b = int(BG_MIDDLE[2] + (BG_BOTTOM[2] - BG_MIDDLE[2]) * r2 + shift * 0.5)
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_W, y))

# ============================================================
#  UTILITY: Draw sparkle / star
# ============================================================
def draw_star(surface, x, y, size, color, alpha=255):
    """Draw a small sparkle/star."""
    s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
    cx, cy = size, size
    for i in range(4):
        angle = i * math.pi / 2
        ex = cx + math.cos(angle) * size
        ey = cy + math.sin(angle) * size
        pygame.draw.line(s, (*color, alpha), (cx, cy), (int(ex), int(ey)), 2)
    for i in range(4):
        angle = i * math.pi / 2 + math.pi / 4
        ex = cx + math.cos(angle) * size * 0.5
        ey = cy + math.sin(angle) * size * 0.5
        pygame.draw.line(s, (*color, alpha), (cx, cy), (int(ex), int(ey)), 1)
    surface.blit(s, (x - size, y - size))

# ============================================================
#  PARTICLE: Candy
# ============================================================
class Candy:
    CANDY_TYPES = ['circle', 'rect', 'lollipop', 'wrapper', 'heart', 'star_candy']
    COLORS = [CANDY_PINK, CANDY_HOT_PINK, CANDY_YELLOW, CANDY_ORANGE,
              CANDY_MINT, CANDY_LAVENDER, CANDY_BLUE, CANDY_RED, CANDY_CORAL,
              CANDY_LIGHT_PINK, GOLD]

    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, SCREEN_W)
        self.y = random.randint(-SCREEN_H, -20)
        self.speed = random.uniform(1.0, 3.5)
        self.wobble_speed = random.uniform(1, 4)
        self.wobble_amp = random.uniform(10, 40)
        self.size = random.randint(8, 22)
        self.color = random.choice(self.COLORS)
        self.candy_type = random.choice(self.CANDY_TYPES)
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-3, 3)
        self.phase = random.uniform(0, math.pi * 2)
        self.alpha = random.randint(180, 255)

    def update(self, dt):
        self.y += self.speed * dt * 60
        self.x += math.sin(time.time() * self.wobble_speed + self.phase) * 0.5
        self.rotation += self.rot_speed * dt * 60
        if self.y > SCREEN_H + 30:
            self.reset()
            self.y = random.randint(-100, -20)

    def draw(self, surface):
        s = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
        cx, cy = self.size * 2, self.size * 2
        c = (*self.color, self.alpha)
        c2 = (*WHITE, self.alpha)

        if self.candy_type == 'circle':
            pygame.draw.circle(s, c, (cx, cy), self.size)
            pygame.draw.circle(s, c2, (cx, cy), self.size, 2)
            pygame.draw.line(s, c2, (cx - self.size + 3, cy), (cx + self.size - 3, cy), 2)
            pygame.draw.circle(s, (*WHITE, 120), (cx - self.size // 3, cy - self.size // 3), self.size // 4)
        elif self.candy_type == 'rect':
            rect = pygame.Rect(cx - self.size, cy - self.size // 2, self.size * 2, self.size)
            pygame.draw.rect(s, c, rect, border_radius=4)
            pygame.draw.rect(s, c2, rect, 2, border_radius=4)
            pygame.draw.polygon(s, c, [
                (cx - self.size - 8, cy - 2), (cx - self.size - 8, cy + 2),
                (cx - self.size, cy + self.size // 2), (cx - self.size, cy - self.size // 2)])
            pygame.draw.polygon(s, c, [
                (cx + self.size + 8, cy - 2), (cx + self.size + 8, cy + 2),
                (cx + self.size, cy + self.size // 2), (cx + self.size, cy - self.size // 2)])
        elif self.candy_type == 'lollipop':
            pygame.draw.circle(s, c, (cx, cy - 4), self.size)
            pygame.draw.circle(s, c2, (cx, cy - 4), self.size // 2)
            pygame.draw.circle(s, c2, (cx, cy - 4), self.size, 2)
            pygame.draw.line(s, (*CANDY_WHITE, self.alpha), (cx, cy + self.size - 4),
                             (cx, cy + self.size + 12), 3)
        elif self.candy_type == 'heart':
            self._draw_heart(s, cx, cy, self.size, c)
            self._draw_heart(s, cx, cy, self.size, c2, width=2)
            pygame.draw.circle(s, (*WHITE, 100), (cx - self.size // 4, cy - self.size // 4), self.size // 5)
        elif self.candy_type == 'star_candy':
            self._draw_star_shape(s, cx, cy, self.size, c)
            self._draw_star_shape(s, cx, cy, self.size, c2, width=2)
        elif self.candy_type == 'wrapper':
            pygame.draw.ellipse(s, c, (cx - self.size, cy - self.size // 2, self.size * 2, self.size))
            pygame.draw.ellipse(s, c2, (cx - self.size, cy - self.size // 2, self.size * 2, self.size), 2)
            for i in range(-self.size + 4, self.size, 6):
                pygame.draw.line(s, c2, (cx + i, cy - self.size // 2 + 3), (cx + i, cy + self.size // 2 - 3), 1)

        rotated = pygame.transform.rotate(s, self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)

    def _draw_heart(self, surface, cx, cy, size, color, width=0):
        pts = []
        for i in range(100):
            t = i / 100 * 2 * math.pi
            x = 16 * math.sin(t) ** 3
            y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
            scale = size / 18
            pts.append((int(cx + x * scale), int(cy + y * scale)))
        if len(pts) > 2:
            if width == 0:
                pygame.draw.polygon(surface, color, pts)
            else:
                pygame.draw.polygon(surface, color, pts, width)

    def _draw_star_shape(self, surface, cx, cy, size, color, width=0):
        pts = []
        for i in range(10):
            angle = i * math.pi / 5 - math.pi / 2
            r = size if i % 2 == 0 else size * 0.45
            pts.append((int(cx + r * math.cos(angle)), int(cy + r * math.sin(angle))))
        if width == 0:
            pygame.draw.polygon(surface, color, pts)
        else:
            pygame.draw.polygon(surface, color, pts, width)

# ============================================================
#  PARTICLE: Sunflower
# ============================================================
class Sunflower:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, SCREEN_W)
        self.y = random.randint(-SCREEN_H, -30)
        self.speed = random.uniform(0.8, 2.5)
        self.size = random.randint(14, 28)
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-2, 2)
        self.wobble = random.uniform(1, 3)
        self.phase = random.uniform(0, math.pi * 2)
        self.alpha = random.randint(200, 255)

    def update(self, dt):
        self.y += self.speed * dt * 60
        self.x += math.sin(time.time() * self.wobble + self.phase) * 0.8
        self.rotation += self.rot_speed * dt * 60
        if self.y > SCREEN_H + 40:
            self.reset()
            self.y = random.randint(-120, -30)

    def draw(self, surface):
        s = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
        cx, cy = self.size * 2, self.size * 2
        num_petals = 12
        for i in range(num_petals):
            angle = i * (360 / num_petals) + self.rotation
            rad = math.radians(angle)
            px = cx + math.cos(rad) * self.size * 0.7
            py = cy + math.sin(rad) * self.size * 0.7
            petal_color = (255, 200 + random.randint(-10, 10), 0, self.alpha)
            pygame.draw.ellipse(s, petal_color,
                                (int(px - self.size * 0.35), int(py - self.size * 0.18),
                                 int(self.size * 0.7), int(self.size * 0.36)))
            angle2 = angle + 360 / num_petals / 2
            rad2 = math.radians(angle2)
            px2 = cx + math.cos(rad2) * self.size * 0.8
            py2 = cy + math.sin(rad2) * self.size * 0.8
            petal_color2 = (255, 220, 50, self.alpha - 30)
            pygame.draw.ellipse(s, petal_color2,
                                (int(px2 - self.size * 0.28), int(py2 - self.size * 0.14),
                                 int(self.size * 0.56), int(self.size * 0.28)))
        pygame.draw.circle(s, (101, 67, 33, self.alpha), (cx, cy), int(self.size * 0.35))
        pygame.draw.circle(s, (139, 90, 43, self.alpha), (cx, cy), int(self.size * 0.28))
        for _ in range(8):
            dx = random.randint(-int(self.size * 0.2), int(self.size * 0.2))
            dy = random.randint(-int(self.size * 0.2), int(self.size * 0.2))
            if dx * dx + dy * dy < (self.size * 0.25) ** 2:
                pygame.draw.circle(s, (80, 50, 20, self.alpha), (cx + dx, cy + dy), 1)
        rotated = pygame.transform.rotate(s, self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)

# ============================================================
#  PARTICLE: Sparkle
# ============================================================
class Sparkle:
    def __init__(self):
        self.x = random.randint(0, SCREEN_W)
        self.y = random.randint(0, SCREEN_H)
        self.life = random.uniform(0, math.pi * 2)
        self.speed = random.uniform(1, 3)
        self.size = random.randint(3, 8)
        self.color = random.choice([WHITE, CANDY_YELLOW, CANDY_PINK, CANDY_LIGHT_PINK, GOLD])

    def update(self, dt):
        self.life += self.speed * dt
        if self.life > math.pi * 2:
            self.life -= math.pi * 2
            self.x = random.randint(0, SCREEN_W)
            self.y = random.randint(0, SCREEN_H)

    def draw(self, surface):
        alpha = int(abs(math.sin(self.life)) * 200)
        if alpha > 20:
            draw_star(surface, self.x, self.y, self.size, self.color, alpha)

# ============================================================
#  CANDY TEXT RENDERER
# ============================================================
def render_candy_text(text, font, t, base_y, surface, shadow=True):
    """Render text with candy-like pink/white striped effect and animation."""
    test_surf = font.render(text, True, WHITE)
    text_w, text_h = test_surf.get_size()
    start_x = (SCREEN_W - text_w) // 2

    text_surface = pygame.Surface((text_w + 20, text_h + 20), pygame.SRCALPHA)

    if shadow:
        shadow_surf = font.render(text, True, (180, 50, 100, 80))
        surface.blit(shadow_surf, (start_x + 3, base_y + 3))

    main_text = font.render(text, True, CANDY_PINK)
    mask = pygame.mask.from_surface(main_text)

    candy_surface = pygame.Surface((text_w, text_h), pygame.SRCALPHA)
    candy_surface.blit(main_text, (0, 0))

    stripe_surf = pygame.Surface((text_w, text_h), pygame.SRCALPHA)
    stripe_width = 8
    offset = int(t * 30) % (stripe_width * 2)
    for i in range(-text_h, text_w + text_h, stripe_width * 2):
        x_start = i + offset
        pts = [(x_start, 0), (x_start + stripe_width, 0),
               (x_start + stripe_width - text_h, text_h), (x_start - text_h, text_h)]
        pygame.draw.polygon(stripe_surf, (*WHITE, 140), pts)

    for x in range(text_w):
        for y in range(text_h):
            if x < mask.get_size()[0] and y < mask.get_size()[1]:
                if not mask.get_at((x, y)):
                    stripe_surf.set_at((x, y), (0, 0, 0, 0))
    candy_surface.blit(stripe_surf, (0, 0))

    glow_alpha = int(abs(math.sin(t * 2)) * 40 + 20)
    glow_surf = font.render(text, True, (*CANDY_HOT_PINK,))
    glow_s = pygame.Surface((text_w + 10, text_h + 10), pygame.SRCALPHA)
    glow_s.blit(glow_surf, (5, 5))
    glow_s.set_alpha(glow_alpha)
    surface.blit(glow_s, (start_x - 5, base_y - 5))

    outline_color = DARK_PINK
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
        outline_surf = font.render(text, True, outline_color)
        surface.blit(outline_surf, (start_x + dx, base_y + dy))

    surface.blit(candy_surface, (start_x, base_y))

    char_x = start_x
    for i, char in enumerate(text):
        char_surf = font.render(char, True, (0, 0, 0, 0))
        char_w = char_surf.get_width()
        bounce = math.sin(t * 3 + i * 0.5) * 4
        highlight_y = base_y + bounce - 1
        highlight_surf = font.render(char, True, (*WHITE, 80))
        s = pygame.Surface((char_w, text_h), pygame.SRCALPHA)
        s.blit(highlight_surf, (0, 0))
        s.set_alpha(60)
        surface.blit(s, (char_x, int(highlight_y)))
        char_x += char_w
    return text_w, text_h

# ============================================================
#  LOADING BAR
# ============================================================
def draw_loading_bar(surface, progress, t):
    """Draw a candy-styled loading bar."""
    bar_w = 400
    bar_h = 30
    bar_x = (SCREEN_W - bar_w) // 2
    bar_y = SCREEN_H // 2 + 100

    loading_text = "Đang tải kỷ niệm ngọt ngào..."
    lt_surf = font_loading.render(loading_text, True, DARK_PINK)
    lt_rect = lt_surf.get_rect(center=(SCREEN_W // 2, bar_y - 25))
    surface.blit(lt_surf, lt_rect)

    bg_rect = pygame.Rect(bar_x - 3, bar_y - 3, bar_w + 6, bar_h + 6)
    pygame.draw.rect(surface, DARK_PINK, bg_rect, border_radius=15)

    inner_bg = pygame.Rect(bar_x, bar_y, bar_w, bar_h)
    pygame.draw.rect(surface, (255, 220, 230), inner_bg, border_radius=12)

    fill_w = int(bar_w * progress)
    if fill_w > 0:
        fill_surf = pygame.Surface((fill_w, bar_h), pygame.SRCALPHA)
        for x in range(fill_w):
            ratio = x / max(fill_w, 1)
            r = int(255)
            g = int(105 + ratio * 60)
            b = int(180 - ratio * 30)
            for y in range(bar_h):
                y_ratio = y / bar_h
                brightness = 1.0 - abs(y_ratio - 0.3) * 0.3
                fr = min(255, int(r * brightness))
                fg = min(255, int(g * brightness))
                fb = min(255, int(b * brightness))
                fill_surf.set_at((x, y), (fr, fg, fb, 255))

        stripe_offset = int(t * 50) % 20
        for i in range(-bar_h, fill_w + bar_h, 20):
            x_start = i + stripe_offset
            pts = [(x_start, 0), (x_start + 10, 0),
                   (x_start + 10 - bar_h, bar_h), (x_start - bar_h, bar_h)]
            clipped = [(max(0, min(fill_w - 1, px)), max(0, min(bar_h - 1, py))) for px, py in pts]
            if len(set(clipped)) >= 3:
                pygame.draw.polygon(fill_surf, (255, 255, 255, 60), clipped)

        shine = pygame.Surface((fill_w, bar_h // 3), pygame.SRCALPHA)
        for y in range(bar_h // 3):
            alpha = int(80 * (1 - y / (bar_h // 3)))
            pygame.draw.line(shine, (255, 255, 255, alpha), (0, y), (fill_w, y))
        fill_surf.blit(shine, (0, 0))

        mask_surf = pygame.Surface((fill_w, bar_h), pygame.SRCALPHA)
        pygame.draw.rect(mask_surf, (255, 255, 255, 255), (0, 0, fill_w, bar_h), border_radius=12)
        final_fill = pygame.Surface((fill_w, bar_h), pygame.SRCALPHA)
        for x in range(fill_w):
            for y in range(bar_h):
                if mask_surf.get_at((x, y))[3] > 0:
                    final_fill.set_at((x, y), fill_surf.get_at((x, y)))
        surface.blit(final_fill, (bar_x, bar_y))

    pygame.draw.rect(surface, DARK_PINK, inner_bg, 2, border_radius=12)

    pct_text = f"{int(progress * 100)}%"
    pct_surf = font_small.render(pct_text, True, WHITE if progress > 0.5 else DARK_PINK)
    pct_rect = pct_surf.get_rect(center=(SCREEN_W // 2, bar_y + bar_h // 2))
    surface.blit(pct_surf, pct_rect)

    if progress > 0.05:
        edge_x = bar_x + fill_w
        edge_y = bar_y + bar_h // 2
        glow_size = int(8 + math.sin(t * 5) * 3)
        pygame.draw.circle(surface, CANDY_HOT_PINK, (edge_x, edge_y), glow_size)
        pygame.draw.circle(surface, WHITE, (edge_x, edge_y), glow_size - 3)
        pygame.draw.circle(surface, CANDY_PINK, (edge_x, edge_y), glow_size - 5)

# ============================================================
#  PLAY BUTTON
# ============================================================
def draw_play_button(surface, t, hover=False):
    """Draw an animated Play button."""
    btn_w, btn_h = 200, 60
    btn_x = (SCREEN_W - btn_w) // 2
    btn_y = SCREEN_H // 2 + 100

    pulse = math.sin(t * 3) * 5
    btn_rect = pygame.Rect(btn_x - pulse, btn_y - pulse / 2,
                           btn_w + pulse * 2, btn_h + pulse)

    glow_surf = pygame.Surface((btn_w + 40, btn_h + 40), pygame.SRCALPHA)
    glow_alpha = int(60 + math.sin(t * 2) * 30)
    pygame.draw.rect(glow_surf, (*CANDY_HOT_PINK, glow_alpha),
                     (0, 0, btn_w + 40, btn_h + 40), border_radius=35)
    surface.blit(glow_surf, (btn_x - 20, btn_y - 20))

    btn_color = CANDY_HOT_PINK if hover else CANDY_PINK
    shadow_rect = pygame.Rect(btn_rect.x + 3, btn_rect.y + 3, btn_rect.w, btn_rect.h)
    pygame.draw.rect(surface, (150, 40, 80), shadow_rect, border_radius=30)
    pygame.draw.rect(surface, btn_color, btn_rect, border_radius=30)

    shine_rect = pygame.Rect(btn_rect.x + 4, btn_rect.y + 4,
                             btn_rect.w - 8, btn_rect.h // 2 - 4)
    shine_surf = pygame.Surface((shine_rect.w, shine_rect.h), pygame.SRCALPHA)
    pygame.draw.rect(shine_surf, (255, 255, 255, 60),
                     (0, 0, shine_rect.w, shine_rect.h), border_radius=25)
    surface.blit(shine_surf, shine_rect)

    pygame.draw.rect(surface, DARK_PINK, btn_rect, 3, border_radius=30)

    play_surf = font_play.render("▶  P L A Y", True, WHITE)
    play_rect = play_surf.get_rect(center=btn_rect.center)
    surface.blit(play_surf, play_rect)

    for i in range(6):
        angle = t * 2 + i * math.pi / 3
        dist = 60 + math.sin(t * 3 + i) * 10
        sx = btn_rect.centerx + math.cos(angle) * dist * 1.8
        sy = btn_rect.centery + math.sin(angle) * dist * 0.6
        sparkle_alpha = int(abs(math.sin(t * 4 + i * 1.5)) * 200)
        draw_star(surface, int(sx), int(sy), 5,
                  random.choice([CANDY_YELLOW, WHITE, GOLD, CANDY_PINK]), sparkle_alpha)
    return btn_rect

# ============================================================
#  BUBBLE (background decoration)
# ============================================================
class Bubble:
    def __init__(self):
        self.x = random.randint(0, SCREEN_W)
        self.y = random.randint(0, SCREEN_H)
        self.size = random.randint(20, 60)
        self.speed = random.uniform(0.3, 1.0)
        self.alpha = random.randint(15, 40)
        self.color = random.choice([CANDY_PINK, CANDY_LIGHT_PINK, CANDY_LAVENDER, WHITE])
        self.phase = random.uniform(0, math.pi * 2)

    def update(self, dt):
        self.y -= self.speed * dt * 60
        self.x += math.sin(time.time() * 0.5 + self.phase) * 0.3
        if self.y < -self.size:
            self.y = SCREEN_H + self.size
            self.x = random.randint(0, SCREEN_W)

    def draw(self, surface):
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, self.alpha), (self.size, self.size), self.size)
        pygame.draw.circle(s, (*WHITE, self.alpha // 2), (self.size, self.size), self.size, 2)
        pygame.draw.circle(s, (*WHITE, self.alpha),
                           (self.size - self.size // 3, self.size - self.size // 3), self.size // 5)
        surface.blit(s, (int(self.x - self.size), int(self.y - self.size)))

# ============================================================
#  CONFETTI
# ============================================================
class Confetti:
    def __init__(self):
        self.reset(start_top=False)

    def reset(self, start_top=True):
        self.x = random.randint(0, SCREEN_W)
        self.y = random.randint(-50, 0) if start_top else random.randint(0, SCREEN_H)
        self.speed = random.uniform(2, 5)
        self.h_speed = random.uniform(-2, 2)
        self.size_w = random.randint(4, 10)
        self.size_h = random.randint(6, 14)
        self.color = random.choice([CANDY_PINK, CANDY_HOT_PINK, CANDY_YELLOW,
                                     CANDY_MINT, CANDY_LAVENDER, CANDY_ORANGE, GOLD, WHITE])
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-8, 8)
        self.alpha = random.randint(180, 255)

    def update(self, dt):
        self.y += self.speed * dt * 60
        self.x += self.h_speed * dt * 60
        self.rotation += self.rot_speed * dt * 60
        if self.y > SCREEN_H + 20:
            self.reset(start_top=True)

    def draw(self, surface):
        s = pygame.Surface((self.size_w * 2 + 4, self.size_h * 2 + 4), pygame.SRCALPHA)
        pygame.draw.rect(s, (*self.color, self.alpha),
                         (2, 2, self.size_w * 2, self.size_h * 2), border_radius=2)
        rotated = pygame.transform.rotate(s, self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)

# ============================================================
#  SCENE 2: MEADOW - Dog brings a letter
# ============================================================

# --- Cloud for meadow ---
class Cloud:
    def __init__(self, x=None):
        self.x = x if x is not None else random.randint(-100, SCREEN_W + 100)
        self.y = random.randint(30, 180)
        self.speed = random.uniform(0.2, 0.6)
        self.size = random.uniform(0.6, 1.3)
        self.alpha = random.randint(160, 230)

    def update(self, dt):
        self.x += self.speed * dt * 60
        if self.x > SCREEN_W + 150:
            self.x = -150
            self.y = random.randint(30, 180)

    def draw(self, surface):
        s = pygame.Surface((200, 100), pygame.SRCALPHA)
        sz = self.size
        pygame.draw.ellipse(s, (*CLOUD_WHITE, self.alpha), (int(30 * sz), int(30 * sz), int(80 * sz), int(50 * sz)))
        pygame.draw.ellipse(s, (*CLOUD_WHITE, self.alpha), (int(60 * sz), int(15 * sz), int(70 * sz), int(60 * sz)))
        pygame.draw.ellipse(s, (*CLOUD_WHITE, self.alpha), (int(10 * sz), int(40 * sz), int(60 * sz), int(35 * sz)))
        pygame.draw.ellipse(s, (*CLOUD_WHITE, self.alpha), (int(80 * sz), int(35 * sz), int(50 * sz), int(35 * sz)))
        surface.blit(s, (int(self.x), int(self.y)))

# --- Grass flower ---
class GrassFlower:
    def __init__(self):
        self.x = random.randint(20, SCREEN_W - 20)
        self.y = random.randint(SCREEN_H - 200, SCREEN_H - 40)
        self.color = random.choice([CANDY_PINK, CANDY_YELLOW, WHITE, CANDY_LAVENDER, CANDY_RED, CANDY_ORANGE])
        self.size = random.randint(3, 7)
        self.phase = random.uniform(0, math.pi * 2)

    def draw(self, surface, t):
        sway = math.sin(t * 1.5 + self.phase) * 2
        # Stem
        pygame.draw.line(surface, (60, 130, 40), (self.x, self.y), (int(self.x + sway), self.y - self.size * 3), 2)
        # Petals
        fx, fy = int(self.x + sway), self.y - self.size * 3
        for i in range(5):
            angle = i * math.pi * 2 / 5 + t * 0.3
            px = fx + int(math.cos(angle) * self.size)
            py = fy + int(math.sin(angle) * self.size)
            pygame.draw.circle(surface, self.color, (px, py), self.size // 2 + 1)
        pygame.draw.circle(surface, CANDY_YELLOW, (fx, fy), self.size // 2)

# --- Butterfly ---
class Butterfly:
    def __init__(self):
        self.x = random.randint(100, SCREEN_W - 100)
        self.y = random.randint(200, SCREEN_H - 250)
        self.color = random.choice([CANDY_PINK, CANDY_LAVENDER, CANDY_LIGHT_PINK, CANDY_BLUE])
        self.phase = random.uniform(0, math.pi * 2)
        self.speed_x = random.uniform(-0.5, 0.5)
        self.speed_y = random.uniform(-0.3, 0.3)

    def update(self, dt):
        self.x += (self.speed_x + math.sin(time.time() * 2 + self.phase) * 0.5) * dt * 60
        self.y += (self.speed_y + math.cos(time.time() * 1.5 + self.phase) * 0.3) * dt * 60
        if self.x < 50 or self.x > SCREEN_W - 50:
            self.speed_x *= -1
        if self.y < 150 or self.y > SCREEN_H - 250:
            self.speed_y *= -1

    def draw(self, surface, t):
        wing_flap = abs(math.sin(t * 8 + self.phase))
        wing_w = int(10 * wing_flap + 3)
        s = pygame.Surface((30, 20), pygame.SRCALPHA)
        # Left wing
        pygame.draw.ellipse(s, (*self.color, 180), (7 - wing_w, 2, wing_w, 14))
        # Right wing
        pygame.draw.ellipse(s, (*self.color, 180), (17, 2, wing_w, 14))
        # Body
        pygame.draw.rect(s, (80, 50, 30, 220), (13, 4, 3, 12))
        surface.blit(s, (int(self.x) - 15, int(self.y) - 10))

# --- Dog drawing function ---
def draw_dog(surface, cx, cy, scale, t, facing_left=True, has_letter=True):
    """Draw a cute cartoon dog at the given position and scale."""
    s = int(scale)
    if s < 5:
        # Too small, just draw a dot
        pygame.draw.circle(surface, (180, 130, 80), (int(cx), int(cy)), max(2, s))
        return

    flip = -1 if facing_left else 1

    # Shadow
    shadow_w = int(s * 1.2)
    shadow_h = int(s * 0.25)
    shadow_surf = pygame.Surface((shadow_w * 2, shadow_h * 2), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_surf, (0, 0, 0, 40), (0, 0, shadow_w * 2, shadow_h * 2))
    surface.blit(shadow_surf, (int(cx - shadow_w), int(cy + s * 0.4)))

    # Leg animation (walking)
    leg_phase = t * 6
    leg_offsets = [
        math.sin(leg_phase) * s * 0.15,
        math.sin(leg_phase + math.pi) * s * 0.15,
        math.sin(leg_phase + math.pi * 0.5) * s * 0.15,
        math.sin(leg_phase + math.pi * 1.5) * s * 0.15,
    ]

    body_color = (200, 155, 100)
    body_light = (225, 185, 135)
    belly_color = (240, 220, 190)
    nose_color = (60, 40, 30)
    eye_color = (40, 25, 15)
    tongue_color = (255, 120, 130)

    body_bounce = math.sin(t * 6) * s * 0.03

    # Body (ellipse)
    body_w = int(s * 1.2)
    body_h = int(s * 0.7)
    body_y = int(cy - s * 0.1 + body_bounce)
    pygame.draw.ellipse(surface, body_color,
                        (int(cx - body_w // 2), body_y - body_h // 2, body_w, body_h))
    # Belly
    pygame.draw.ellipse(surface, belly_color,
                        (int(cx - body_w // 3), body_y - body_h // 4, int(body_w * 0.65), int(body_h * 0.55)))

    # Legs
    leg_w = max(3, int(s * 0.15))
    leg_h = max(5, int(s * 0.4))
    leg_positions = [
        (cx + flip * s * 0.35, body_y + body_h // 2 - 5),   # front-front
        (cx + flip * s * 0.15, body_y + body_h // 2 - 5),   # front-back
        (cx - flip * s * 0.35, body_y + body_h // 2 - 5),   # back-front
        (cx - flip * s * 0.15, body_y + body_h // 2 - 5),   # back-back
    ]
    for i, (lx, ly) in enumerate(leg_positions):
        foot_y = ly + leg_h + leg_offsets[i]
        pygame.draw.rect(surface, body_color,
                         (int(lx - leg_w // 2), int(ly), leg_w, int(foot_y - ly)),
                         border_radius=max(1, leg_w // 2))
        # Paw
        pygame.draw.ellipse(surface, body_light,
                            (int(lx - leg_w * 0.7), int(foot_y - 3), int(leg_w * 1.4), max(3, int(s * 0.08))))

    # Tail (wagging)
    tail_wag = math.sin(t * 8) * 25
    tail_x = cx - flip * s * 0.55
    tail_y = body_y - body_h * 0.1
    tail_end_x = tail_x - flip * s * 0.3
    tail_end_y = tail_y - s * 0.35 + math.sin(t * 8) * s * 0.1
    pygame.draw.line(surface, body_color,
                     (int(tail_x), int(tail_y)),
                     (int(tail_end_x), int(tail_end_y)),
                     max(3, int(s * 0.1)))
    pygame.draw.circle(surface, body_light, (int(tail_end_x), int(tail_end_y)), max(2, int(s * 0.06)))

    # Head
    head_size = int(s * 0.45)
    head_x = int(cx + flip * s * 0.5)
    head_y = int(body_y - body_h * 0.25 + body_bounce)
    pygame.draw.circle(surface, body_color, (head_x, head_y), head_size)
    pygame.draw.circle(surface, body_light, (head_x + flip * int(head_size * 0.15), head_y + int(head_size * 0.1)),
                       int(head_size * 0.7))

    # Ears
    ear_size = int(s * 0.25)
    ear_droop = math.sin(t * 4) * 3
    # Left ear
    ear1_x = head_x - int(head_size * 0.6)
    ear1_y = head_y - int(head_size * 0.6)
    pygame.draw.ellipse(surface, (170, 120, 70),
                        (ear1_x - ear_size // 2, int(ear1_y + ear_droop), ear_size, int(ear_size * 1.4)))
    # Right ear
    ear2_x = head_x + int(head_size * 0.6)
    ear2_y = head_y - int(head_size * 0.6)
    pygame.draw.ellipse(surface, (170, 120, 70),
                        (ear2_x - ear_size // 2, int(ear2_y + ear_droop), ear_size, int(ear_size * 1.4)))

    # Eyes
    eye_size = max(2, int(s * 0.08))
    eye1_x = head_x + flip * int(head_size * 0.25) - int(head_size * 0.2)
    eye2_x = head_x + flip * int(head_size * 0.25) + int(head_size * 0.2)
    eye_y = head_y - int(head_size * 0.1)
    # White
    pygame.draw.circle(surface, WHITE, (eye1_x, eye_y), eye_size + 2)
    pygame.draw.circle(surface, WHITE, (eye2_x, eye_y), eye_size + 2)
    # Pupil
    pygame.draw.circle(surface, eye_color, (eye1_x + flip * 1, eye_y), eye_size)
    pygame.draw.circle(surface, eye_color, (eye2_x + flip * 1, eye_y), eye_size)
    # Shine
    pygame.draw.circle(surface, WHITE, (eye1_x + flip * 1 - 1, eye_y - 1), max(1, eye_size // 2))
    pygame.draw.circle(surface, WHITE, (eye2_x + flip * 1 - 1, eye_y - 1), max(1, eye_size // 2))

    # Nose
    nose_x = head_x + flip * int(head_size * 0.55)
    nose_y = head_y + int(head_size * 0.15)
    pygame.draw.ellipse(surface, nose_color,
                        (nose_x - max(2, int(s * 0.07)), nose_y - max(1, int(s * 0.04)),
                         max(4, int(s * 0.14)), max(3, int(s * 0.08))))

    # Mouth / tongue
    mouth_x = nose_x - flip * int(s * 0.02)
    mouth_y = nose_y + max(2, int(s * 0.08))
    tongue_out = abs(math.sin(t * 3)) * s * 0.12
    if tongue_out > s * 0.05:
        pygame.draw.ellipse(surface, tongue_color,
                            (int(mouth_x - s * 0.06), int(mouth_y),
                             max(3, int(s * 0.12)), max(3, int(tongue_out))))

    # Letter in mouth
    if has_letter:
        letter_x = nose_x + flip * int(s * 0.1)
        letter_y = nose_y + int(s * 0.12)
        lw = max(8, int(s * 0.35))
        lh = max(5, int(s * 0.22))
        # Envelope
        pygame.draw.rect(surface, ENVELOPE_CREAM,
                         (int(letter_x - lw // 2), int(letter_y - lh // 2), lw, lh))
        pygame.draw.rect(surface, (200, 180, 140),
                         (int(letter_x - lw // 2), int(letter_y - lh // 2), lw, lh), 1)
        # Envelope flap (triangle)
        pygame.draw.polygon(surface, ENVELOPE_FLAP, [
            (int(letter_x - lw // 2), int(letter_y - lh // 2)),
            (int(letter_x + lw // 2), int(letter_y - lh // 2)),
            (int(letter_x), int(letter_y + 1))
        ])
        # Seal
        seal_r = max(2, int(s * 0.04))
        pygame.draw.circle(surface, SEAL_RED, (int(letter_x), int(letter_y - 1)), seal_r)
        # Heart on seal
        if seal_r >= 3:
            pygame.draw.circle(surface, (255, 80, 80), (int(letter_x - 1), int(letter_y - 2)), seal_r // 2)
            pygame.draw.circle(surface, (255, 80, 80), (int(letter_x + 1), int(letter_y - 2)), seal_r // 2)

def draw_meadow_bg(surface, t):
    """Draw a peaceful meadow with blue sky and green grass."""
    # Sky gradient
    for y in range(int(SCREEN_H * 0.6)):
        ratio = y / (SCREEN_H * 0.6)
        r = int(SKY_TOP[0] + (SKY_BOTTOM[0] - SKY_TOP[0]) * ratio)
        g = int(SKY_TOP[1] + (SKY_BOTTOM[1] - SKY_TOP[1]) * ratio)
        b = int(SKY_TOP[2] + (SKY_BOTTOM[2] - SKY_TOP[2]) * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_W, y))

    # Sun
    sun_x, sun_y = 120, 80
    # Sun glow
    glow_size = int(60 + math.sin(t * 0.8) * 8)
    glow_surf = pygame.Surface((glow_size * 4, glow_size * 4), pygame.SRCALPHA)
    for i in range(glow_size, 0, -2):
        alpha = int(40 * (1 - i / glow_size))
        pygame.draw.circle(glow_surf, (*SUN_YELLOW, alpha), (glow_size * 2, glow_size * 2), i * 2)
    surface.blit(glow_surf, (sun_x - glow_size * 2, sun_y - glow_size * 2))
    # Sun rays
    for i in range(12):
        angle = t * 0.3 + i * math.pi / 6
        ray_len = 50 + math.sin(t * 2 + i) * 10
        ex = sun_x + math.cos(angle) * ray_len
        ey = sun_y + math.sin(angle) * ray_len
        pygame.draw.line(surface, (255, 240, 100, 150), (sun_x, sun_y), (int(ex), int(ey)), 2)
    pygame.draw.circle(surface, SUN_YELLOW, (sun_x, sun_y), 35)
    pygame.draw.circle(surface, (255, 245, 150), (sun_x - 8, sun_y - 8), 15)

    # Grass - rolling hills
    grass_y = int(SCREEN_H * 0.55)
    # Background hill
    hill_pts = [(0, SCREEN_H)]
    for x in range(0, SCREEN_W + 10, 5):
        y = grass_y + math.sin(x * 0.005 + 1) * 30 + math.sin(x * 0.01) * 15
        hill_pts.append((x, int(y)))
    hill_pts.append((SCREEN_W, SCREEN_H))
    pygame.draw.polygon(surface, (80, 160, 50), hill_pts)

    # Foreground grass
    grass_pts = [(0, SCREEN_H)]
    for x in range(0, SCREEN_W + 10, 5):
        y = grass_y + 30 + math.sin(x * 0.008 + 2) * 20 + math.sin(x * 0.015) * 10
        grass_pts.append((x, int(y)))
    grass_pts.append((SCREEN_W, SCREEN_H))
    pygame.draw.polygon(surface, GRASS_GREEN, grass_pts)

    # Grass texture / blades
    random.seed(123)
    for _ in range(80):
        gx = random.randint(0, SCREEN_W)
        gy_base = grass_y + 40 + math.sin(gx * 0.008 + 2) * 20 + math.sin(gx * 0.015) * 10
        gy = random.randint(int(gy_base), SCREEN_H - 10)
        blade_h = random.randint(8, 20)
        sway = math.sin(t * 1.2 + gx * 0.02) * 3
        color = random.choice([GRASS_GREEN, GRASS_DARK, GRASS_LIGHT, (90, 170, 55)])
        pygame.draw.line(surface, color, (gx, gy), (int(gx + sway), gy - blade_h), 2)
    random.seed()

    # Dirt path
    path_y = int(SCREEN_H * 0.78)
    for x in range(0, SCREEN_W + 5, 5):
        pw = 40 + math.sin(x * 0.01) * 10
        py = path_y + math.sin(x * 0.005) * 8
        pygame.draw.rect(surface, DIRT_BROWN, (x, int(py - pw // 4), 5, int(pw // 2)))
        pygame.draw.rect(surface, (150, 130, 90), (x, int(py - pw // 4), 5, int(pw // 6)))

def draw_envelope_big(surface, cx, cy, scale, t):
    """Draw a big envelope in front of the screen."""
    ew = int(300 * scale)
    eh = int(200 * scale)
    ex = cx - ew // 2
    ey = cy - eh // 2

    # Shadow
    shadow_s = pygame.Surface((ew + 20, eh + 20), pygame.SRCALPHA)
    pygame.draw.rect(shadow_s, (0, 0, 0, 50), (0, 0, ew + 20, eh + 20), border_radius=10)
    surface.blit(shadow_s, (ex - 5, ey + 5))

    # Envelope body
    pygame.draw.rect(surface, ENVELOPE_CREAM, (ex, ey, ew, eh), border_radius=8)

    # Flap (top triangle)
    pygame.draw.polygon(surface, ENVELOPE_FLAP, [
        (ex, ey), (ex + ew, ey), (cx, cy + int(10 * scale))
    ])
    pygame.draw.polygon(surface, (200, 180, 140), [
        (ex, ey), (ex + ew, ey), (cx, cy + int(10 * scale))
    ], 2)

    # Border
    pygame.draw.rect(surface, (200, 180, 140), (ex, ey, ew, eh), 3, border_radius=8)

    # Inner lines (decorative)
    for i in range(3):
        line_y = cy + int(20 * scale) + i * int(20 * scale)
        if line_y < ey + eh - 20:
            lw = int(ew * 0.5) - i * int(15 * scale)
            pygame.draw.line(surface, (220, 200, 170), (cx - lw // 2, line_y), (cx + lw // 2, line_y), 2)

    # Red wax seal
    seal_r = int(22 * scale)
    seal_cx = cx
    seal_cy = cy - int(5 * scale)
    pygame.draw.circle(surface, SEAL_RED, (seal_cx, seal_cy), seal_r)
    pygame.draw.circle(surface, (240, 70, 70), (seal_cx, seal_cy), seal_r - 3)
    # Heart on seal
    heart_pts = []
    for i in range(100):
        tt = i / 100 * 2 * math.pi
        hx = 16 * math.sin(tt) ** 3
        hy = -(13 * math.cos(tt) - 5 * math.cos(2 * tt) - 2 * math.cos(3 * tt) - math.cos(4 * tt))
        sc = seal_r / 25
        heart_pts.append((int(seal_cx + hx * sc), int(seal_cy + hy * sc)))
    if len(heart_pts) > 2:
        pygame.draw.polygon(surface, (255, 180, 180), heart_pts)

    # Sparkles around seal
    for i in range(6):
        angle = t * 2 + i * math.pi / 3
        dist = seal_r + 8 + math.sin(t * 3 + i) * 4
        sx = seal_cx + int(math.cos(angle) * dist)
        sy = seal_cy + int(math.sin(angle) * dist)
        alpha = int(abs(math.sin(t * 4 + i)) * 200)
        draw_star(surface, sx, sy, 4, GOLD, alpha)

# ============================================================
#  SCENE 3 (Matrix): Matrix Digital Rain - Pink
# ============================================================
class MatrixColumn:
    MESSAGES = [
        "em iu sinh nhat vui ve",
        "anh yeu Chi",
        "Tho oi snvv nha",
        "happy bit tet",
        "ai o si ma"
    ]

    def __init__(self, x):
        self.x = x
        self.chars = []
        self.speed = random.uniform(2, 8)
        self.y = random.randint(-500, 0)
        self.char_height = 20
        self.msg = random.choice(self.MESSAGES)
        self.msg_index = random.randint(0, len(self.msg) - 1)
        self.max_len = random.randint(10, 30)
        self.reset()

    def reset(self):
        self.y = random.randint(-400, -50)
        self.speed = random.uniform(2, 8)
        self.msg = random.choice(self.MESSAGES)
        self.msg_index = random.randint(0, len(self.msg) - 1)
        self.max_len = random.randint(10, 30)
        self.chars = []

    def update(self, dt):
        self.y += self.speed * dt * 60
        # Build character trail
        num_chars = int((self.y + 400) / self.char_height)
        num_chars = min(num_chars, self.max_len)
        self.chars = []
        for i in range(num_chars):
            char_y = self.y - i * self.char_height
            if 0 <= char_y < SCREEN_H:
                idx = (self.msg_index + i) % len(self.msg)
                ch = self.msg[idx]
                # Brightness fades for trailing chars
                brightness = max(0, 1.0 - i / self.max_len)
                self.chars.append((ch, char_y, brightness, i == 0))

        if self.y - self.max_len * self.char_height > SCREEN_H:
            self.reset()

    def draw(self, surface, font):
        for ch, char_y, brightness, is_head in self.chars:
            if is_head:
                # Head character is brightest white-pink
                color = (255, 220, 240)
                alpha = 255
            else:
                # Trailing chars are pink with fading alpha
                r = int(255 * brightness)
                g = int(50 * brightness)
                b = int(120 * brightness)
                color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
                alpha = int(brightness * 255)

            if alpha > 10:
                char_surf = font.render(ch, True, color)
                char_surf.set_alpha(alpha)
                surface.blit(char_surf, (self.x, int(char_y)))

                # Glow for head
                if is_head:
                    glow_s = pygame.Surface((20, 20), pygame.SRCALPHA)
                    pygame.draw.circle(glow_s, (*CANDY_PINK, 40), (10, 10), 10)
                    surface.blit(glow_s, (self.x - 5, int(char_y) - 5))

# ============================================================
#  SCENE 3.5: GIFT BOX IN DARKNESS → 3D ROSE
# ============================================================

# --- Sparkle particle for rose scene ---
class RoseSparkle:
    def __init__(self, cx, cy, radius=0):
        angle = random.uniform(0, math.pi * 2)
        dist = random.uniform(0, radius) if radius > 0 else random.uniform(50, 220)
        self.x = cx + math.cos(angle) * dist
        self.y = cy + math.sin(angle) * dist
        self.vx = math.cos(angle) * random.uniform(0.5, 2.5)
        self.vy = math.sin(angle) * random.uniform(0.5, 2.5) - random.uniform(1, 3)
        self.life = 1.0
        self.decay = random.uniform(0.008, 0.025)
        self.size = random.randint(2, 6)
        self.color = random.choice([
            (255, 215, 0), (255, 255, 200), (255, 180, 230),
            (255, 100, 180), (200, 255, 255), (255, 255, 255)
        ])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.04
        self.life -= self.decay
        return self.life > 0

    def draw(self, surface):
        if self.life <= 0:
            return
        alpha = int(self.life * 255)
        s = pygame.Surface((self.size * 2 + 2, self.size * 2 + 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (self.size + 1, self.size + 1), self.size)
        surface.blit(s, (int(self.x - self.size - 1), int(self.y - self.size - 1)))


def draw_gift_box(surface, cx, cy, size, t, reveal_progress=0.0):
    """Draw an animated colorful gift box emerging from darkness."""
    # Oscillating colors for ribbons and decorations
    rainbow_colors = [
        (255, 80, 80),   (255, 165, 0),  (255, 230, 0),
        (80, 255, 120),  (80, 180, 255), (180, 80, 255),
        (255, 80, 200),
    ]

    bw = int(size * 1.4)   # box width
    bh = int(size * 1.2)   # box height
    lid_h = int(size * 0.35)
    bx = cx - bw // 2
    by = cy - bh // 2

    # Floating bob
    bob = math.sin(t * 2) * 6 * reveal_progress
    by = int(by + bob)

    # ---- SHADOW ----
    shadow_alpha = int(60 * reveal_progress)
    if shadow_alpha > 0:
        sh_s = pygame.Surface((bw + 40, 30), pygame.SRCALPHA)
        pygame.draw.ellipse(sh_s, (0, 0, 0, shadow_alpha), (0, 0, bw + 40, 30))
        surface.blit(sh_s, (bx - 20, cy + bh // 2 + 15))

    # ---- BOX BODY ----
    # Animated gradient body - cycling colors
    color_idx = int(t * 0.8) % len(rainbow_colors)
    box_col1 = rainbow_colors[color_idx]
    box_col2 = rainbow_colors[(color_idx + 2) % len(rainbow_colors)]
    box_col3 = rainbow_colors[(color_idx + 4) % len(rainbow_colors)]

    # Draw box body with vertical color bands
    band_w = bw // 3
    for i, col in enumerate([box_col1, box_col2, box_col3]):
        bnd_x = bx + i * band_w
        bnd_actual_w = band_w if i < 2 else bw - 2 * band_w
        # Make slightly lighter version
        lighter = tuple(min(255, int(c * 1.3)) for c in col)
        box_rect = pygame.Rect(bnd_x, by + lid_h, bnd_actual_w, bh - lid_h)
        pygame.draw.rect(surface, col, box_rect)
        # Shine highlight on top portion
        shine_s = pygame.Surface((bnd_actual_w, (bh - lid_h) // 3), pygame.SRCALPHA)
        for yy in range((bh - lid_h) // 3):
            a = int(60 * (1 - yy / max(1, (bh - lid_h) // 3)))
            pygame.draw.line(shine_s, (255, 255, 255, a), (0, yy), (bnd_actual_w, yy))
        surface.blit(shine_s, (bnd_x, by + lid_h))

    # Box border
    pygame.draw.rect(surface, (255, 255, 255), (bx, by + lid_h, bw, bh - lid_h), 3, border_radius=4)

    # ---- LID ----
    lid_col = rainbow_colors[(color_idx + 1) % len(rainbow_colors)]
    lid_rect = pygame.Rect(bx - 8, by, bw + 16, lid_h)
    pygame.draw.rect(surface, lid_col, lid_rect, border_radius=6)
    pygame.draw.rect(surface, (255, 255, 255), lid_rect, 3, border_radius=6)
    # Lid shine
    lid_shine = pygame.Surface((bw + 16, lid_h // 2), pygame.SRCALPHA)
    for yy in range(lid_h // 2):
        a = int(80 * (1 - yy / max(1, lid_h // 2)))
        pygame.draw.line(lid_shine, (255, 255, 255, a), (0, yy), (bw + 16, yy))
    surface.blit(lid_shine, (bx - 8, by))

    # ---- VERTICAL RIBBON ----
    ribbon_w = int(size * 0.1)
    ribbon_col = rainbow_colors[(color_idx + 3) % len(rainbow_colors)]
    pygame.draw.rect(surface, ribbon_col, (cx - ribbon_w // 2, by, ribbon_w, bh))
    pygame.draw.rect(surface, (255, 255, 255), (cx - ribbon_w // 2, by, ribbon_w, bh), 1)

    # ---- HORIZONTAL RIBBON ----
    pygame.draw.rect(surface, ribbon_col, (bx, by + bh // 2 - ribbon_w // 2, bw, ribbon_w))
    pygame.draw.rect(surface, (255, 255, 255), (bx, by + bh // 2 - ribbon_w // 2, bw, ribbon_w), 1)

    # ---- BOW on top ----
    bow_col = rainbow_colors[(color_idx + 5) % len(rainbow_colors)]
    bow_col2 = rainbow_colors[(color_idx + 6) % len(rainbow_colors)]
    bow_cx, bow_cy = cx, by + 4
    bow_phase = math.sin(t * 3) * 0.1

    # Left loop
    pts_l = []
    for i in range(20):
        angle = math.pi + i * math.pi / 19 + bow_phase
        r = int(size * 0.32)
        pts_l.append((int(bow_cx - r * 0.5 + math.cos(angle) * r * 0.9),
                      int(bow_cy + math.sin(angle) * r * 0.55)))
    if len(pts_l) > 2:
        pygame.draw.polygon(surface, bow_col, pts_l)
        pygame.draw.polygon(surface, (255, 255, 255), pts_l, 2)
    # Right loop
    pts_r = []
    for i in range(20):
        angle = i * math.pi / 19 - bow_phase
        r = int(size * 0.32)
        pts_r.append((int(bow_cx + r * 0.5 + math.cos(angle) * r * 0.9),
                      int(bow_cy + math.sin(angle) * r * 0.55)))
    if len(pts_r) > 2:
        pygame.draw.polygon(surface, bow_col2, pts_r)
        pygame.draw.polygon(surface, (255, 255, 255), pts_r, 2)
    # Bow center knot
    pygame.draw.circle(surface, rainbow_colors[(color_idx + 4) % len(rainbow_colors)], (bow_cx, bow_cy), int(size * 0.1))
    pygame.draw.circle(surface, (255, 255, 255), (bow_cx, bow_cy), int(size * 0.1), 2)

    # ---- STAR DECORATIONS on box ----
    for i in range(6):
        star_angle = i * math.pi / 3 + t * 1.5
        star_r = int(size * 0.38)
        sx = cx + int(math.cos(star_angle) * star_r * 0.65)
        sy = cy + int(math.sin(star_angle) * star_r * 0.4) + lid_h // 2
        star_col = rainbow_colors[(color_idx + i) % len(rainbow_colors)]
        star_alpha = int(abs(math.sin(t * 3 + i)) * 220 + 35)
        draw_star(surface, sx, sy, int(size * 0.08) + 2, star_col, star_alpha)

    # ---- SPARKLE RING around box ----
    for i in range(12):
        sp_angle = i * math.pi / 6 + t * 2
        sp_r = bw * 0.7 + math.sin(t * 4 + i) * 10
        spx = cx + int(math.cos(sp_angle) * sp_r)
        spy = cy + int(math.sin(sp_angle) * sp_r * 0.55)
        sp_col = rainbow_colors[i % len(rainbow_colors)]
        sp_alpha = int(abs(math.sin(t * 5 + i * 0.8)) * 200)
        if sp_alpha > 30:
            draw_star(surface, spx, spy, 4, sp_col, sp_alpha)


def draw_3d_rose(surface, cx, cy, t, scale=1.0, bloom_progress=1.0):
    """Draw a beautiful 3D-style rose with halo and sparkling ring."""
    # Colors
    ROSE_DEEP   = (180, 20, 60)
    ROSE_MID    = (220, 50, 90)
    ROSE_BRIGHT = (255, 100, 130)
    ROSE_LIGHT  = (255, 160, 180)
    ROSE_EDGE   = (255, 200, 210)
    LEAF_DARK   = (30, 100, 40)
    LEAF_MID    = (60, 150, 60)
    LEAF_LIGHT  = (100, 200, 80)

    bp = bloom_progress  # 0→1

    # ---- OUTER HALO / AURA ----
    halo_layers = [
        (int(220 * scale * bp), (255, 120, 160, 8)),
        (int(170 * scale * bp), (255, 150, 180, 14)),
        (int(130 * scale * bp), (255, 180, 200, 20)),
        (int(100 * scale * bp), (255, 200, 220, 28)),
        (int(75 * scale * bp),  (255, 220, 235, 38)),
    ]
    halo_pulse = math.sin(t * 1.5) * 0.12 + 1.0
    for radius, color in halo_layers:
        r_pulsed = int(radius * halo_pulse)
        if r_pulsed > 0:
            h_s = pygame.Surface((r_pulsed * 2 + 4, r_pulsed * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(h_s, color, (r_pulsed + 2, r_pulsed + 2), r_pulsed)
            surface.blit(h_s, (cx - r_pulsed - 2, cy - r_pulsed - 2))

    # ---- STEM ----
    stem_len = int(130 * scale * bp)
    stem_w = max(2, int(8 * scale))
    if stem_len > 5:
        stem_sway = math.sin(t * 1.2) * 6 * scale
        pygame.draw.line(surface, LEAF_DARK,
                         (cx, cy + int(50 * scale)),
                         (int(cx + stem_sway), cy + int(50 * scale) + stem_len), stem_w + 2)
        pygame.draw.line(surface, LEAF_MID,
                         (cx, cy + int(50 * scale)),
                         (int(cx + stem_sway), cy + int(50 * scale) + stem_len), stem_w - 1)

    # ---- LEAVES ----
    leaf_base_y = cy + int(100 * scale * bp)
    leaf_sway = math.sin(t * 1.5) * 4 * scale
    for side in [-1, 1]:
        lx = cx + side * int(30 * scale * bp)
        ly = leaf_base_y
        pts = []
        for i in range(16):
            angle = i * math.pi / 15
            r = int(45 * scale * bp)
            pts.append((int(lx + side * math.cos(angle) * r * 1.1 + leaf_sway),
                        int(ly + math.sin(angle) * r * 0.5)))
        pts += [(lx, ly)]
        if len(pts) > 2:
            pygame.draw.polygon(surface, LEAF_MID, pts)
            pygame.draw.polygon(surface, LEAF_DARK, pts, 2)
        # Leaf vein
        pygame.draw.line(surface, LEAF_LIGHT,
                         (lx, ly),
                         (int(lx + side * 40 * scale * bp + leaf_sway), int(ly - 15 * scale * bp)), 2)

    # ---- PETALS (multiple layers, 3D effect) ----
    petal_layers = [
        # (num_petals, petal_radius, petal_spread_r, color, angle_offset)
        (5, int(70 * scale * bp), int(48 * scale * bp), ROSE_DEEP, 0),
        (6, int(60 * scale * bp), int(38 * scale * bp), ROSE_MID, math.pi / 6),
        (6, int(48 * scale * bp), int(28 * scale * bp), ROSE_BRIGHT, 0),
        (5, int(36 * scale * bp), int(18 * scale * bp), ROSE_LIGHT, math.pi / 5),
        (4, int(24 * scale * bp), int(10 * scale * bp), ROSE_EDGE, math.pi / 8),
    ]

    rose_sway = math.sin(t * 1.3) * 3 * scale

    for num_petals, petal_r, spread_r, col, ang_off in petal_layers:
        if petal_r < 3:
            continue
        for i in range(num_petals):
            base_angle = i * (2 * math.pi / num_petals) + ang_off + t * 0.3
            # Petal center
            pcx = cx + int(math.cos(base_angle) * spread_r + rose_sway)
            pcy = cy + int(math.sin(base_angle) * spread_r * 0.6)

            # Draw elliptical petal
            petal_surf = pygame.Surface((petal_r * 2 + 4, petal_r * 2 + 4), pygame.SRCALPHA)
            # Gradient petal: lighter at tip
            for rr in range(petal_r, 0, -1):
                ratio = rr / petal_r
                pr = min(255, int(col[0] + (255 - col[0]) * (1 - ratio) * 0.5))
                pg = min(255, int(col[1] + (255 - col[1]) * (1 - ratio) * 0.5))
                pb = min(255, int(col[2] + (255 - col[2]) * (1 - ratio) * 0.5))
                pa = int(230 * bp)
                pygame.draw.ellipse(petal_surf, (pr, pg, pb, pa),
                                    (petal_r + 2 - rr, petal_r + 2 - int(rr * 0.6),
                                     rr * 2, int(rr * 1.2)))

            # Rotate petal to face outward
            angle_deg = math.degrees(base_angle) + 90
            rotated_petal = pygame.transform.rotate(petal_surf, -angle_deg)
            rr = rotated_petal.get_rect(center=(pcx, pcy))
            surface.blit(rotated_petal, rr)

    # ---- CENTER BUD ----
    bud_r = int(20 * scale * bp)
    if bud_r > 1:
        for rr in range(bud_r, 0, -1):
            ratio = rr / bud_r
            rc = int(140 + (1 - ratio) * 80)
            gc = int(20 + (1 - ratio) * 20)
            bc = int(50 + (1 - ratio) * 30)
            pygame.draw.circle(surface, (rc, gc, bc), (cx, cy), rr)
        # Center highlight
        pygame.draw.circle(surface, (255, 200, 220), (cx - bud_r // 3, cy - bud_r // 3), bud_r // 4)

    # ---- SPARKLING RING ----
    ring_radius_base = int(90 * scale * bp)
    ring_count = 24
    for i in range(ring_count):
        angle = i * (2 * math.pi / ring_count) + t * 1.8
        # Two rings
        for ring_r_mult in [1.0, 1.35]:
            ring_r = ring_radius_base * ring_r_mult
            sx = cx + int(math.cos(angle) * ring_r)
            sy = cy + int(math.sin(angle) * ring_r * 0.55)
            alpha = int(abs(math.sin(t * 4 + i * 0.5)) * 240 + 15)
            size_sp = random.choice([3, 4, 5]) if bp > 0.8 else 3
            col_sp = random.choice([(255, 215, 0), (255, 255, 200), (255, 180, 220), (200, 255, 255)])
            draw_star(surface, sx, sy, size_sp, col_sp, alpha)

    # ---- SHIMMER / GLITTER ----
    if bp > 0.5:
        glitter_r = int(110 * scale * bp)
        for i in range(18):
            gangle = t * 2.5 + i * math.pi / 9
            gr = glitter_r + math.sin(t * 6 + i) * 20 * scale
            gx = cx + int(math.cos(gangle) * gr)
            gy = cy + int(math.sin(gangle) * gr * 0.5)
            g_alpha = int(abs(math.sin(t * 5 + i * 1.2)) * 180)
            if g_alpha > 20:
                g_s = pygame.Surface((8, 8), pygame.SRCALPHA)
                pygame.draw.circle(g_s, (255, 255, 255, g_alpha), (4, 4), 4)
                surface.blit(g_s, (gx - 4, gy - 4))


def draw_scene_giftbox(surface, t, scene_state, rose_sparkles):
    """
    scene_state dict keys:
      'phase': 'darkness' | 'reveal' | 'open' | 'rose'
      'reveal_t': time when reveal started
      'open_t': time when open started
      'rose_t': time when rose started
      'box_reveal': 0→1 float
      'rose_bloom': 0→1 float
    """
    phase = scene_state.get('phase', 'darkness')
    box_reveal = scene_state.get('box_reveal', 0.0)
    rose_bloom = scene_state.get('rose_bloom', 0.0)
    cx, cy = SCREEN_W // 2, SCREEN_H // 2 - 20

    if phase in ('darkness', 'reveal'):
        # ---- DARK BACKGROUND ----
        # Very dark background with subtle vignette
        surface.fill((5, 2, 8))
        # Subtle nebula glow in center
        glow_alpha = int(30 + math.sin(t * 0.8) * 15)
        for rr in [200, 150, 100, 60]:
            ns = pygame.Surface((rr * 2, rr * 2), pygame.SRCALPHA)
            pygame.draw.circle(ns, (60, 10, 40, glow_alpha // (rr // 40 + 1)), (rr, rr), rr)
            surface.blit(ns, (cx - rr, cy - rr))
        # Floating dust particles
        random.seed(int(t * 3))
        for _ in range(20):
            dx = random.randint(0, SCREEN_W)
            dy = random.randint(0, SCREEN_H)
            da = random.randint(10, 50)
            ds = random.randint(1, 3)
            pygame.draw.circle(surface, (255, 200, 220), (dx, dy), ds)
        random.seed()

        # ---- SPOTLIGHT ----
        spot_alpha = int(box_reveal * 200)
        if spot_alpha > 0:
            for sr in [300, 220, 150, 90]:
                spot_s = pygame.Surface((sr * 2, sr * 2), pygame.SRCALPHA)
                base_a = int((sr / 300) * spot_alpha * 0.3)
                pygame.draw.circle(spot_s, (255, 240, 200, base_a), (sr, sr), sr)
                surface.blit(spot_s, (cx - sr, cy - sr - 20))

        # Draw gift box
        if box_reveal > 0.01:
            # Clip alpha for fade-in
            box_surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            draw_gift_box(box_surf, cx, cy, 120, t, box_reveal)
            box_surf.set_alpha(int(box_reveal * 255))
            surface.blit(box_surf, (0, 0))

        # ---- OPEN BUTTON ----
        if box_reveal >= 1.0:
            btn_w, btn_h = 220, 60
            btn_x = (SCREEN_W - btn_w) // 2
            btn_y = cy + 165
            pulse = math.sin(t * 3) * 5

            # Glow
            gw_s = pygame.Surface((btn_w + 60, btn_h + 60), pygame.SRCALPHA)
            gw_a = int(60 + math.sin(t * 2) * 30)
            pygame.draw.rect(gw_s, (255, 100, 200, gw_a), (0, 0, btn_w + 60, btn_h + 60), border_radius=35)
            surface.blit(gw_s, (btn_x - 30, btn_y - 30))

            # Shadow
            pygame.draw.rect(surface, (100, 20, 60),
                             (btn_x + 3 - pulse, btn_y + 4 - pulse / 2, btn_w + pulse * 2, btn_h + pulse),
                             border_radius=32)
            # Button
            btn_rect = pygame.Rect(btn_x - pulse, btn_y - pulse / 2, btn_w + pulse * 2, btn_h + pulse)
            pygame.draw.rect(surface, CANDY_HOT_PINK, btn_rect, border_radius=32)

            # Shine
            sh_s = pygame.Surface((int(btn_rect.w - 8), btn_rect.h // 2 - 4), pygame.SRCALPHA)
            pygame.draw.rect(sh_s, (255, 255, 255, 55), (0, 0, sh_s.get_width(), sh_s.get_height()), border_radius=26)
            surface.blit(sh_s, (btn_rect.x + 4, btn_rect.y + 4))

            pygame.draw.rect(surface, DARK_PINK, btn_rect, 3, border_radius=32)

            open_font = get_font(30, bold=True)
            open_txt = open_font.render("🎁  Mở quà!", True, WHITE)
            open_txt_rect = open_txt.get_rect(center=btn_rect.center)
            surface.blit(open_txt, open_txt_rect)

            # Sparkles around button
            for i in range(8):
                ang = t * 3 + i * math.pi / 4
                dist = 65 + math.sin(t * 4 + i) * 10
                spx = btn_rect.centerx + int(math.cos(ang) * dist * 1.6)
                spy = btn_rect.centery + int(math.sin(ang) * dist * 0.5)
                sp_alpha = int(abs(math.sin(t * 5 + i)) * 220)
                draw_star(surface, spx, spy, 5,
                          [(255, 215, 0), (255, 255, 200), (255, 150, 220), WHITE][i % 4], sp_alpha)

            scene_state['open_btn_rect'] = btn_rect

    elif phase in ('open', 'rose'):
        # ---- DARK → GLOWING BACKGROUND for rose ----
        # Gradient from dark to deep violet-rose
        for yy in range(SCREEN_H):
            ratio = yy / SCREEN_H
            rr = int(10 + ratio * 20 + rose_bloom * 30)
            gg = int(5 + ratio * 8 + rose_bloom * 10)
            bb = int(20 + ratio * 30 + rose_bloom * 20)
            pygame.draw.line(surface, (rr, gg, bb), (0, yy), (SCREEN_W, yy))

        # Background glow rings
        for i in range(5):
            ring_r = int((80 + i * 50) * rose_bloom)
            if ring_r > 0:
                rn_s = pygame.Surface((ring_r * 2 + 4, ring_r * 2 + 4), pygame.SRCALPHA)
                ra = int(15 + i * 5)
                pygame.draw.circle(rn_s, (255, 80, 150, ra), (ring_r + 2, ring_r + 2), ring_r)
                surface.blit(rn_s, (cx - ring_r - 2, cy - ring_r - 2))

        # Update and draw rose sparkles
        rose_sparkles[:] = [sp for sp in rose_sparkles if sp.update()]
        for sp in rose_sparkles:
            sp.draw(surface)

        # Add new sparkles periodically
        if rose_bloom > 0.3 and random.random() < 0.4:
            rose_sparkles.append(RoseSparkle(cx, cy, int(120 * rose_bloom)))

        # Draw the 3D rose
        draw_3d_rose(surface, cx, cy - 20, t, scale=1.0, bloom_progress=rose_bloom)

        # Title text when rose fully bloomed
        if rose_bloom > 0.7:
            alpha_title = int(min(1.0, (rose_bloom - 0.7) / 0.3) * 255)
            title_font = get_font(42, bold=True)
            title_text = "🌹 Dành Tặng Thùy Chi 🌹"
            # Glow
            glow_col = (255, 120, 180)
            for dx2, dy2 in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                gt = title_font.render(title_text, True, glow_col)
                gt.set_alpha(int(alpha_title * 0.5))
                gr2 = gt.get_rect(center=(SCREEN_W // 2, SCREEN_H - 130 + dx2))
                surface.blit(gt, gr2)
            # Main title
            ts = title_font.render(title_text, True, (255, 200, 220))
            ts.set_alpha(alpha_title)
            tr = ts.get_rect(center=(SCREEN_W // 2, SCREEN_H - 130))
            surface.blit(ts, tr)

            # Sub text
            sub_font = get_font(24)
            sub_txt = sub_font.render("✨ Chúc mừng sinh nhật! ✨", True, (255, 230, 240))
            sub_txt.set_alpha(alpha_title)
            sub_rect = sub_txt.get_rect(center=(SCREEN_W // 2, SCREEN_H - 85))
            surface.blit(sub_txt, sub_rect)

        # Next button when rose fully bloomed
        if rose_bloom >= 1.0:
            btn_w2, btn_h2 = 180, 48
            btn_x2 = (SCREEN_W - btn_w2) // 2
            btn_y2 = SCREEN_H - 55
            pulse2 = math.sin(t * 3) * 3
            nr = pygame.Rect(btn_x2 - pulse2, btn_y2 - pulse2 / 2, btn_w2 + pulse2 * 2, btn_h2 + pulse2)
            pygame.draw.rect(surface, (80, 20, 60), (nr.x + 2, nr.y + 2, nr.w, nr.h), border_radius=24)
            pygame.draw.rect(surface, CANDY_HOT_PINK, nr, border_radius=24)
            pygame.draw.rect(surface, DARK_PINK, nr, 2, border_radius=24)
            nt = get_font(22, bold=True).render("Tiếp theo ▶", True, WHITE)
            ntr = nt.get_rect(center=nr.center)
            surface.blit(nt, ntr)
            scene_state['next_btn_rect'] = nr

    return scene_state


# ============================================================
#  SCENE 4: BIRTHDAY CARD
# ============================================================
def draw_scene_card(surface, t, confetti_list, sparkles, bubbles):
    """Draw the birthday card / message scene."""
    draw_gradient_bg(surface, t)

    for b in bubbles:
        b.update(1/60)
        b.draw(surface)

    for c in confetti_list:
        c.update(1/60)
        c.draw(surface)

    # Central card
    card_w, card_h = 600, 420
    card_x = (SCREEN_W - card_w) // 2
    card_y = (SCREEN_H - card_h) // 2 - 20

    shadow_s = pygame.Surface((card_w + 10, card_h + 10), pygame.SRCALPHA)
    pygame.draw.rect(shadow_s, (100, 30, 60, 60), (0, 0, card_w + 10, card_h + 10), border_radius=20)
    surface.blit(shadow_s, (card_x - 2, card_y + 5))

    card_s = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
    pygame.draw.rect(card_s, (255, 245, 250, 230), (0, 0, card_w, card_h), border_radius=20)
    for i in range(10):
        alpha = 20 - i * 2
        if alpha > 0:
            pygame.draw.rect(card_s, (*CANDY_PINK, alpha),
                             (i, i, card_w - 2 * i, card_h - 2 * i), border_radius=20, width=2)
    surface.blit(card_s, (card_x, card_y))

    pygame.draw.rect(surface, CANDY_HOT_PINK,
                     (card_x, card_y, card_w, card_h), 3, border_radius=20)

    hb_font = get_font(48, bold=True)
    render_candy_text("🎂 Happy Birthday! 🎂", hb_font, t, card_y + 30, surface)

    line_y = card_y + 100
    for x in range(card_x + 40, card_x + card_w - 40, 12):
        color = CANDY_PINK if (x // 12) % 2 == 0 else CANDY_LIGHT_PINK
        pygame.draw.circle(surface, color, (x, line_y), 3)

    messages = [
        "Chúc mừng sinh nhật Thùy Chi!",
        "Chúc bạn luôn vui vẻ, hạnh phúc",
        "và thật nhiều sức khỏe! 💖",
        "",
        "🌻 Mỗi ngày đều tươi đẹp như",
        "những bông hoa hướng dương 🌻"
    ]
    msg_font = get_font(24)
    for i, msg in enumerate(messages):
        if msg:
            delay = i * 0.5
            alpha_factor = min(1.0, max(0, (t - 1 - delay) * 2))
            if alpha_factor > 0:
                msg_surf = msg_font.render(msg, True, DARK_PINK)
                msg_surf.set_alpha(int(alpha_factor * 255))
                msg_rect = msg_surf.get_rect(center=(SCREEN_W // 2, line_y + 35 + i * 35))
                surface.blit(msg_surf, msg_rect)

    bottom_y = card_y + card_h - 50
    for i in range(8):
        cx = card_x + 50 + i * (card_w - 100) // 7
        cy = bottom_y + math.sin(t * 2 + i * 0.8) * 5
        color = [CANDY_PINK, CANDY_YELLOW, CANDY_MINT, CANDY_LAVENDER,
                 CANDY_ORANGE, CANDY_HOT_PINK, CANDY_BLUE, CANDY_CORAL][i]
        pygame.draw.circle(surface, color, (cx, int(cy)), 8)
        pygame.draw.circle(surface, WHITE, (cx, int(cy)), 8, 2)
        pygame.draw.circle(surface, (*WHITE, 150), (cx - 2, int(cy) - 2), 3)

    for s in sparkles:
        s.update(1/60)
        s.draw(surface)

    next_btn_w, next_btn_h = 160, 45
    next_btn_x = (SCREEN_W - next_btn_w) // 2
    next_btn_y = SCREEN_H - 80

    pulse = math.sin(t * 3) * 3
    next_rect = pygame.Rect(next_btn_x - pulse, next_btn_y - pulse / 2,
                             next_btn_w + pulse * 2, next_btn_h + pulse)
    pygame.draw.rect(surface, (150, 40, 80),
                     (next_rect.x + 2, next_rect.y + 2, next_rect.w, next_rect.h), border_radius=22)
    pygame.draw.rect(surface, CANDY_PINK, next_rect, border_radius=22)
    pygame.draw.rect(surface, DARK_PINK, next_rect, 2, border_radius=22)

    next_text = font_loading.render("Tiếp theo ▶", True, WHITE)
    next_text_rect = next_text.get_rect(center=next_rect.center)
    surface.blit(next_text, next_text_rect)

    return next_rect

# ============================================================
#  SCENE 5: FIREWORKS & WISHES
# ============================================================
class Firework:
    def __init__(self):
        self.x = random.randint(100, SCREEN_W - 100)
        self.y = SCREEN_H
        self.target_y = random.randint(100, SCREEN_H // 2)
        self.speed = random.uniform(5, 9)
        self.color = random.choice([CANDY_PINK, CANDY_HOT_PINK, CANDY_YELLOW,
                                     CANDY_MINT, CANDY_LAVENDER, GOLD, CANDY_ORANGE])
        self.exploded = False
        self.particles = []
        self.trail = []

    def update(self, dt):
        if not self.exploded:
            self.trail.append((self.x, self.y))
            if len(self.trail) > 10:
                self.trail.pop(0)
            self.y -= self.speed * dt * 60
            if self.y <= self.target_y:
                self.explode()
        else:
            for p in self.particles:
                p['x'] += p['vx'] * dt * 60
                p['y'] += p['vy'] * dt * 60
                p['vy'] += 0.05 * dt * 60
                p['life'] -= dt * 60
                p['alpha'] = max(0, int(p['life'] / p['max_life'] * 255))
            self.particles = [p for p in self.particles if p['life'] > 0]

    def explode(self):
        self.exploded = True
        for _ in range(random.randint(30, 60)):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 5)
            life = random.uniform(30, 70)
            self.particles.append({
                'x': self.x, 'y': self.y,
                'vx': math.cos(angle) * speed, 'vy': math.sin(angle) * speed,
                'life': life, 'max_life': life, 'alpha': 255,
                'size': random.randint(2, 5), 'color': self.color
            })

    def draw(self, surface):
        if not self.exploded:
            for i, (tx, ty) in enumerate(self.trail):
                alpha = int(i / len(self.trail) * 200)
                s = pygame.Surface((6, 6), pygame.SRCALPHA)
                pygame.draw.circle(s, (*self.color, alpha), (3, 3), 3)
                surface.blit(s, (int(tx - 3), int(ty - 3)))
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 4)
            pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), 2)
        else:
            for p in self.particles:
                if p['alpha'] > 0:
                    s = pygame.Surface((p['size'] * 2, p['size'] * 2), pygame.SRCALPHA)
                    pygame.draw.circle(s, (*p['color'], p['alpha']),
                                       (p['size'], p['size']), p['size'])
                    surface.blit(s, (int(p['x'] - p['size']), int(p['y'] - p['size'])))

    @property
    def done(self):
        return self.exploded and len(self.particles) == 0

def draw_small_heart(surface, cx, cy, size, color, alpha):
    s = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
    pts = []
    for i in range(100):
        t_val = i / 100 * 2 * math.pi
        x = 16 * math.sin(t_val) ** 3
        y = -(13 * math.cos(t_val) - 5 * math.cos(2 * t_val) - 2 * math.cos(3 * t_val) - math.cos(4 * t_val))
        scale = size / 18
        pts.append((int(size * 2 + x * scale), int(size * 2 + y * scale)))
    if len(pts) > 2:
        pygame.draw.polygon(s, (*color, alpha), pts)
    surface.blit(s, (cx - size * 2, cy - size * 2))

def draw_scene_fireworks(surface, t, fireworks):
    """Draw the final celebration scene with fireworks."""
    for y in range(SCREEN_H):
        ratio = y / SCREEN_H
        shift = math.sin(t * 0.2 + ratio) * 5
        r = max(0, min(255, int(40 + ratio * 30 + shift)))
        g = max(0, min(255, int(10 + ratio * 20)))
        b = max(0, min(255, int(60 + ratio * 40 + shift)))
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_W, y))

    random.seed(42)
    for _ in range(50):
        sx = random.randint(0, SCREEN_W)
        sy = random.randint(0, SCREEN_H // 2)
        sa = int(abs(math.sin(t * random.uniform(1, 3) + random.uniform(0, 6))) * 200)
        if sa > 30:
            draw_star(surface, sx, sy, random.randint(2, 4), WHITE, sa)
    random.seed()

    for fw in fireworks:
        fw.update(1/60)
        fw.draw(surface)

    fireworks[:] = [fw for fw in fireworks if not fw.done]
    if random.random() < 0.03:
        fireworks.append(Firework())

    big_font = get_font(56, bold=True)
    render_candy_text("🎉 Chúc Mừng Sinh Nhật! 🎉", big_font, t, SCREEN_H // 2 - 80, surface)

    sub_font = get_font(32, bold=True)
    sub_text = "✨ Thùy Chi ✨"
    sub_surf = sub_font.render(sub_text, True, GOLD)
    glow_factor = abs(math.sin(t * 2))
    sub_glow = sub_font.render(sub_text, True, CANDY_YELLOW)
    sub_glow.set_alpha(int(glow_factor * 100))
    sub_rect = sub_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))
    surface.blit(sub_glow, (sub_rect.x - 2, sub_rect.y - 2))
    surface.blit(sub_surf, sub_rect)

    wish_font = get_font(22)
    wishes = [
        "Chúc bạn một tuổi mới thật xinh đẹp và hạnh phúc!",
        "Mọi ước mơ đều trở thành hiện thực! 🌟",
        "Luôn tỏa sáng như những ngôi sao trên bầu trời! ⭐"
    ]
    for i, wish in enumerate(wishes):
        wave = math.sin(t * 1.5 + i * 0.8) * 3
        wish_surf = wish_font.render(wish, True, CANDY_LIGHT_PINK)
        alpha_val = min(255, int((t - 2 - i * 0.8) * 200))
        if alpha_val > 0:
            wish_surf.set_alpha(min(255, alpha_val))
            wish_rect = wish_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 60 + i * 35 + wave))
            surface.blit(wish_surf, wish_rect)

    for i in range(10):
        hx = SCREEN_W // 2 + math.cos(t * 0.8 + i * math.pi / 5) * (200 + i * 20)
        hy = SCREEN_H // 2 + math.sin(t * 0.6 + i * math.pi / 5) * (100 + i * 10) - 50
        h_alpha = int(abs(math.sin(t + i)) * 150 + 50)
        draw_small_heart(surface, int(hx), int(hy), 8 + i % 4,
                         random.choice([CANDY_PINK, CANDY_HOT_PINK, CANDY_RED]), h_alpha)

    replay_w, replay_h = 160, 45
    replay_x = (SCREEN_W - replay_w) // 2
    replay_y = SCREEN_H - 80

    pulse = math.sin(t * 3) * 3
    replay_rect = pygame.Rect(replay_x - pulse, replay_y - pulse / 2,
                               replay_w + pulse * 2, replay_h + pulse)
    pygame.draw.rect(surface, (80, 20, 60),
                     (replay_rect.x + 2, replay_rect.y + 2, replay_rect.w, replay_rect.h), border_radius=22)
    pygame.draw.rect(surface, CANDY_HOT_PINK, replay_rect, border_radius=22)
    pygame.draw.rect(surface, (200, 80, 150), replay_rect, 2, border_radius=22)

    replay_text = font_loading.render("🔄 Xem lại", True, WHITE)
    replay_text_rect = replay_text.get_rect(center=replay_rect.center)
    surface.blit(replay_text, replay_text_rect)

    return replay_rect

# ============================================================
#  MAIN GAME LOOP
# ============================================================

# Create particles
candies = [Candy() for _ in range(35)]
sunflowers = [Sunflower() for _ in range(12)]
sparkles = [Sparkle() for _ in range(25)]
bubbles = [Bubble() for _ in range(15)]
confetti_list = [Confetti() for _ in range(40)]
fireworks = [Firework() for _ in range(3)]

# Meadow objects
clouds = [Cloud(x=i * 250) for i in range(5)]
grass_flowers = [GrassFlower() for _ in range(30)]
butterflies = [Butterfly() for _ in range(5)]

# Matrix columns
matrix_columns = [MatrixColumn(x * 18) for x in range(SCREEN_W // 18 + 1)]

# ==========================================
#  SCENE FLOW:
#  1 = Loading screen
#  2 = Meadow (dog brings letter)
#  3 = Matrix Digital Rain (pink)
#  4 = Birthday card
#  5 = Fireworks celebration
# ==========================================
current_scene = 1
loading_progress = 0.0
loading_complete = False
scene_start_time = time.time()
play_button_rect = None

# Scene 2 state
dog_progress = 0.0        # 0 = far away, 1 = arrived
dog_arrived = False
letter_scale = 0.0        # grows to 1.0 when dog delivers
letter_delivered = False
open_btn_visible = False

# Scene 3 state
matrix_black_start = 0
matrix_rain_started = False

running = True
while running:
    dt = clock.tick(60) / 1000.0
    t = time.time() - scene_start_time
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_scene == 1 and loading_complete and play_button_rect:
                if play_button_rect.collidepoint(mouse_pos):
                    current_scene = 2
                    scene_start_time = time.time()
                    dog_progress = 0.0
                    dog_arrived = False
                    letter_scale = 0.0
                    letter_delivered = False
                    open_btn_visible = False

            elif current_scene == 2 and open_btn_visible:
                # Check open button click
                btn_w, btn_h = 180, 55
                btn_x = (SCREEN_W - btn_w) // 2
                btn_y = SCREEN_H // 2 + 160
                open_rect = pygame.Rect(btn_x - 5, btn_y - 5, btn_w + 10, btn_h + 10)
                if open_rect.collidepoint(mouse_pos):
                    current_scene = 3
                    scene_start_time = time.time()
                    matrix_black_start = time.time()
                    matrix_rain_started = False
                    # Reset matrix columns
                    matrix_columns = [MatrixColumn(x * 18) for x in range(SCREEN_W // 18 + 1)]

            elif current_scene == 3:
                # After matrix, check for continue button
                if matrix_rain_started and t > 7:
                    btn_w, btn_h = 160, 45
                    btn_x = (SCREEN_W - btn_w) // 2
                    btn_y = SCREEN_H - 70
                    continue_rect = pygame.Rect(btn_x - 5, btn_y - 5, btn_w + 10, btn_h + 10)
                    if continue_rect.collidepoint(mouse_pos):
                        current_scene = 4
                        scene_start_time = time.time()

            elif current_scene == 4:
                next_rect = pygame.Rect((SCREEN_W - 160) // 2 - 3, SCREEN_H - 83, 166, 51)
                if next_rect.collidepoint(mouse_pos):
                    current_scene = 5
                    scene_start_time = time.time()
                    fireworks = [Firework() for _ in range(5)]

            elif current_scene == 5:
                replay_rect = pygame.Rect((SCREEN_W - 160) // 2 - 3, SCREEN_H - 83, 166, 51)
                if replay_rect.collidepoint(mouse_pos):
                    current_scene = 1
                    scene_start_time = time.time()
                    loading_progress = 0.0
                    loading_complete = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # ===================== SCENE 1: LOADING =====================
    if current_scene == 1:
        draw_gradient_bg(screen, t)

        for b in bubbles:
            b.update(dt)
            b.draw(screen)
        for s in sparkles:
            s.update(dt)
            s.draw(screen)
        for c in candies:
            c.update(dt)
            c.draw(screen)
        for sf in sunflowers:
            sf.update(dt)
            sf.draw(screen)

        title_y = SCREEN_H // 2 - 80
        title_bounce = math.sin(t * 2) * 8
        render_candy_text("Sinh nhật Thùy Chi", font_title, t, int(title_y + title_bounce), screen)

        sub = "🌻 Một món quà đặc biệt dành cho bạn 🌻"
        sub_surf = font_subtitle.render(sub, True, DARK_PINK)
        sub_alpha = min(255, int(t * 100))
        sub_surf.set_alpha(sub_alpha)
        sub_rect = sub_surf.get_rect(center=(SCREEN_W // 2, title_y + title_bounce + 80))
        screen.blit(sub_surf, sub_rect)

        if not loading_complete:
            loading_progress += dt * 0.2
            if loading_progress >= 1.0:
                loading_progress = 1.0
                loading_complete = True
            draw_loading_bar(screen, loading_progress, t)
        else:
            hover = False
            btn_test = pygame.Rect((SCREEN_W - 200) // 2 - 5, SCREEN_H // 2 + 95, 210, 70)
            if btn_test.collidepoint(mouse_pos):
                hover = True
            play_button_rect = draw_play_button(screen, t, hover)

    # ===================== SCENE 2: MEADOW + DOG =====================
    elif current_scene == 2:
        draw_meadow_bg(screen, t)

        # Draw clouds
        for cloud in clouds:
            cloud.update(dt)
            cloud.draw(screen)

        # Draw butterflies
        for bf in butterflies:
            bf.update(dt)
            bf.draw(screen, t)

        # Draw grass flowers
        for gf in grass_flowers:
            gf.draw(screen, t)

        # Dog animation
        if not dog_arrived:
            # Dog walks from right (far) to center
            dog_progress += dt * 0.12  # takes ~8 seconds
            if dog_progress >= 1.0:
                dog_progress = 1.0
                dog_arrived = True

            # Dog position: starts far right (small) and walks to center-left (big)
            # Perspective: x goes from right edge to center, scale grows
            dog_x = SCREEN_W - 50 - (SCREEN_W // 2 - 50) * dog_progress
            dog_y_base = SCREEN_H * 0.55 + 60
            dog_scale = 10 + 55 * dog_progress  # starts small, grows big
            # Bobbing
            dog_y = dog_y_base + math.sin(t * 6) * 3 * dog_progress

            draw_dog(screen, dog_x, dog_y, dog_scale, t, facing_left=True, has_letter=True)

        else:
            # Dog arrived, show dog at center
            dog_x = SCREEN_W // 2
            dog_y = SCREEN_H * 0.55 + 60 + math.sin(t * 2) * 2
            dog_scale = 65

            # Animate letter delivery
            if not letter_delivered:
                letter_scale += dt * 0.5  # letter grows over 2 seconds
                if letter_scale >= 1.0:
                    letter_scale = 1.0
                    letter_delivered = True
                    open_btn_visible = True

                # Dog still visible but letter is growing
                draw_dog(screen, dog_x, dog_y, dog_scale, t, facing_left=True,
                         has_letter=(letter_scale < 0.3))

                # Letter growing from dog's mouth to center screen
                env_scale = letter_scale
                env_cx = int(dog_x + (SCREEN_W // 2 - dog_x) * letter_scale)
                env_cy = int(dog_y - 30 + (SCREEN_H // 2 - 30 - (dog_y - 30)) * letter_scale)
                draw_envelope_big(screen, env_cx, env_cy, env_scale, t)

            else:
                # Letter delivered, dog sits happily
                draw_dog(screen, dog_x - 120, dog_y + 10, dog_scale * 0.8, t,
                         facing_left=False, has_letter=False)

                # Big envelope in center
                draw_envelope_big(screen, SCREEN_W // 2, SCREEN_H // 2 - 30, 1.0, t)

                # "MỞ THƯ" button
                btn_w, btn_h = 180, 55
                btn_x = (SCREEN_W - btn_w) // 2
                btn_y = SCREEN_H // 2 + 160

                pulse = math.sin(t * 3) * 4
                btn_rect = pygame.Rect(btn_x - pulse, btn_y - pulse / 2,
                                       btn_w + pulse * 2, btn_h + pulse)

                # Glow
                glow_s = pygame.Surface((btn_w + 30, btn_h + 30), pygame.SRCALPHA)
                glow_a = int(50 + math.sin(t * 2) * 30)
                pygame.draw.rect(glow_s, (*CANDY_HOT_PINK, glow_a),
                                 (0, 0, btn_w + 30, btn_h + 30), border_radius=30)
                screen.blit(glow_s, (btn_x - 15, btn_y - 15))

                # Shadow
                pygame.draw.rect(screen, (150, 40, 80),
                                 (btn_rect.x + 3, btn_rect.y + 3, btn_rect.w, btn_rect.h), border_radius=28)
                # Button
                hover = btn_rect.collidepoint(mouse_pos)
                btn_color = CANDY_HOT_PINK if hover else CANDY_PINK
                pygame.draw.rect(screen, btn_color, btn_rect, border_radius=28)
                pygame.draw.rect(screen, DARK_PINK, btn_rect, 3, border_radius=28)

                # Shine
                shine_r = pygame.Rect(btn_rect.x + 4, btn_rect.y + 4,
                                      btn_rect.w - 8, btn_rect.h // 2 - 4)
                shine_s = pygame.Surface((shine_r.w, shine_r.h), pygame.SRCALPHA)
                pygame.draw.rect(shine_s, (255, 255, 255, 50),
                                 (0, 0, shine_r.w, shine_r.h), border_radius=22)
                screen.blit(shine_s, shine_r)

                # Text
                open_text = font_open_btn.render("💌 Mở thư", True, WHITE)
                open_text_rect = open_text.get_rect(center=btn_rect.center)
                screen.blit(open_text, open_text_rect)

                # Sparkles around button
                for i in range(5):
                    angle = t * 2.5 + i * math.pi / 2.5
                    dist = 55 + math.sin(t * 3 + i) * 8
                    sx = btn_rect.centerx + math.cos(angle) * dist * 1.5
                    sy = btn_rect.centery + math.sin(angle) * dist * 0.5
                    sp_alpha = int(abs(math.sin(t * 4 + i)) * 200)
                    draw_star(screen, int(sx), int(sy), 4, GOLD, sp_alpha)

    # ===================== SCENE 3: MATRIX RAIN =====================
    elif current_scene == 3:
        elapsed_since_black = time.time() - matrix_black_start

        if elapsed_since_black < 5.0:
            # Black screen phase - fade to black with subtle text
            screen.fill(BLACK)

            # Fading "..." text
            if elapsed_since_black > 1.0:
                dots = "." * min(3, int((elapsed_since_black - 1.0) / 0.8) + 1)
                dot_surf = font_subtitle.render(dots, True, (60, 20, 40))
                alpha = min(255, int((elapsed_since_black - 1.0) * 100))
                dot_surf.set_alpha(alpha)
                dot_rect = dot_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))
                screen.blit(dot_surf, dot_rect)

            # Countdown hint at bottom
            remaining = max(0, 5.0 - elapsed_since_black)
            if remaining > 0 and elapsed_since_black > 2:
                hint_surf = font_small.render(f"Đợi chút nha... {remaining:.0f}s", True, (80, 30, 50))
                hint_surf.set_alpha(min(200, int((elapsed_since_black - 2) * 150)))
                hint_rect = hint_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H - 50))
                screen.blit(hint_surf, hint_rect)

        else:
            # Matrix rain phase
            if not matrix_rain_started:
                matrix_rain_started = True

            screen.fill((5, 0, 5))  # Very slight pink tint on black

            # Update and draw matrix columns
            for col in matrix_columns:
                col.update(dt)
                col.draw(screen, font_matrix)

            # Overlay glow effect at random intervals
            if random.random() < 0.05:
                glow_x = random.randint(0, SCREEN_W)
                glow_y = random.randint(0, SCREEN_H)
                glow_s = pygame.Surface((100, 100), pygame.SRCALPHA)
                pygame.draw.circle(glow_s, (*CANDY_PINK, 15), (50, 50), 50)
                screen.blit(glow_s, (glow_x - 50, glow_y - 50))

            # Show the messages clearly in the center after a while
            matrix_elapsed = elapsed_since_black - 5.0

            if matrix_elapsed > 3:
                # Display messages one by one
                center_msgs = [
                    "em iu sinh nhat vui ve",
                    "anh yeu Chi",
                    "Tho oi snvv nha",
                    "happy bit tet",
                    "ai o si ma"
                ]
                msg_font_big = get_font(28, bold=True)
                for i, msg in enumerate(center_msgs):
                    appear_time = 3 + i * 1.2
                    if matrix_elapsed > appear_time:
                        alpha_f = min(1.0, (matrix_elapsed - appear_time) * 0.8)
                        # Glowing text
                        msg_y = SCREEN_H // 2 - 80 + i * 45
                        # Glow behind
                        glow_surf = msg_font_big.render(msg, True, CANDY_HOT_PINK)
                        glow_surf.set_alpha(int(alpha_f * 60))
                        glow_rect = glow_surf.get_rect(center=(SCREEN_W // 2, msg_y))
                        for dx in range(-2, 3):
                            for dy in range(-2, 3):
                                screen.blit(glow_surf, (glow_rect.x + dx, glow_rect.y + dy))
                        # Main text
                        msg_surf = msg_font_big.render(msg, True, CANDY_PINK)
                        msg_surf.set_alpha(int(alpha_f * 255))
                        msg_rect = msg_surf.get_rect(center=(SCREEN_W // 2, msg_y))
                        screen.blit(msg_surf, msg_rect)

            # Continue button after messages appear
            if matrix_elapsed > 10:
                btn_w, btn_h = 160, 45
                btn_x = (SCREEN_W - btn_w) // 2
                btn_y = SCREEN_H - 70

                pulse = math.sin(t * 3) * 3
                c_rect = pygame.Rect(btn_x - pulse, btn_y - pulse / 2,
                                     btn_w + pulse * 2, btn_h + pulse)
                pygame.draw.rect(screen, (60, 10, 30),
                                 (c_rect.x + 2, c_rect.y + 2, c_rect.w, c_rect.h), border_radius=22)
                pygame.draw.rect(screen, CANDY_HOT_PINK, c_rect, border_radius=22)
                pygame.draw.rect(screen, CANDY_PINK, c_rect, 2, border_radius=22)

                cont_text = font_loading.render("Tiếp tục ▶", True, WHITE)
                cont_rect = cont_text.get_rect(center=c_rect.center)
                screen.blit(cont_text, cont_rect)

    # ===================== SCENE 4: BIRTHDAY CARD =====================
    elif current_scene == 4:
        draw_scene_card(screen, t, confetti_list, sparkles, bubbles)

    # ===================== SCENE 5: FIREWORKS =====================
    elif current_scene == 5:
        draw_scene_fireworks(screen, t, fireworks)

    pygame.display.flip()

pygame.quit()
sys.exit()
