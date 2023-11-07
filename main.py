
import pygame
from pygame import mixer
import random
import math

pygame.init()

screen = pygame.display.set_mode((800,600))
background = pygame.image.load("space.png")
caption = pygame.display.set_caption("Space Invaders")

mixer.music.load("background.mp3")
mixer.music.play(-1)

icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

player_img = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemies = 6
for i in range(enemies):
    enemy_img.append(pygame.image.load("enemy1.png"))
    enemyX.append(random.randint(0,750))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(1)
    enemyY_change.append(40)

bullet_img =  pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 2
bullet_state = "ready"

score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10

over_font = pygame.font.Font("freesansbold.ttf",64)
def showscore(x,y):
    score = font.render("Score : " + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))
def player(x,y):
    screen.blit(player_img,(x,y))

def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))

def firebullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img,(x+16,y+10))

def is_collision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX),2) + math.pow((enemyY - bulletY),2))
    if distance < 27:
        return True
    else:
        return False

running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    firebullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    player(playerX,playerY)

    for i in range(enemies):
        if enemyY[i] > 430:
            for j in range(enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 750:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 750)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i],enemyY[i],i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        firebullet(bulletX,bulletY)
        bulletY -= bulletY_change

    showscore(textX,textY)
    pygame.display.update()
