# -*- coding: utf-8 -*-
"""
TOP-DOWN 2D SHOOTER SIMULATION
Controls:
  WASD       - Move
  Mouse      - Aim (360 deg rotation)
  LMB        - Fire (hold for auto with Rifle)
  R          - Manual reload
  1/2/3      - Switch weapon (Pistol/Shotgun/Rifle)
  F          - Toggle Fog of War (Raycasting)
  TAB        - Stats overlay
  ESC        - Quit
"""

import pygame, math, random, sys
from dataclasses import dataclass
from typing import List, Tuple

WIDTH, HEIGHT = 1200, 700
FPS = 60
TILE = 40

C_BG=(18,20,30)
C_WALL=(45,50,75)
C_WALL_LIT=(70,80,120)
C_FLOOR=(28,32,45)
C_FLOOR2=(32,36,52)
C_FOG=(10,12,18)
C_PLAYER=(80,200,255)
C_PLAYER2=(40,120,200)
C_GUN=(200,210,220)
C_ENEMY=(220,80,80)
C_ENEMY2=(160,40,40)
C_BULLET=(255,230,80)
C_BULLET_SG=(255,160,40)
C_BULLET_RF=(120,255,180)
C_HIT=(255,100,50)
C_HP_BAR=(60,220,100)
C_HP_LOW=(220,60,60)
C_AMMO=(80,180,255)
C_RELOAD=(255,180,40)
C_WHITE=(255,255,255)
C_GRAY=(120,130,150)
C_CROSSHAIR=(255,80,80)

@dataclass
class WeaponDef:
    name:str
    damage:float
    bullet_speed:float
    spread:float
    pellets:int
    fire_rate:float
    mag_size:int
    reload_time:float
    bullet_color:tuple
    bullet_radius:int
    auto:bool

WEAPONS = {
    'pistol':  WeaponDef('Pistol',  25, 600, 0.04, 1,  3,   12, 1.5, C_BULLET,    4, False),
    'shotgun': WeaponDef('Shotgun', 18, 450, 0.18, 7,  1.2,  6, 2.2, C_BULLET_SG, 3, False),
    'rifle':   WeaponDef('Rifle',   15, 900, 0.02, 1, 12,   30, 2.0, C_BULLET_RF, 3, True),
}

RAW_MAP = [
    '##############################',
    '#............#.......#........#',
    '#............#.......#........#',
    '#....####....#.......#........#',
    '#....#..#................#....#',
    '#....#..#####....#.......#....#',
    '#....#...............#...#....#',
    '#....#########.......#...#....#',
    '#.................#..#...#....#',
    '#.....#.....#....#...#...#....#',
    '#.....#.....#....#.......#....#',
    '#.....#.....##########...#....#',
    '#.....#..................#....#',
    '#.....##########.............#',
    '#.................................#',
    '#.........#.....#.....#.......#',
    '##############################',
]

class GameMap:
    def __init__(self):
        self.grid=[]
        self.walls=[]
        for ri,row in enumerate(RAW_MAP):
            r=[]
            for ci,ch in enumerate(row):
                v=1 if ch=='#' else 0
                r.append(v)
                if v==1: self.walls.append(pygame.Rect(ci*TILE,ri*TILE,TILE,TILE))
            self.grid.append(r)
        self.rows=len(self.grid)
        self.cols=max(len(r) for r in self.grid)
        self.pixel_w=self.cols*TILE
        self.pixel_h=self.rows*TILE

    def is_wall(self,x,y):
        col=int(x//TILE); row=int(y//TILE)
        if row<0 or row>=self.rows or col<0: return True
        if col>=len(self.grid[row]): return True
        return self.grid[row][col]==1

    def draw(self,surf,cam_x,cam_y):
        sc=max(0,int(cam_x//TILE)); ec=min(self.cols,sc+WIDTH//TILE+2)
        sr=max(0,int(cam_y//TILE)); er=min(self.rows,sr+HEIGHT//TILE+2)
        for row in range(sr,er):
            for col in range(sc,ec):
                if col>=len(self.grid[row]): continue
                rx=col*TILE-cam_x; ry=row*TILE-cam_y
                if self.grid[row][col]==1:
                    pygame.draw.rect(surf,C_WALL,(rx,ry,TILE,TILE))
                    pygame.draw.rect(surf,C_WALL_LIT,(rx,ry,TILE,TILE),1)
                else:
                    c=C_FLOOR if (row+col)%2==0 else C_FLOOR2
                    pygame.draw.rect(surf,c,(rx,ry,TILE,TILE))

def cast_ray(gmap,ox,oy,angle,max_dist=600):
    dx=math.cos(angle); dy=math.sin(angle)
    step=4.0; dist=0.0; x,y=ox,oy
    while dist<max_dist:
        x+=dx*step; y+=dy*step; dist+=step
        if gmap.is_wall(x,y): break
    return x,y

def build_vis_poly(gmap,ox,oy,num=180):
    pts=[]
    for i in range(num):
        a=(2*math.pi*i)/num
        ex,ey=cast_ray(gmap,ox,oy,a)
        pts.append((ex,ey))
    return pts

class Particle:
    def __init__(self,x,y,vx,vy,color,life=0.4,radius=3):
        self.x=x; self.y=y; self.vx=vx; self.vy=vy
        self.color=color; self.life=life; self.max_life=life; self.radius=radius
    def update(self,dt):
        self.x+=self.vx*dt; self.y+=self.vy*dt; self.vy+=200*dt; self.life-=dt
    def draw(self,surf,cam_x,cam_y):
        if self.life<=0: return
        a=self.life/self.max_life; r=int(self.radius*a)
        if r<1: return
        c=tuple(int(v*a) for v in self.color[:3])
        pygame.draw.circle(surf,c,(int(self.x-cam_x),int(self.y-cam_y)),r)

class Bullet:
    def __init__(self,x,y,angle,wdef):
        sp=random.uniform(-wdef.spread,wdef.spread); a=angle+sp
        self.pos=pygame.math.Vector2(x,y)
        self.vel=pygame.math.Vector2(math.cos(a)*wdef.bullet_speed,math.sin(a)*wdef.bullet_speed)
        self.damage=wdef.damage; self.color=wdef.bullet_color
        self.radius=wdef.bullet_radius; self.alive=True; self.trail=[]
    def update(self,dt,gmap):
        self.trail.append((self.pos.x,self.pos.y))
        if len(self.trail)>8: self.trail.pop(0)
        self.pos+=self.vel*dt
        if gmap.is_wall(self.pos.x,self.pos.y): self.alive=False
    def draw(self,surf,cam_x,cam_y):
        for i,(tx,ty) in enumerate(self.trail):
            al=(i+1)/len(self.trail); r=max(1,int(self.radius*al*0.7))
            c=tuple(int(v*al*0.5) for v in self.color)
            pygame.draw.circle(surf,c,(int(tx-cam_x),int(ty-cam_y)),r)
        pygame.draw.circle(surf,self.color,(int(self.pos.x-cam_x),int(self.pos.y-cam_y)),self.radius)
        gs=pygame.Surface((self.radius*4,self.radius*4),pygame.SRCALPHA)
        pygame.draw.circle(gs,(*self.color,60),(self.radius*2,self.radius*2),self.radius*2)
        surf.blit(gs,(int(self.pos.x-cam_x-self.radius*2),int(self.pos.y-cam_y-self.radius*2)))

class Weapon:
    def __init__(self,key):
        self.key=key; self.wdef=WEAPONS[key]
        self.ammo=self.wdef.mag_size; self.reload_timer=0.0
        self.fire_timer=0.0; self.reloading=False; self.muzzle_flash=0.0

    @property
    def fire_interval(self): return 1.0/self.wdef.fire_rate

    def can_fire(self): return not self.reloading and self.ammo>0 and self.fire_timer<=0

    def fire(self,px,py,angle):
        if not self.can_fire():
            if self.ammo==0 and not self.reloading: self.start_reload()
            return []
        self.ammo-=1; self.fire_timer=self.fire_interval; self.muzzle_flash=0.08
        bs=[Bullet(px,py,angle,self.wdef) for _ in range(self.wdef.pellets)]
        if self.ammo==0: self.start_reload()
        return bs

    def start_reload(self):
        if not self.reloading and self.ammo<self.wdef.mag_size:
            self.reloading=True; self.reload_timer=self.wdef.reload_time

    def update(self,dt):
        if self.fire_timer>0: self.fire_timer-=dt
        if self.muzzle_flash>0: self.muzzle_flash-=dt
        if self.reloading:
            self.reload_timer-=dt
            if self.reload_timer<=0: self.ammo=self.wdef.mag_size; self.reloading=False

class Player:
    RADIUS=14; SPEED=180.0
    def __init__(self,x,y):
        self.pos=pygame.math.Vector2(x,y); self.angle=0.0
        self.hp=100; self.max_hp=100
        self.weapons={'pistol':Weapon('pistol'),'shotgun':Weapon('shotgun'),'rifle':Weapon('rifle')}
        self.active_weapon='pistol'
        self.kills=0; self.shots_fired=0; self.shots_hit=0

    @property
    def weapon(self): return self.weapons[self.active_weapon]

    def switch_weapon(self,key):
        if key in self.weapons: self.active_weapon=key

    def aim_at(self,mx,my,cam_x,cam_y):
        wx=mx+cam_x; wy=my+cam_y
        self.angle=math.atan2(wy-self.pos.y,wx-self.pos.x)

    def try_move(self,dx,dy,gmap):
        r=self.RADIUS; nx=self.pos.x+dx; ny=self.pos.y+dy
        if not (gmap.is_wall(nx-r,self.pos.y) or gmap.is_wall(nx+r,self.pos.y) or
                gmap.is_wall(nx,self.pos.y-r) or gmap.is_wall(nx,self.pos.y+r)):
            self.pos.x=nx
        if not (gmap.is_wall(self.pos.x,ny-r) or gmap.is_wall(self.pos.x,ny+r) or
                gmap.is_wall(self.pos.x-r,ny) or gmap.is_wall(self.pos.x+r,ny)):
            self.pos.y=ny

    def update(self,dt,keys,gmap):
        mv=pygame.math.Vector2(0,0)
        if keys[pygame.K_w] or keys[pygame.K_UP]: mv.y-=1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: mv.y+=1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: mv.x-=1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: mv.x+=1
        if mv.length()>0: mv=mv.normalize()*self.SPEED*dt; self.try_move(mv.x,mv.y,gmap)
        for w in self.weapons.values(): w.update(dt)

    def draw(self,surf,cam_x,cam_y):
        sx=int(self.pos.x-cam_x); sy=int(self.pos.y-cam_y)
        shadow=pygame.Surface((self.RADIUS*2+4,self.RADIUS*2+4),pygame.SRCALPHA)
        pygame.draw.circle(shadow,(0,0,0,60),(self.RADIUS+2,self.RADIUS+5),self.RADIUS)
        surf.blit(shadow,(sx-self.RADIUS-2,sy-self.RADIUS-2))
        pygame.draw.circle(surf,C_PLAYER2,(sx,sy),self.RADIUS)
        pygame.draw.circle(surf,C_PLAYER,(sx,sy),self.RADIUS-3)
        pygame.draw.circle(surf,C_WHITE,(sx,sy),self.RADIUS,2)
        gl=self.RADIUS+12
        gx=sx+math.cos(self.angle)*gl; gy=sy+math.sin(self.angle)*gl
        pygame.draw.line(surf,C_GUN,(sx,sy),(int(gx),int(gy)),5)
        pygame.draw.line(surf,C_WHITE,(sx,sy),(int(gx),int(gy)),2)
        if self.weapon.muzzle_flash>0:
            flx=sx+math.cos(self.angle)*(gl+8); fly=sy+math.sin(self.angle)*(gl+8)
            fl=pygame.Surface((30,30),pygame.SRCALPHA)
            pygame.draw.circle(fl,(255,230,100,180),(15,15),12)
            pygame.draw.circle(fl,(255,255,200,220),(15,15),6)
            surf.blit(fl,(int(flx)-15,int(fly)-15))

class Enemy:
    RADIUS=13; SPEED_PATROL=60.0; SPEED_CHASE=100.0
    DETECT_RANGE=280.0; ATTACK_RANGE=250.0; FIRE_INTERVAL=1.5; BULLET_SPEED=320.0

    def __init__(self,x,y):
        self.pos=pygame.math.Vector2(x,y); self.hp=60; self.max_hp=60
        self.angle=0.0; self.alive=True; self.state='patrol'
        self.patrol_dir=pygame.math.Vector2(1,0)
        self.patrol_timer=random.uniform(1,3)
        self.fire_timer=random.uniform(0,self.FIRE_INTERVAL)
        self.hit_flash=0.0

    def try_move(self,dx,dy,gmap):
        r=self.RADIUS; nx=self.pos.x+dx; ny=self.pos.y+dy
        if not (gmap.is_wall(nx-r,self.pos.y) or gmap.is_wall(nx+r,self.pos.y)):
            self.pos.x=nx
        else: self.patrol_dir.x*=-1
        if not (gmap.is_wall(self.pos.x,ny-r) or gmap.is_wall(self.pos.x,ny+r)):
            self.pos.y=ny
        else: self.patrol_dir.y*=-1

    def update(self,dt,player,gmap,enemy_bullets,particles):
        if not self.alive: return
        if self.hit_flash>0: self.hit_flash-=dt
        diff=player.pos-self.pos; dist=diff.length()
        if dist<self.DETECT_RANGE:
            self.state='chase' if dist>self.ATTACK_RANGE else 'attack'
        else: self.state='patrol'
        if self.state=='patrol':
            self.patrol_timer-=dt
            if self.patrol_timer<=0:
                a=random.uniform(0,2*math.pi)
                self.patrol_dir=pygame.math.Vector2(math.cos(a),math.sin(a))
                self.patrol_timer=random.uniform(1.5,3.5)
            mv=self.patrol_dir*self.SPEED_PATROL*dt
            self.try_move(mv.x,mv.y,gmap)
        elif self.state=='chase':
            if dist>0:
                d=diff.normalize()
                mv=d*self.SPEED_CHASE*dt
                self.try_move(mv.x,mv.y,gmap)
            self.angle=math.atan2(diff.y,diff.x)
        elif self.state=='attack':
            self.angle=math.atan2(diff.y,diff.x)
            self.fire_timer-=dt
            if self.fire_timer<=0:
                self.fire_timer=self.FIRE_INTERVAL+random.uniform(-0.3,0.3)
                sp=random.uniform(-0.12,0.12); a=self.angle+sp
                ewd=WeaponDef('enemy',10,320,0,1,1,99,0,C_HIT,4,False)
                b=Bullet(self.pos.x,self.pos.y,a,ewd)
                b.vel=pygame.math.Vector2(math.cos(a)*self.BULLET_SPEED,math.sin(a)*self.BULLET_SPEED)
                enemy_bullets.append(b)

    def take_damage(self,dmg,particles):
        self.hp-=dmg; self.hit_flash=0.15
        for _ in range(6):
            a=random.uniform(0,2*math.pi); s=random.uniform(50,200)
            particles.append(Particle(self.pos.x,self.pos.y,math.cos(a)*s,math.sin(a)*s,(200,30,30),0.5,4))
        if self.hp<=0: self.alive=False

    def draw(self,surf,cam_x,cam_y):
        if not self.alive: return
        sx=int(self.pos.x-cam_x); sy=int(self.pos.y-cam_y)
        if not (0<=sx<WIDTH and 0<=sy<HEIGHT): return
        col=(255,150,150) if self.hit_flash>0 else C_ENEMY
        pygame.draw.circle(surf,C_ENEMY2,(sx,sy),self.RADIUS)
        pygame.draw.circle(surf,col,(sx,sy),self.RADIUS-2)
        pygame.draw.circle(surf,(255,200,200),(sx,sy),self.RADIUS,2)
        ex=sx+math.cos(self.angle)*(self.RADIUS+8)
        ey=sy+math.sin(self.angle)*(self.RADIUS+8)
        pygame.draw.line(surf,(220,80,80),(sx,sy),(int(ex),int(ey)),3)
        bw=32; bh=4; rt=max(0,self.hp/self.max_hp); bx=sx-bw//2; by=sy-self.RADIUS-10
        pygame.draw.rect(surf,(60,20,20),(bx,by,bw,bh))
        pygame.draw.rect(surf,C_HP_LOW,(bx,by,int(bw*rt),bh))
        sc={'patrol':(100,100,200),'chase':(200,150,50),'attack':(220,50,50)}
        pygame.draw.circle(surf,sc.get(self.state,C_GRAY),(sx,sy-self.RADIUS-16),4)

def draw_hud(surf,player,fs,fm,fl,fog_on):
    pad=16; bw=220; bh=18; hr=max(0,player.hp/player.max_hp)
    bx=pad; by=HEIGHT-pad-bh-30
    bg=pygame.Surface((bw+16,bh+50),pygame.SRCALPHA); bg.fill((10,12,20,160))
    surf.blit(bg,(bx-8,by-28))
    surf.blit(fs.render('HP',True,C_WHITE),(bx,by-22))
    pygame.draw.rect(surf,(40,20,20),(bx,by,bw,bh),border_radius=4)
    hc=C_HP_BAR if hr>0.4 else C_HP_LOW
    pygame.draw.rect(surf,hc,(bx,by,int(bw*hr),bh),border_radius=4)
    pygame.draw.rect(surf,C_WHITE,(bx,by,bw,bh),1,border_radius=4)
    ht=fs.render(str(player.hp)+'/'+str(player.max_hp),True,C_WHITE)
    surf.blit(ht,(bx+bw//2-ht.get_width()//2,by+1))
    w=player.weapon; ax=WIDTH-240; ay=HEIGHT-90
    abg=pygame.Surface((230,80),pygame.SRCALPHA); abg.fill((10,12,20,160))
    surf.blit(abg,(ax-8,ay-8))
    surf.blit(fm.render(w.wdef.name,True,C_WHITE),(ax,ay))
    if w.reloading:
        prog=1.0-(w.reload_timer/w.wdef.reload_time)
        surf.blit(fs.render('RELOADING...',True,C_RELOAD),(ax,ay+26))
        rw=200
        pygame.draw.rect(surf,(60,40,10),(ax,ay+44,rw,10),border_radius=3)
        pygame.draw.rect(surf,C_RELOAD,(ax,ay+44,int(rw*prog),10),border_radius=3)
    else:
        surf.blit(fs.render(str(w.ammo)+' / '+str(w.wdef.mag_size),True,C_AMMO),(ax,ay+28))
        for i in range(w.wdef.mag_size):
            px2=ax+i*(200//w.wdef.mag_size); py2=ay+52
            c=C_AMMO if i<w.ammo else (50,60,80)
            pygame.draw.rect(surf,c,(px2,py2,max(3,200//w.wdef.mag_size-2),8),border_radius=2)
    for i,(key,num) in enumerate([('pistol','1'),('shotgun','2'),('rifle','3')]):
        sx2=10+i*110; sy2=HEIGHT-50; act=(key==player.active_weapon)
        bc=(40,80,120,200) if act else (20,24,36,160)
        sb=pygame.Surface((100,38),pygame.SRCALPHA); sb.fill(bc)
        surf.blit(sb,(sx2,sy2))
        if act: pygame.draw.rect(surf,C_AMMO,(sx2,sy2,100,38),2,border_radius=3)
        surf.blit(fs.render('['+num+'] '+WEAPONS[key].name,True,C_WHITE if act else C_GRAY),(sx2+6,sy2+10))
    surf.blit(fm.render('Kills: '+str(player.kills),True,C_WHITE),(pad,pad))
    ft=fs.render('[F] Fog: '+('ON' if fog_on else 'OFF'),True,C_AMMO if fog_on else C_GRAY)
    surf.blit(ft,(pad,pad+30))
    surf.blit(fs.render('WASD:Move  LMB:Fire  R:Reload  1/2/3:Weapon  TAB:Stats',True,C_GRAY),(pad,pad+54))
    mx,my=pygame.mouse.get_pos(); sz=12; gp=5
    pygame.draw.line(surf,C_CROSSHAIR,(mx-sz,my),(mx-gp,my),2)
    pygame.draw.line(surf,C_CROSSHAIR,(mx+gp,my),(mx+sz,my),2)
    pygame.draw.line(surf,C_CROSSHAIR,(mx,my-sz),(mx,my-gp),2)
    pygame.draw.line(surf,C_CROSSHAIR,(mx,my+gp),(mx,my+sz),2)
    pygame.draw.circle(surf,C_CROSSHAIR,(mx,my),3,1)

def draw_minimap(surf,gmap,player,enemies,cam_x,cam_y):
    mw=180; mh=120; mx2=WIDTH-mw-10; my2=10
    sxm=mw/gmap.pixel_w; sym=mh/gmap.pixel_h
    ms=pygame.Surface((mw,mh),pygame.SRCALPHA); ms.fill((8,10,18,200))
    for row in range(gmap.rows):
        for col in range(len(gmap.grid[row])):
            if gmap.grid[row][col]==1:
                rx=int(col*TILE*sxm); ry=int(row*TILE*sym)
                rw=max(1,int(TILE*sxm)); rh=max(1,int(TILE*sym))
                pygame.draw.rect(ms,(70,80,110),(rx,ry,rw,rh))
    for e in enemies:
        if e.alive:
            ex=int(e.pos.x*sxm); ey=int(e.pos.y*sym)
            pygame.draw.circle(ms,C_ENEMY,(ex,ey),3)
    ppx=int(player.pos.x*sxm); ppy=int(player.pos.y*sym)
    pygame.draw.circle(ms,C_PLAYER,(ppx,ppy),4)
    cx=int(cam_x*sxm); cy=int(cam_y*sym)
    cw=int(WIDTH*sxm); ch=int(HEIGHT*sym)
    pygame.draw.rect(ms,(100,180,255,80),(cx,cy,cw,ch))
    pygame.draw.rect(ms,(100,180,255),(cx,cy,cw,ch),1)
    surf.blit(ms,(mx2,my2))
    pygame.draw.rect(surf,C_GRAY,(mx2,my2,mw,mh),1)

def draw_tab(surf,player,fs,fm,fl):
    ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); ov.fill((0,0,0,160))
    surf.blit(ov,(0,0))
    pw=500; ph=320; ppx=WIDTH//2-pw//2; ppy=HEIGHT//2-ph//2
    pn=pygame.Surface((pw,ph),pygame.SRCALPHA); pn.fill((15,18,30,230))
    surf.blit(pn,(ppx,ppy))
    pygame.draw.rect(surf,C_AMMO,(ppx,ppy,pw,ph),2,border_radius=8)
    t=fl.render('-- STATISTICS --',True,C_WHITE)
    surf.blit(t,(ppx+pw//2-t.get_width()//2,ppy+20))
    acc=(player.shots_hit/player.shots_fired*100) if player.shots_fired else 0
    stats=[('Kills',str(player.kills)),('Shots Fired',str(player.shots_fired)),
           ('Shots Hit',str(player.shots_hit)),('Accuracy','%.1f%%'%acc),
           ('HP','%d/%d'%(player.hp,player.max_hp))]
    for i,(lb,vl) in enumerate(stats):
        y=ppy+80+i*40
        l2=fm.render(lb,True,C_GRAY); v2=fm.render(vl,True,C_WHITE)
        surf.blit(l2,(ppx+40,y)); surf.blit(v2,(ppx+pw-40-v2.get_width(),y))
        pygame.draw.line(surf,(40,50,70),(ppx+30,y+28),(ppx+pw-30,y+28))
    h=fs.render('Hold TAB to view  |  ESC to quit',True,C_GRAY)
    surf.blit(h,(ppx+pw//2-h.get_width()//2,ppy+ph-30))

def main():
    pygame.init()
    pygame.mouse.set_visible(False)
    screen=pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('TOP-DOWN 2D SHOOTER SIMULATION')
    clock=pygame.time.Clock()
    try:
        fs=pygame.font.SysFont('Consolas',14)
        fm=pygame.font.SysFont('Consolas',18)
        fl=pygame.font.SysFont('Consolas',28)
    except:
        fs=pygame.font.Font(None,16)
        fm=pygame.font.Font(None,22)
        fl=pygame.font.Font(None,32)
    gmap=GameMap()
    player=Player(3*TILE+20,3*TILE+20)
    ep=[(8*TILE,3*TILE),(20*TILE,5*TILE),(15*TILE,10*TILE),(5*TILE,12*TILE),
        (25*TILE,12*TILE),(10*TILE,7*TILE),(22*TILE,3*TILE),(28*TILE,8*TILE)]
    enemies=[Enemy(ex,ey) for ex,ey in ep if not gmap.is_wall(ex,ey)]
    bullets=[]
    particles=[]
    enemy_bullets=[]
    fog_on=True
    fog_surface=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
    vis_poly=[]
    cam_x=float(player.pos.x-WIDTH//2)
    cam_y=float(player.pos.y-HEIGHT//2)
    show_tab=False
    running=True
    while running:
        dt=min(clock.tick(FPS)/1000.0,0.05)
        for event in pygame.event.get():
            if event.type==pygame.QUIT: running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: running=False
                if event.key==pygame.K_r: player.weapon.start_reload()
                if event.key==pygame.K_1: player.switch_weapon('pistol')
                if event.key==pygame.K_2: player.switch_weapon('shotgun')
                if event.key==pygame.K_3: player.switch_weapon('rifle')
                if event.key==pygame.K_f: fog_on=not fog_on
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                if not player.weapon.wdef.auto:
                    nb=player.weapon.fire(player.pos.x,player.pos.y,player.angle)
                    if nb: player.shots_fired+=1
                    bullets.extend(nb)
        keys=pygame.key.get_pressed()
        show_tab=keys[pygame.K_TAB]
        if pygame.mouse.get_pressed()[0] and player.weapon.wdef.auto:
            nb=player.weapon.fire(player.pos.x,player.pos.y,player.angle)
            if nb: player.shots_fired+=1
            bullets.extend(nb)
        player.update(dt,keys,gmap)
        mx,my=pygame.mouse.get_pos()
        player.aim_at(mx,my,cam_x,cam_y)
        cam_x+=(player.pos.x-WIDTH//2-cam_x)*8*dt
        cam_y+=(player.pos.y-HEIGHT//2-cam_y)*8*dt
        for b in bullets: b.update(dt,gmap)
        new_eb=[]
        for b in enemy_bullets:
            b.update(dt,gmap)
            d=(b.pos-player.pos).length()
            if d<player.RADIUS+b.radius:
                player.hp=max(0,player.hp-b.damage)
                b.alive=False
            if b.alive: new_eb.append(b)
        enemy_bullets=new_eb
        for e in enemies:
            e.update(dt,player,gmap,enemy_bullets,particles)
        alive_b=[]
        for b in bullets:
            if not b.alive: continue
            hit=False
            for e in enemies:
                if not e.alive: continue
                if (b.pos-e.pos).length()<e.RADIUS+b.radius:
                    e.take_damage(b.damage,particles)
                    if not e.alive: player.kills+=1
                    player.shots_hit+=1
                    for _ in range(5):
                        a=random.uniform(0,2*math.pi); s=random.uniform(80,250)
                        particles.append(Particle(b.pos.x,b.pos.y,math.cos(a)*s,math.sin(a)*s,b.color,0.3,3))
                    hit=True; break
            if not hit: alive_b.append(b)
        bullets=alive_b
        particles=[p for p in particles if p.life>0]
        for p in particles: p.update(dt)
        if fog_on:
            vis_poly=build_vis_poly(gmap,player.pos.x,player.pos.y,200)
        screen.fill(C_BG)
        gmap.draw(screen,cam_x,cam_y)
        for p in particles: p.draw(screen,cam_x,cam_y)
        for e in enemies: e.draw(screen,cam_x,cam_y)
        for b in bullets+enemy_bullets: b.draw(screen,cam_x,cam_y)
        player.draw(screen,cam_x,cam_y)
        if fog_on and len(vis_poly)>=3:
            fog_surface.fill((0,0,0,0))
            pygame.draw.rect(fog_surface,(*C_FOG,230),(0,0,WIDTH,HEIGHT))
            sp=[(int(px-cam_x),int(py-cam_y)) for px,py in vis_poly]
            if len(sp)>=3: pygame.draw.polygon(fog_surface,(0,0,0,0),sp)
            screen.blit(fog_surface,(0,0))
        draw_hud(screen,player,fs,fm,fl,fog_on)
        draw_minimap(screen,gmap,player,enemies,cam_x,cam_y)
        if show_tab: draw_tab(screen,player,fs,fm,fl)
        fps=fs.render('FPS: '+str(int(clock.get_fps())),True,C_GRAY)
        screen.blit(fps,(WIDTH//2-fps.get_width()//2,4))
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__=='__main__':
    main()