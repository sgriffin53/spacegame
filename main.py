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

class Point():
    def __init__(self):
        self.x = 0
        self.y = 0

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
        self.width = 50
        self.index = 0

class SpaceStation():
    def __init__(self):
        self.x = -1000
        self.y = -1000
        self.rotation = 0
        self.width = 1024

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
        tgt = self.targeted
        start_tgt = tgt
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
            if dist > 2000:
                continue
            else:
                self.targeted = tgt - 1
                break


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = myfont.render(fps + " FPS", 1, pygame.Color("coral"))
    return fps_text

def get_fps():
    return int(clock.get_fps())

def onScreen(obj, ship):
    # detects whether a circle with radius obj.width is on the screen

    # screen:
    # A ---- B
    # |      |
    # C ---- D

    obj_left = obj.x - obj.width / 2
    obj_right = obj.x + obj.width / 2
    obj_top = obj.y + obj.width / 2
    obj_bottom = obj.y - obj.width / 2
    pointA_x = ship.x - width / 2
    pointA_y = ship.y + height / 2
    pointB_x = ship.x + width / 2
    pointB_y = pointA_y
    pointC_x = pointA_x
    pointC_y = ship.y - height / 2
    pointD_x = pointB_x
    pointD_y = pointC_y
    if obj_right >= pointA_x and obj_left <= pointB_x and obj_top >= pointC_y and obj_bottom <= pointA_y:
        return True
    return False


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

def drawTargetLine(screen, myship, enemyship):
    # x1, y1 = point at edge of screen
    # x2, y2 = point which intersects with line between ships at (x1, y2 - 200)
    centre = (width / 2, height / 2)

    # find direction
    lowest_dist = 0
    x_dist = abs(enemyship.x - myship.x)
    y_dist = abs(enemyship.y - myship.y)
    dir = "left"
    if enemyship.x <= myship.x:
        dir = "left"
        lowest_dist = x_dist
    if enemyship.y <= myship.y:
        if y_dist >= lowest_dist:
            dir = "bottom"
            lowest_dist = y_dist
    if enemyship.x >= myship.x:
        if x_dist >= lowest_dist:
            dir = "right"
            lowest_dist = x_dist
    if enemyship.y >= myship.y:
        if y_dist >= lowest_dist:
            dir = "top"
    x1, y1, x2, y2, m, c = 0, 0, 0, 0, 0, 0
    if enemyship.x - myship.x == 0: m = 0
    else: m = (enemyship.y - myship.y) / (enemyship.x - myship.x)
    if m == 0: m = 0.00001
    c = myship.y - m * myship.x
    if dir == "bottom":
        y1 = myship.y - height / 2
        x1 = (y1 - c) / m
        y2 = y1 + 150
        x2 = (y2 - c) / m
    elif dir == "top":
        y1 = myship.y + height / 2
        x1 = (y1 - c) / m
        y2 = y1 - 150
        x2 = (y2 - c) / m
    elif dir == "left":
        x1 = myship.x - width / 2
        y1 = m * x1 + c
        x2 = x1 + 150
        y2 = m * x2 + c
    elif dir == "right":
        x1 = myship.x + width / 2
        y1 = m * x1 + c
        x2 = x1 - 150
        y2 = m * x2 + c
    else: return
    draw_x1 = int(centre[0] + x1 - myship.x)
    draw_y1 = int(centre[1] - y1 + myship.y)
    draw_x2 = int(centre[0] + x2 - myship.x)
    draw_y2 = int(centre[1] - y2 + myship.y)
    colour = (128, 0, 0)
    if enemyship.index == myship.targeted:
        colour = (0, 0, 128)
    pygame.draw.line(screen, colour, (draw_x1, draw_y1), (draw_x2, draw_y2), 3)
    thisfont = pygame.font.SysFont('Fixedsys', 16)
    dist = distance(myship, enemyship)
    distanceText = thisfont.render(str(int(dist)), False, (255, 255, 255))
    drawX = -1000
    drawY = -1000
    if dir == "top":
        drawX = draw_x2 + 20
        drawY = draw_y2 - 20
    #screen.blit(distanceText, (drawX, drawY))

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
    i = -1
    enemytotarget = False
    targeteddrawX = 0
    targeteddrawY = 0
    targetedenemy = None
    for enemyship in enemyships:
        i += 1
        dist = distance(myship, enemyship)
        if dist > 2000: continue
        if (not onScreen(enemyship, myship)): drawTargetLine(screen, myship, enemyship)
        if dist > 1400: continue
        # Draw enemy ship
        enemydrawX = centre[0] + enemyship.x - myship.x
        enemydrawY = centre[1] - enemyship.y + myship.y
        if enemyship.visible:
            screen.blit(enemyshipIMG, (enemydrawX, enemydrawY))
            thisfont = pygame.font.SysFont('Fixedsys', 16)
            indexText = thisfont.render(str(i), False, (255, 255, 255))
            distanceText = thisfont.render(str(int(dist)), False, (255, 255, 255))
            screen.blit(indexText, (enemydrawX - 10, enemydrawY - 10))
            screen.blit(distanceText, (enemydrawX - 10, enemydrawY + 20))
            if myship.targeted == i:
                pygame.draw.rect(screen, (255, 0, 0), (enemydrawX, enemydrawY, 48, 46), 2)
                targeteddrawX = enemydrawX
                targeteddrawY = enemydrawY
                enemytotarget = True
                targetedenemy = enemyship


    # Draw space station
    spacestationX = centre[0] + spacestation.x - myship.x
    spacestationY = centre[1] - spacestation.y + myship.y
    dist = distance(myship, spacestation)
    if onScreen(spacestation, myship):
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
for i in range(100):
    enemyships.append(EnemyShip())
    enemyships[i].x = random.randint(-10000, 10000)
    enemyships[i].y = random.randint(-10000, 10000)
    enemyships[i].index = i
    #enemyships[i].x = 0
    #enemyships[i].y = 0

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