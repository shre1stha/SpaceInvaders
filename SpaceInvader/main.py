import pygame
import random
import math
from pygame import mixer

#Initialize the pygame
pygame.init()
#Create the screen with tuple of  width and height
screen = pygame.display.set_mode((800,600))
#Background
background=pygame.image.load('back.png')
#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)
#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('spaceship (3).png')
playerX=370
playerY=480
playerX_change=0

#enemy
enemyImg = []
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(30)

#bullet
#ready means you can't see the bullet on screen
#fire means bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=0.5
bullet_state="ready"

#score
score_value=0
font = pygame.font.Font('freesansbold.ttf',32)

textX=10
textY=10

#game over text
over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score=font.render("Score:"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))
def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+10))

def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance= math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance <27:
        return True
    else:
        return False

#Game loop
running=True
while running:

    #RGB - Red, Green, Blue
    screen.fill((0,0,0))
    #Background image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change =-0.3
            if event.key == pygame.K_RIGHT:
                playerX_change =0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
#checking for boundaries of spaceship so that it doesn't go out of bound
    playerX +=playerX_change

    if playerX<=0:
        playerX=0
    elif playerX >=736:
        playerX=736
# enemy movement
    for i in range(num_of_enemies):
        #game over
        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i],i)


    #bullet movement
    if bulletY <=0:
        bulletY=480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -=bulletY_change



    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()