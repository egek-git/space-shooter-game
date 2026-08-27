import pygame
import datetime
import random
#setup
pygame.init()
SCREEN_WIDTH = 540
SCREEN_HEIGHT = 960
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
game_over = False
#add score
score = 0
Enemy_bullets = []
Player_bullets = []
font = pygame.font.SysFont("Arial", 64)
score_font = pygame.font.SysFont("Arial", 20)
class Plane:
    def __init__(self, x, y):
        plane_image_original = pygame.image.load("assets/plane-96x96.png")
        self.image = plane_image_original
        self.width = 96
        self.height = 96
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.speed = 5
        self.life = 3
        self.last_fired = 0
        self.cooldown = 250
    def lifeControl(self):
        if self.life <= 0:
            return True
        return False
            #add "game over"
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width ))
        self.y = max(SCREEN_HEIGHT*0.2, min(self.y, SCREEN_HEIGHT - self.height))
        self.rect.x = self.x
        self.rect.y = self.y
    def fire(self):
        now = pygame.time.get_ticks()
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and now - self.last_fired >= self.cooldown:
            new_bullet = Bullet(self.x + self.width/2, self.y, speed=-8, color=(255,0,0))
            Player_bullets.append(new_bullet)
            self.last_fired = now
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
plane_player = Plane(220,800)
#lifes and effects
blast_image = pygame.image.load("assets/blast-96x96.png")
heart_image = pygame.image.load("assets/heart.png")
scaled_heart = pygame.transform.scale(heart_image,(70,70))
broken_heart_image = pygame.image.load("assets/broken-heart.png")
scaled_broken_heart = pygame.transform.scale(broken_heart_image,(70,70))
#enemy images
enemy_blue = pygame.image.load("assets/enemy1-64x64.png")
enemy_orange = pygame.image.load("assets/enemy2-64x64.png")
enemy_green = pygame.image.load("assets/enemy3-64x64.png")
ENEMY_WIDTH = 64
enemy_limit=5
last_enemy_spawn = 0
enemy_spawn_timer = 1500 
enemies = []
explosions = []
def reset_game():
    global score, game_over, Player_bullets, Enemy_bullets, enemies, explosions
    score =  0
    plane_player.life = 3
    game_over = False
    Player_bullets.clear()
    Enemy_bullets.clear()
    enemies.clear()
    explosions.clear()
    plane_player.x = 220
    plane_player.y = 800
    plane_player.rect.x = plane_player.x
    plane_player.rect.y = plane_player.y

 
class Enemy:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - 64)
        self.y = random.randint(0, 400)
        self.width = 64
        self.height = 64
        self.speed = random.randint(20, 30)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.type = random.randint(1,3)
        self.last_slide = 0
        if self.type == 1:
            self.image = enemy_blue
            self.slide_cooldown = 1000
            self.cooldown = random.randint(2000,2500)
        elif self.type == 2:
            self.image = enemy_orange
            self.slide_cooldown = 1500
            self.cooldown = random.randint(1500,2000)
        else:
            self.image = enemy_green
            self.slide_cooldown = 2000
            self.cooldown = random.randint(1000,1500)
        self.last_fired = 0

    def slide(self):
        now = pygame.time.get_ticks()
        if now - self.last_slide >= self.slide_cooldown:
            self.y += self.speed
            self.rect.y = self.y
            self.last_slide = now
    def fire(self):
        now = pygame.time.get_ticks()
        if now - self.last_fired >= self.cooldown:
            enemy_bullet = Bullet(self.x + self.width/2, self.y, speed=6, color=(0,255,0))
            Enemy_bullets.append(enemy_bullet)
            self.last_fired = now
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = blast_image
        self.spawn_time = pygame.time.get_ticks()
        self.duration = 250
    def draw(self,screen):
        screen.blit(self.image, (self.x, self.y))

class Bullet:
    def __init__(self, x, y, speed, color=(255,255,0)):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 12
        self.speed = speed
        self.color = color
        self.rect = pygame.Rect(self.x ,self.y , self.width, self.height)
    def moveBullet(self):
        self.y += self.speed
        self.rect.y = self.y
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


while running:
    now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((131, 174, 242))
    if len(enemies) < enemy_limit and now - last_enemy_spawn >= enemy_spawn_timer:
        new_enemy = Enemy()
        enemies.append(new_enemy)
        last_enemy_spawn = now
    if not game_over:
        plane_player.move()
        for enemy in enemies[:]:
            enemy.slide()
            enemy.draw(screen)
            enemy.fire()
            if enemy.y > 800:
                enemies.remove(enemy)
        for enemy_bullet in Enemy_bullets[:]:
            enemy_bullet.moveBullet()
            enemy_bullet.draw(screen)
            if enemy_bullet.y >= 960:
                Enemy_bullets.remove(enemy_bullet)
        game_over = plane_player.lifeControl()
        plane_player.fire()
        for bullet in Player_bullets[:]:
            bullet.moveBullet()
            bullet.draw(screen)
            if bullet.y < 0:
                Player_bullets.remove(bullet)
        for bullet in Player_bullets[:]:
            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    Player_bullets.remove(bullet)
                    enemies.remove(enemy)
                    new_explosion = Explosion(enemy.x, enemy.y)
                    explosions.append(new_explosion)
                    score += 10
                    break
        for explosion in explosions[:]:
            explosion.draw(screen)
            if now - explosion.spawn_time >= explosion.duration:
                explosions.remove(explosion)
        for enemy_bullet in Enemy_bullets[:]:
            if enemy_bullet.rect.colliderect(plane_player.rect):
                Enemy_bullets.remove(enemy_bullet)
                plane_player.life -= 1
    #heart images and score
    if plane_player.life == 3:
        screen.blit(scaled_heart, (10, SCREEN_HEIGHT -70))
        screen.blit(scaled_heart, (50, SCREEN_HEIGHT - 70))
        screen.blit(scaled_heart, (90, SCREEN_HEIGHT - 70))
    elif plane_player.life == 2:
        screen.blit(scaled_heart, (10, SCREEN_HEIGHT -70))
        screen.blit(scaled_heart, (50, SCREEN_HEIGHT - 70))
        screen.blit(scaled_broken_heart, (95, SCREEN_HEIGHT - 65))
    elif plane_player.life == 1:
        screen.blit(scaled_heart, (5, SCREEN_HEIGHT -70))
        screen.blit(scaled_broken_heart, (50, SCREEN_HEIGHT - 65))
        screen.blit(scaled_broken_heart, (95, SCREEN_HEIGHT - 65))
    elif plane_player.life <= 0:
        screen.blit(scaled_broken_heart, (5, SCREEN_HEIGHT -65))
        screen.blit(scaled_broken_heart, (50, SCREEN_HEIGHT - 65))
        screen.blit(scaled_broken_heart, (95, SCREEN_HEIGHT - 65))
    score_write = score_font.render(f"Score: {score}", True, (0,0,0))
    score_rect = score_write.get_rect(center=(60,20))
    screen.blit(score_write, score_rect)
    #writing Game over and stopping the game  
    if game_over:
        writing = font.render("GAME OVER \nPress 'R' to restart", True, (255,0,0))
        text_rect = writing.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(writing, text_rect)
        key = pygame.key.get_pressed()
        if key[pygame.K_r]:
            reset_game()

    
    plane_player.draw(screen)
    pygame.display.flip()
    clock.tick(60) #limits FPS to 60 


pygame.quit()