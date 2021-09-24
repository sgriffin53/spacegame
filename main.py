# Simple pygame program

# Import and initialize the pygame library
import pygame
import os
import math
import random
import time
import sys

pygame.init()
myfont = pygame.font.SysFont('Fixedsys', 22)
clock = pygame.time.Clock()

class FrameInfo():
    def __init__(self):
        self.firingphasers = False
        self.phaserstart = 0
        self.enemyexploding = False
        self.explodestart = 0

class EnemyShip():
    def __init__(self):
        self.hull = 100
        self.maxhull = 100
        self.x = 800
        self.y = 800
        self.visible = True

class SpaceStation():
    def __init__(self):
        self.x = -1000
        self.y = -1000
        self.rotation = 0

class MyShip():
    def __init__(self):
        self.hull = 100
        self.maxhull = 100
        self.x = 0
        self.y = 0
        self.accel = 0
        self.vel = 0
        self.rotaccel = 0
        self.rotation = 0
        self.targeted = None
    def nextTarget(self, enemyships):
        tot_targets = 0
        ava_targets = []
        tgt = self.targeted
        start_tgt = tgt
        new_target = None
        ships_checked = 0
        if tgt == None: tgt = 0
        else: tgt += 1
        while True:
            if ships_checked >= len(enemyships):
                self.targeted = None
                break
            if tgt >= len(enemyships):
                tgt = 0
            if tgt == start_tgt:
                self.targeted = None
                break
            next_target = enemyships[tgt]
            tgt += 1
            ships_checked += 1
            dist = distance(self, next_target)
            if dist > 300:
                continue
            else:
                new_target = tgt - 1
                self.targeted = tgt - 1
                break


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = myfont.render(fps + " FPS", 1, pygame.Color("coral"))
    return fps_text

def get_fps():
    return int(clock.get_fps())

def distance(ship1, ship2):
    # c ^ 2 = a ^ 2 + b ^ 2
    # c = sqrt(a ^ 2 + b ^ 2)
    return math.sqrt((abs(ship1.x - ship2.x) ** 2) + (abs(ship1.y - ship2.y) ** 2))

def rot_center(image, angle, x, y):
    angle = 360 - angle
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect

def drawStars(screen, stars, myship):
    for i in range(0,len(stars)):
        thisX = (stars[i]['x'] - myship.x) % width
        thisY = (stars[i]['y'] + myship.y) % height
        screen.set_at((int(thisX), int(thisY)), (255, 255, 255))

def drawHealthBar(enemyship):
    percentage = enemyship.hull * 100 / enemyship.maxhull

def physicsTick(myship, spacestation, time_since_phys_tick):
    # Calculate new position
    myship.rotation += myship.rotaccel * time_since_phys_tick
    spacestation.rotation += 15 * time_since_phys_tick
    if myship.rotation > 360: myship.rotation = 0
    if myship.rotation > 360: myship.rotation -= 360
    rotation_rads = myship.rotation * math.pi / 180
    myship.vel = myship.vel + myship.accel
    if myship.vel >= 500: myship.vel = 500
    if myship.vel <= 0: myship.vel = 0
    myship.x += (myship.vel) * math.sin(rotation_rads) * time_since_phys_tick
    myship.y += (myship.vel) * math.cos(rotation_rads) * time_since_phys_tick
def renderFrame(screen, stars, myship, enemyships, spacestation, frameinfo, shipIMG, enemyshipIMG, spacestationIMG):

    # Fill the background with white
    screen.fill((0, 0, 0))

    drawStars(screen, stars, myship)

    # Calculate centre

    centre = (width / 2, height / 2)

    # Draw ship

    (shipIMG, newcentre) = rot_center(shipIMG, myship.rotation, centre[0], centre[1]) # rotate ship appropriately
    screen.blit(shipIMG, newcentre)
    i = 0
    enemytotarget = False
    targeteddrawX = 0
    targeteddrawY = 0
    targetedenemy = None
    for enemyship in enemyships:
        dist = distance(myship, enemyship)
        if dist > 1400: continue
        # Draw enemy ship
        enemydrawX = centre[0] + enemyship.x - myship.x
        enemydrawY = centre[1] - enemyship.y + myship.y
        if enemyship.visible:
            screen.blit(enemyshipIMG, (enemydrawX, enemydrawY))
            if myship.targeted == i:
                pygame.draw.rect(screen, (255, 0, 0), (enemydrawX, enemydrawY, 48, 46), 2)
                targeteddrawX = enemydrawX
                targeteddrawY = enemydrawY
                enemytotarget = True
                targetedenemy = enemyship
        i += 1


    # Draw space station
    spacestationX = centre[0] + spacestation.x - myship.x
    spacestationY = centre[1] - spacestation.y + myship.y
    dist = distance(myship, spacestation)
    if dist <= 1400:
        (spacestationIMG, spacestationcentre) = rot_center(spacestationIMG, spacestation.rotation, spacestationX, spacestationY)
        screen.blit(spacestationIMG, spacestationcentre)
    # Draw phasers

    if frameinfo.firingphasers and enemytotarget:
        pygame.draw.line(screen, (255, 0, 0), (centre[0], centre[1]), (targeteddrawX + 15, targeteddrawY + 15), 4)
        if (time.time() - frameinfo.phaserstart > 0.03):
            frameinfo.firingphasers = False
            targetedenemy.hull -= 10

    if frameinfo.enemyexploding and myship.targeted is not None:
        time_elapsed = time.time() - frameinfo.explodestart
        if time_elapsed >= 0.25:
            frameinfo.enemyexploding = False
            targetedenemy.visible = False
        else:
            circlesize = 160 * (0.25 - time_elapsed)
            pygame.draw.circle(screen, (255, 50, 50), (targeteddrawX + 25, targeteddrawY + 25), circlesize)

    if targetedenemy != None and targetedenemy.visible and not frameinfo.enemyexploding and targetedenemy.hull <= 0:
        frameinfo.enemyexploding = True
        frameinfo.explodestart = time.time()

    # Draw text:

    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.

    velText = myfont.render('Velocity: ' + str(round(myship.vel,1)), False, (255, 255, 255))
    shipXText = myfont.render('X: ' + str(round(myship.x,0)), False, (255, 255, 255))
    shipYText = myfont.render('Y: ' + str(round(myship.y,0)), False, (255, 255, 255))
    screen.blit(shipXText, (2, 540))
    screen.blit(shipYText, (2, 560))
    screen.blit(velText, (2, 580))
    curfps = get_fps()
    fps_text = myfont.render(str(curfps) + " FPS", 1, pygame.Color("coral"))
    screen.blit(fps_text, (10, 5))


width = 1280
height = 720

# Set up the drawing window
screen = pygame.display.set_mode([width, height])

spacestationIMG = pygame.image.load(os.path.join('images', 'station.png')).convert_alpha()
shipIMG = pygame.image.load(os.path.join('images','ship.png')).convert_alpha()
enemyshipIMG = pygame.image.load(os.path.join('images', 'enemyship.png')).convert_alpha()

fullscreen = False
stars = []
for i in range(250):
  stars.append(dict({'x': 0, 'y': 0}))
  stars[i]['x'] = random.random()*width
  stars[i]['y'] = random.random()*height
myship = MyShip()
enemyships = []
for i in range(10000):
    enemyships.append(EnemyShip())
    enemyships[i].x = random.randint(-100000,100000)
    enemyships[i].y = random.randint(-100000,100000)

#enemyship = EnemyShip()
spacestation = SpaceStation()

frameinfo = FrameInfo()
# Run until the user asks to quit
running = True
i = 0
curfps = 0
alt_pressed = False
enter_pressed = False
last_phys_tick = time.time()

while running:
    i+= 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
            if not fullscreen:
                screen = pygame.display.set_mode([width, height], pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode([width, height])
            fullscreen = not fullscreen
        # set alt and enter flags if the keys are pressed
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_RALT or event.key == pygame.K_LALT):
            alt_pressed = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            enter_pressed = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            myship.nextTarget(enemyships)
    if alt_pressed and enter_pressed: # full screen with alt+enter
        if not fullscreen:
            screen = pygame.display.set_mode([width, height], pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode([width, height])
        fullscreen = not fullscreen

    keys = pygame.key.get_pressed()  # checking pressed keys

    # unset alt and enter flags if they're not pressed

    if not keys[pygame.K_RALT] and not keys[pygame.K_LALT]:
        alt_pressed = False
    if not keys[pygame.K_RETURN]:
        enter_pressed = False
    if keys[pygame.K_LEFT]:
        myship.rotaccel = -120
    elif keys[pygame.K_RIGHT]:
        myship.rotaccel = 120
    else:
        myship.rotaccel = 0
    if keys[pygame.K_UP]:
        myship.accel = 10
    elif keys[pygame.K_DOWN]:
        myship.accel = -10
    else:
        myship.accel = 0
    if keys[pygame.K_ESCAPE]:
        sys.exit()
    if keys[pygame.K_SPACE]:
        if myship.targeted != None:
            frameinfo.firingphasers = True
            frameinfo.phaserstart = time.time()

    time_since_phys_tick = time.time() - last_phys_tick
    physicsTick(myship, spacestation, time_since_phys_tick)
    last_phys_tick = time.time()

    renderFrame(screen, stars, myship, enemyships, spacestation, frameinfo, shipIMG, enemyshipIMG, spacestationIMG)

    clock.tick(100000)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()