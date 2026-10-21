
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
import sys

# --- Khởi tạo ---
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("🌊 Thợ Lặn Đại Dương 3D")
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# --- Camera / Player ---
cam_pos   = [0.0, -2.0, 5.0]
cam_yaw   = 0.0
cam_pitch = 0.0
SPEED     = 0.08
MOUSE_SEN = 0.15

# --- Màu sắc ---
CORAL_COLORS = [
    (1.0, 0.2, 0.5), (1.0, 0.6, 0.0), (0.3, 0.9, 0.6),
    (0.9, 0.1, 0.9), (0.2, 0.7, 1.0), (1.0, 0.8, 0.1),
]
FISH_COLORS = [
    (1.0, 0.3, 0.0), (0.9, 0.9, 0.0), (0.0, 1.0, 0.5),
    (1.0, 0.1, 0.5), (0.3, 0.5, 1.0), (0.8, 0.2, 1.0),
]

# ===================== SINH VẬT =====================

def rand_range(a, b): return random.uniform(a, b)

# --- San hô ---
corals = []
for _ in range(60):
    x = rand_range(-30, 30)
    z = rand_range(-30, 30)
    col = random.choice(CORAL_COLORS)
    h   = rand_range(0.5, 2.5)
    r   = rand_range(0.15, 0.4)
    kind= random.choice(['tube', 'fan', 'brain'])
    corals.append({'pos': [x, -5.0, z], 'color': col, 'h': h, 'r': r, 'kind': kind})

# --- Cá ---
fishes = []
for _ in range(40):
    fishes.append({
        'pos':   [rand_range(-25,25), rand_range(-4,-0.5), rand_range(-25,25)],
        'color': random.choice(FISH_COLORS),
        'color2': random.choice(FISH_COLORS),
        'speed': rand_range(0.01, 0.04),
        'angle': rand_range(0, 360),
        'radius': rand_range(2, 6),
        'center': [rand_range(-20,20), rand_range(-4,-0.5), rand_range(-20,20)],
        'bob_phase': rand_range(0, 6.28),
        'scale':  rand_range(0.25, 0.55),
    })

# --- Cá voi xanh ---
whale = {
    'pos':   [0.0, -1.5, -15.0],
    'angle': 0.0,
    'speed': 0.005,
    'radius': 18.0,
    'center': [0, -1.5, 0],
}

# --- Bong bóng ---
bubbles = []
for _ in range(80):
    bubbles.append({
        'pos':  [rand_range(-25,25), rand_range(-5,2), rand_range(-25,25)],
        'speed': rand_range(0.005, 0.02),
        'r':    rand_range(0.03, 0.12),
    })

# ===================== HÀM VẼ =====================

quad  = gluNewQuadric()
gluQuadricNormals(quad, GLU_SMOOTH)

def set_color(r,g,b,a=1.0):
    glColor4f(r,g,b,a)

def draw_sphere(r, slices=12, stacks=8):
    gluSphere(quad, r, slices, stacks)

def draw_cylinder(r, h, slices=10):
    gluCylinder(quad, r, r*0.5, h, slices, 2)

def draw_coral(c):
    glPushMatrix()
    glTranslatef(*c['pos'])
    set_color(*c['color'])
    if c['kind'] == 'tube':
        draw_cylinder(c['r'], c['h'])
        glTranslatef(0,0,c['h'])
        draw_sphere(c['r']*1.3)
    elif c['kind'] == 'fan':
        # vẽ nhiều nhánh quạt
        for i in range(5):
            glPushMatrix()
            glRotatef(i*36, 0,0,1)
            draw_cylinder(c['r']*0.6, c['h'])
            glTranslatef(0,0,c['h'])
            draw_sphere(c['r'])
            glPopMatrix()
    else:  # brain
        draw_sphere(c['r']*1.5)
        set_color(c['color'][0]*0.7, c['color'][1]*0.7, c['color'][2]*0.7)
        glScalef(1.4, 0.7, 1.4)
        draw_sphere(c['r'])
    glPopMatrix()

def draw_fish(f, t):
    glPushMatrix()
    px, py, pz = f['pos']
    bob = math.sin(t*2 + f['bob_phase']) * 0.15
    glTranslatef(px, py+bob, pz)
    glRotatef(-f['angle'], 0, 1, 0)
    s = f['scale']
    glScalef(s, s, s)

    # Thân cá
    set_color(*f['color'])
    glScalef(1.6, 0.7, 0.7)
    draw_sphere(0.3)
    glScalef(1/1.6, 1/0.7, 1/0.7)

    # Đầu
    set_color(f['color'][0]*0.8, f['color'][1]*0.8, f['color'][2]*0.8)
    glTranslatef(0.4, 0, 0)
    draw_sphere(0.22)
    glTranslatef(-0.4, 0, 0)

    # Đuôi
    set_color(*f['color2'])
    glTranslatef(-0.5, 0, 0)
    glScalef(0.5, 1.0, 1.0)
    draw_sphere(0.2)
    glScalef(2, 1, 1)
    glTranslatef(0.5, 0, 0)

    # Vây lưng
    set_color(f['color2'][0], f['color2'][1]*0.8, 0.2)
    glTranslatef(0.0, 0.25, 0)
    glScalef(0.3, 0.6, 0.15)
    draw_sphere(0.25)
    glScalef(1/0.3, 1/0.6, 1/0.15)
    glTranslatef(0, -0.25, 0)

    # Sọc trang trí
    set_color(1.0, 1.0, 1.0)
    glTranslatef(0.0, 0, 0)
    glScalef(0.15, 0.8, 0.8)
    draw_sphere(0.3)

    glPopMatrix()

def draw_whale(w, t):
    glPushMatrix()
    glTranslatef(*w['pos'])
    glRotatef(-w['angle'], 0, 1, 0)

    # Thân cá voi
    set_color(0.2, 0.4, 0.9)
    glScalef(4.0, 1.2, 1.5)
    draw_sphere(1.0)
    glScalef(1/4.0, 1/1.2, 1/1.5)

    # Bụng trắng
    set_color(0.85, 0.95, 1.0)
    glTranslatef(0, -0.7, 0)
    glScalef(3.5, 0.5, 1.0)
    draw_sphere(0.9)
    glScalef(1/3.5, 1/0.5, 1/1.0)
    glTranslatef(0, 0.7, 0)

    # Đầu
    set_color(0.15, 0.35, 0.8)
    glTranslatef(3.5, 0, 0)
    glScalef(1.2, 0.9, 1.0)
    draw_sphere(0.9)
    glScalef(1/1.2, 1/0.9, 1)
    glTranslatef(-3.5, 0, 0)

    # Đuôi
    set_color(0.1, 0.3, 0.75)
    glTranslatef(-4.5, 0, 0)
    bob_tail = math.sin(t*0.8)*0.3
    glRotatef(bob_tail*20, 0, 0, 1)
    glScalef(1.5, 0.4, 1.8)
    draw_sphere(0.7)
    glScalef(1/1.5, 1/0.4, 1/1.8)
    glTranslatef(4.5, 0, 0)

    # Vây ngực trái
    set_color(0.2, 0.5, 0.95)
    glTranslatef(1.0, -0.8, 1.2)
    glRotatef(-30, 1, 0, 0)
    glScalef(1.5, 0.2, 0.6)
    draw_sphere(0.5)
    glScalef(1/1.5, 1/0.2, 1/0.6)
    glTranslatef(-1.0, 0.8, -1.2)

    # Vây ngực phải
    glTranslatef(1.0, -0.8, -1.2)
    glRotatef(30, 1, 0, 0)
    glScalef(1.5, 0.2, 0.6)
    draw_sphere(0.5)

    glPopMatrix()

def draw_bubbles():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    for b in bubbles:
        glPushMatrix()
        glTranslatef(*b['pos'])
        set_color(0.7, 0.9, 1.0, 0.35)
        draw_sphere(b['r'], 8, 6)
        set_color(1.0, 1.0, 1.0, 0.15)
        draw_sphere(b['r']*0.7, 8, 6)
        glPopMatrix()
    glDisable(GL_BLEND)

def draw_seabed():
    glBegin(GL_QUADS)
    N = 20
    for ix in range(-N, N):
        for iz in range(-N, N):
            nx = (ix+N)/(2*N)
            nz = (iz+N)/(2*N)
            r = 0.55 + 0.15*math.sin(ix*0.5)*math.cos(iz*0.4)
            g = 0.4 + 0.1*nx
            b2= 0.25
            set_color(r, g, b2)
            y = -5.0 + 0.3*math.sin(ix*0.7)*math.cos(iz*0.5)
            glVertex3f(ix*1.5, y, iz*1.5)
            glVertex3f((ix+1)*1.5, y, iz*1.5)
            glVertex3f((ix+1)*1.5, y, (iz+1)*1.5)
            glVertex3f(ix*1.5, y, (iz+1)*1.5)
    glEnd()

def draw_water_surface():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    set_color(0.0, 0.4, 0.9, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(-50, 2, -50)
    glVertex3f( 50, 2, -50)
    glVertex3f( 50, 2,  50)
    glVertex3f(-50, 2,  50)
    glEnd()
    glDisable(GL_BLEND)

def draw_particles(t):
    """Hạt phù du nhỏ lơ lửng"""
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    random.seed(42)
    for i in range(120):
        x = random.uniform(-25, 25)
        y = random.uniform(-5, 2) + math.sin(t + i)*0.3
        z = random.uniform(-25, 25)
        r = random.uniform(0.02, 0.06)
        cr = random.uniform(0.6,1.0)
        cg = random.uniform(0.8,1.0)
        cb = random.uniform(0.9,1.0)
        glPushMatrix()
        glTranslatef(x, y, z)
        set_color(cr, cg, cb, 0.5)
        draw_sphere(r, 5, 4)
        glPopMatrix()
    random.seed()
    glDisable(GL_BLEND)

# ===================== OPENGL SETUP =====================

def setup_gl():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glShadeModel(GL_SMOOTH)

    # Ánh sáng mặt trời chiếu xuống nước
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 10.0, 0.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [0.6, 0.85, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.15, 0.35, 0.55, 1.0])

    # Ánh sáng phụ màu xanh dưới nước
    glLightfv(GL_LIGHT1, GL_POSITION, [5.0, -2.0, 5.0, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE,  [0.2, 0.5, 0.8, 1.0])
    glLightfv(GL_LIGHT1, GL_AMBIENT,  [0.05, 0.1, 0.2, 1.0])

    glFogi = GL_FOG
    glEnable(GL_FOG)
    glFogfv(GL_FOG_COLOR, [0.0, 0.2, 0.55, 1.0])
    glFogf(GL_FOG_DENSITY, 0.025)
    glFogf(GL_FOG_START, 10.0)
    glFogf(GL_FOG_END, 45.0)
    glFogi(GL_FOG_MODE, GL_EXP2)

    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, WIDTH/HEIGHT, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# ===================== CAMERA =====================

def apply_camera():
    glLoadIdentity()
    glRotatef(cam_pitch, 1, 0, 0)
    glRotatef(cam_yaw,   0, 1, 0)
    glTranslatef(-cam_pos[0], -cam_pos[1], -cam_pos[2])

def get_forward():
    yaw_r   = math.radians(cam_yaw)
    pitch_r = math.radians(cam_pitch)
    fx = -math.sin(yaw_r) * math.cos(pitch_r)
    fy =  math.sin(pitch_r)
    fz = -math.cos(yaw_r) * math.cos(pitch_r)
    return fx, fy, fz

def get_right():
    yaw_r = math.radians(cam_yaw)
    return math.cos(yaw_r), 0, -math.sin(yaw_r)

# ===================== UPDATE =====================

def update(t, dt):
    global cam_yaw, cam_pitch

    # Mouse look
    mx, my = pygame.mouse.get_rel()
    cam_yaw   += mx * MOUSE_SEN
    cam_pitch += my * MOUSE_SEN
    cam_pitch  = max(-80, min(80, cam_pitch))

    # WASD
    keys = pygame.key.get_pressed()
    fx, fy, fz = get_forward()
    rx, ry, rz = get_right()
    if keys[K_w]:
        cam_pos[0] += fx*SPEED; cam_pos[1] += fy*SPEED; cam_pos[2] += fz*SPEED
    if keys[K_s]:
        cam_pos[0] -= fx*SPEED; cam_pos[1] -= fy*SPEED; cam_pos[2] -= fz*SPEED
    if keys[K_d]:
        cam_pos[0] += rx*SPEED; cam_pos[2] += rz*SPEED
    if keys[K_a]:
        cam_pos[0] -= rx*SPEED; cam_pos[2] -= rz*SPEED

    # Giới hạn vùng chơi
    cam_pos[0] = max(-28, min(28, cam_pos[0]))
    cam_pos[1] = max(-4.5, min(1.5, cam_pos[1]))
    cam_pos[2] = max(-28, min(28, cam_pos[2]))

    # Cập nhật cá
    for f in fishes:
        f['angle'] += f['speed'] * 60
        rad = math.radians(f['angle'])
        f['pos'][0] = f['center'][0] + math.cos(rad) * f['radius']
        f['pos'][2] = f['center'][2] + math.sin(rad) * f['radius']
        f['pos'][1] = f['center'][1] + math.sin(t*1.5 + f['bob_phase']) * 0.2

    # Cập nhật cá voi
    whale['angle'] += whale['speed'] * 60 * dt
    rad = math.radians(whale['angle'])
    whale['pos'][0] = whale['center'][0] + math.cos(rad) * whale['radius']
    whale['pos'][2] = whale['center'][2] + math.sin(rad) * whale['radius']
    whale['pos'][1] = whale['center'][1] + math.sin(t*0.3) * 0.5

    # Bong bóng nổi lên
    for b in bubbles:
        b['pos'][1] += b['speed']
        if b['pos'][1] > 2.5:
            b['pos'][1] = -5.0
            b['pos'][0] = rand_range(-25, 25)
            b['pos'][2] = rand_range(-25, 25)

# ===================== MAIN LOOP =====================

def main():
    setup_gl()
    clock = pygame.time.Clock()
    font  = pygame.font.SysFont('Arial', 18)
    t = 0.0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        t += dt

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        update(t, dt)

        # --- Vẽ cảnh ---
        glClearColor(0.0, 0.15, 0.45, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        apply_camera()

        draw_seabed()
        draw_water_surface()

        for c in corals:
            draw_coral(c)

        for f in fishes:
            draw_fish(f, t)

        draw_whale(whale, t)
        draw_bubbles()
        draw_particles(t)

        pygame.display.flip()

        # HUD (vẽ chữ 2D lên màn hình)
        # Chuyển sang 2D tạm thời để vẽ text
        # (dùng pygame overlay)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
