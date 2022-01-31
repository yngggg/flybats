import pygame
import random
import os

WIDTH = 1920
HEIGHT = 1080
FPS = 60

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра")
clock = pygame.time.Clock()

#пикчи
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
player_img = pygame.image.load(os.path.join(img_folder, 'p1_jump.png')).convert()
level1_img = pygame.image.load(os.path.join(img_folder, 'bg_grasslands.png')).convert()
enem_img = pygame.image.load(os.path.join(img_folder, 'enem.png')).convert()
bomb_img = pygame.image.load(os.path.join(img_folder, 'bomb.png')).convert()
bul_img = pygame.image.load(os.path.join(img_folder, 'bul.png')).convert()
heart_img = pygame.image.load(os.path.join(img_folder, 'heart.png')).convert()
cycl_img = pygame.image.load(os.path.join(img_folder, 'cycl.png')).convert()
diabl_img = pygame.image.load(os.path.join(img_folder, 'diabl.png')).convert()
orang_img = pygame.image.load(os.path.join(img_folder, 'orang.png')).convert()
boss_img = pygame.image.load(os.path.join(img_folder, 'boss.png')).convert()


jumpCount = 30
jump = jumpCount

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

heart_img.set_colorkey(BLACK)

def pause():
    pygame.pause(player)
    
def newcycl():
    c = Cycl()
    all_sprites.add(c)
    cycls.add(c)
    
def newdiabl():
    d = Diabl()
    all_sprites.add(d)
    diabls.add(d)
 
def neworang():
    o = Orang()
    all_sprites.add(o)
    orangs.add(o)
def newheart():
    h = Heart()
    all_sprites.add(h)
    hearts.add(h)
    

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 400
    BAR_HEIGHT = 40
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)
    

        
    
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 130))
        self.image = boss_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(600,900)
        self.rect.y = random.randrange(HEIGHT - 700)
        self.speedx = random.randrange(-10 , 10)
        self.shield = 400

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speedx = random.randrange(-10 ,-1)
        if self.rect.left < 0:
            self.rect.left = 0
            self.speedx = random.randrange(1 , 10)

    def draw_boss(self, surf, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH_1 = 150
        BAR_HEIGHT_1 = 20
        fill_1 = (pct / 100) * BAR_LENGTH_1
        outline_rect_1 = pygame.Rect(self.rect.x-70/2, self.rect.y-25, BAR_LENGTH_1, BAR_HEIGHT_1)
        fill_rect_1 = pygame.Rect(self.rect.x-70/2, self.rect.y-25, fill_1, BAR_HEIGHT_1)
        pygame.draw.rect(surf, GREEN, fill_rect_1)
        pygame.draw.rect(surf, WHITE, outline_rect_1, 2)
        
    def shoot(self):
        if aras.shield>1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
        else:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(90,120))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom= HEIGHT-10
        self.speedx=0
        self.shield = 100
        self.lives = 4
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        
        
        
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
	        self.hidden = False
	        self.rect.centerx = WIDTH / 2
	        self.rect.bottom = HEIGHT - 10
        if self.shield<1:
            self.kill()    
        
    def shoot(self):
        if player.shield>1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
        else:
            self.kill()
        
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
            
            
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(enem_img, (80,60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        
    
    def update(self):
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top > HEIGHT +10:
            self.rect.x=random.randrange(WIDTH - self.rect.width)
            self.rect.y=random.randrange(-10,-4)
            self.speedy=random.randrange(1,8)
            
            
class Cycl(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(cycl_img, (80,60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-3, 3)
        self.shield = 200

    
    def update(self):
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top > HEIGHT +10:
            self.rect.x=random.randrange(WIDTH - self.rect.width)
            self.rect.y=random.randrange(-10,-4)
            self.speedy=random.randrange(1,8)

class Diabl(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(diabl_img, (80,60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        
    
    def update(self):
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top > HEIGHT +10:
            self.rect.x=random.randrange(WIDTH - self.rect.width)
            self.rect.y=random.randrange(-10,-4)
            self.speedy=random.randrange(1,8)            

class Orang(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(orang_img, (90,40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        
    
    def update(self):
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top > HEIGHT +10:
            self.rect.x=random.randrange(WIDTH - self.rect.width)
            self.rect.y=random.randrange(-10,-4)
            self.speedy=random.randrange(1,8)            
            
class Heart(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=heart_img
        self.image.set_colorkey(BLACK)
        self.rect= self.image.get_rect()
        self.rect.x=random.randrange(WIDTH - self.rect.width)
        self.rect.y=random.randrange(-100,-40)
        self.speedy=random.randrange(1,8)
        self.speedx=random.randrange(-3,3)
        

    
    def update(self):
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top > HEIGHT +10:
            self.rect.x=random.randrange(WIDTH - self.rect.width)
            self.rect.y=random.randrange(-10,40)
            self.speedy=random.randrange(1,4)
           
            
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=bul_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        
    def update(self):
        self.rect.y+=self.speedy 
        if self.rect.bottom<0:
            self.kill()
            
       

class Background(pygame.sprite.Sprite):
    def __init__(self,image_file,location):
        pygame.sprite.Sprite.__init__(self)
        self.image = level1_img
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = location 
        

            
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
cycls = pygame.sprite.Group()
diabls=pygame.sprite.Group()
orangs=pygame.sprite.Group()     
bullets = pygame.sprite.Group()
bombs=pygame.sprite.Group()
hearts=pygame.sprite.Group()
aras = pygame.sprite.Group()

ara = Boss()

pygame.sprite.collide_rect_ratio(0.7)
BackGround=Background('bg_grasslands',[0,0])
player = Player()
all_sprites.add(player)

def die_screen():
    screen.blit(BackGround.image, BackGround.rect)
    draw_text(screen, "Wellcome!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to start", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
def newara():
    a = Boss()
    all_sprites.add(a)
    aras.add(a)

for i in range(8):
    newmob()

for i in range(5):
    newcycl()  
    
for i in range(5):
    newdiabl()
    
for i in range(10):
    neworang()


for i in range(10):
    newheart()


for i in range(4):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


if player.shield < 1:
    start = True
    
    
# Цикл игры
start = True
running = True
while running:
    if start:
        die_screen()
        start = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        cycls = pygame.sprite.Group()
        diabls=pygame.sprite.Group()
        orangs=pygame.sprite.Group()     
        bullets = pygame.sprite.Group()
        bombs=pygame.sprite.Group()
        hearts=pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
            newdiabl()
            newcycl()
            neworang()
            newheart()
            all_sprites.add(player)
        score = 0
        if player.shield < 1:
            start = False
            
            
    clock.tick(FPS)
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
                
    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        newmob()
        score +=100
    hits = pygame.sprite.groupcollide(diabls, bullets, True, True)
    for hit in hits:
        newdiabl()
        score +=100
    hits = pygame.sprite.groupcollide(cycls, bullets, True, True)
    for hit in hits:
        score +=100
        newcycl()
    hits = pygame.sprite.groupcollide(orangs, bullets, True, True)
    for hit in hits:    
        neworang()
        score +=100
    hits = pygame.sprite.groupcollide(aras, bullets, True, True)
    for hit in hits:
        score +=10000000

    hits = pygame.sprite.spritecollide(player,hearts, True, pygame.sprite.collide_circle)
    if hits: #здесь хп после урона от моба
        player.shield =  100
            
        if player.shield <= 0:
            running = True
    hits = pygame.sprite.spritecollide(player,mobs, True, pygame.sprite.collide_circle)
    if hits: #здесь хп после урона от моба
        player.shield -=  10
        if player.shield <= 0:
            running = True
    hits = pygame.sprite.spritecollide(player,orangs, True, pygame.sprite.collide_circle)
    if hits: #здесь хп после урона от моба
        player.shield -=  40
        if player.shield <= 0:
            running = True
    hits = pygame.sprite.spritecollide(player,diabls, True, pygame.sprite.collide_circle)
    if hits: #здесь хп после урона от моба
        player.shield -=  60
        if player.shield <= 0:
            running = True
            
    hits = pygame.sprite.spritecollide(player,cycls, True, pygame.sprite.collide_circle)
    if hits: #здесь хп после урона от моба
        player.shield -=  30
        if player.shield <= 0:
            running = True
             

    screen.fill([255,255,255])
    screen.blit(BackGround.image, BackGround.rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 28, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    pygame.display.flip()
   
pygame.quit()  
    



