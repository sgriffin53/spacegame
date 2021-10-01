# Simple pygame program

# Import and initialize the pygame library
import pygame
import os
import math
import random
import time
import sys
from datetime import datetime

pygame.init()
myfont = pygame.font.SysFont('Fixedsys', 22)
dir_label_font = pygame.font.SysFont('Courier', 12)
clock = pygame.time.Clock()

class Animation():
    def __init__(self):
        self.type = None
        self.starttime = 0
        self.endtime = 0
        self.startpos = 0
        self.endpos = 0
        self.colour = (255, 0, 0)
        self.targettype = None

class Music():
    def __init__(self):
        self.file = None

class Sound():
    def __init__(self):
        self.file = None
        self.mixer = None


class Weapon():
    def __init__(self):
        self.type = None
        self.duration = None
        self.chargetime = 0
        self.lastfired = 0
        self.range = 0

class GameInfo():
    def __init__(self):
        self.timefactor = 1
        self.redalert = False
        self.alive = True
        self.lastdied = 0

class Point():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0

class FrameInfo():
    def __init__(self):
        self.firingphasers = False
        self.phaserstart = 0
        self.enemyexploding = False
        self.explodestart = 0

class EnemyShip():
    def __init__(self):
        self.objtype = "enemy"
        self.hull = 100
        self.maxhull = 100
        self.x = 800
        self.y = 800
        self.visible = True
        self.width = 50
        self.index = 0
        self.type = "Frigate"
        self.state = None
        self.vel = 0
        self.rotation = 0
        self.rotaccel = 0
        self.patroldist = 0
        self.patrolstart = [0, 0]
        self.accel = 0
        self.patrolgoal = [0, 0]
        self.patrolangle = 0
        self.patrolspeed = 0
        self.totrotations = 0
        self.patroltotrotations = 0
        self.shipIMG = None
        self.lastx = 0
        self.lasty = 0
        self.radius = 24
        self.resttime = 0
        self.reststart = 0
        self.weapons = []
        self.lastattacked = 0
        self.maxspeed = 400
        self.substate = None
        self.attackstart = 0
    def startPatrol(self):
        self.totrotations = 0
        self.accel = 250
        self.rotaccel = 120
        if random.randint(0,1) == 0:
            self.rotaccel = -120
        self.patrolstart = [self.x, self.y]
        self.patrolangle = random.randint(-360, 360)
        #self.patrolangle = self.rotation + self.patrolangle
        self.origangle = self.patrolangle
        self.patroltotrotations = abs(self.patrolangle - self.rotation)
        if self.patrolangle < 0: self.patrolangle += 360
        if self.patrolangle > 360: self.patrolangle -= 360
        self.patroldist = random.randint(500, 2000)
        patrolanglerads = self.patrolangle * math.pi / 180
        a = patrolanglerads
        d = self.patroldist
        self.patrolspeed = random.randint(120, 300)
        opp = abs(math.cos(a) * d)
        adj = abs(math.sin(a) * d)
        x2 = self.x + opp
        y2 = self.y + adj
        self.patrolgoal = (x2, y2)
    def startLeaveStation_rot(self):
        self.totrotations = 0
        self.patrolstart = [self.x, self.y]
        self.rotaccel = 120
        self.patrolangle = self.rotation - 180
        self.origangle = self.patrolangle
        if self.patrolangle > 360: self.patrolangle -= 360
        elif self.patrolangle < 0: self.patrolangle += 360
        self.patroltotrotations = 180
    def startLeaveStation_fly(self):
        self.totrotations = 0
        self.patrolstart = [self.x, self.y]
        self.accel = 250
        self.rotaccel = 0
        self.patrolstart = [self.x, self.y]
        self.patroldist = random.randint(400, 800)
        if self.substate == "attack" or self.substate == "attack_delay":
            self.patroldist = 100
    def startGoToStation(self, spacestation):
        self.totrotations = 0
        self.patrolstart = [self.x, self.y]
        self.accel = 250
        self.rotaccel = 120
        dy = self.y - spacestation.y
        dx = self.x - spacestation.x
        angle_deg = 360 - math.atan2(dy, dx) * 180 / math.pi - 90
        self.patrolangle = angle_deg
        self.origangle = self.patrolangle
        self.patroltotrotations = abs(self.patrolangle - self.rotation)
        if self.patrolangle < 0: self.patrolangle += 360
        if self.patrolangle > 360: self.patrolangle -= 360
        mypoint = Point()
        mypoint.x = spacestation.x
        mypoint.y = spacestation.y
        dist = int(distance(self, mypoint))
        self.patroldist = dist - spacestation.radius - random.randint(30,150)
        #r = random.randint(1,2)
        #if r == 1:
         #   self.patroldist += random.randint(20, 50)
        #elif r == 2:
            #self.patroldist -= random.randint(20, 50)
        self.patrolspeed = random.randint(120, 300)
    def startRetreat(self):
        self.patrolspeed = self.maxspeed
        self.patrolstart = [self.x, self.y]
        self.patroldist = 5000
        self.accel = 250
        dy = self.y - myship.y
        dx = self.x - myship.x
        angle_deg = 360 - math.atan2(dy, dx) * 180 / math.pi - 90 - 180
        self.patrolangle = angle_deg
        self.rotaccel = 120
        if angle_deg >= 180:
            self.rotaccel = -120
    def explode(self, animations):
        self.vel = 0
        animation = Animation()
        animation.type = "explosion"
        animation.starttime = time.time()
        animation.endtime = time.time() + 0.25
        animation.startpos = (self.x, self.y)
        animation.targettype = "enemyship"
        animation.width = enemyship.width
        animations.append(animation)

    def fireNextWeapon(self, myship, animations, sounds):
        dist = distance(self, myship)
        for weapon in self.weapons:
            if dist > weapon.range: continue
            charged = False
            if time.time() - weapon.lastfired >= weapon.chargetime:
                # weapon is charged

                weapon.lastfired = time.time()
                pygame.mixer.Sound.play(sounds[0].mixer)
                # fired weapon on target

                myship.hull -= 10
                if myship.hull <= 0:
                    myship.alive = False
                    gameinfo.alive = False
                    gameinfo.lastdied = time.time()
                    myship.vel = 0
                    myship.rotaccel = 0
                    myship.accel = 0
                    myship.explode(animations)
                myship.lastattacker = self.index
                # add animation

                animation = Animation()
                animation.type = "laser"
                animation.colour = (0, 255, 0)
                animation.starttime = time.time()
                animation.endtime = time.time() + weapon.duration
                animation.startpos = (myship.x, myship.y)
                animation.endpos = (self.x, self.y)
                animations.append(animation)

class SpaceStation():
    def __init__(self):
        self.objtype = "spacestation"
        self.x = -1000
        self.y = -1000
        self.rotation = 0
        self.width = 922
        self.type = "Space Station"
        self.radius = 922 / 2

class MyShip():
    def __init__(self):
        self.hull = 200
        self.maxhull = 200
        self.x = 0
        self.y = 0
        self.lastx = 0
        self.lasty = 0
        self.accel = 0
        self.vel = 0
        self.rotaccel = 0
        self.rotation = 0
        self.targeted = None
        self.sensorrange_ships = 2000
        self.sensorrange_stations = 5000
        self.width = 49
        self.radius = 24
        self.weapons = []
        self.lastattacker = None
        self.alive = True
    def respawn(self, spacestation):
        dist = spacestation.width / 2 + 75
        angle = random.randint(0, 360)
        #angle = 90
        angle_rads = (angle) * math.pi / 180
        newx = spacestation.x + math.sin(angle_rads) * dist
        newy = spacestation.y + math.cos(angle_rads) * dist
        self.x = newx
        self.y = newy
        self.vel = 0
        self.accel = 0
        self.rotaccel = 0
        self.rotation = angle
        self.hull = self.maxhull
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
    def closestTarget(self, enemyships):
        closestship = None
        closestdist = math.inf
        for enemyship in enemyships:
            if not onScreen(enemyship, myship): continue
            dist = distance(enemyship, myship)
            if dist < closestdist:
                closestdist = dist
                closestship = enemyship.index
        self.targeted = closestship
    def attackerTarget(self):
        self.targeted = self.lastattacker
    def fireNextWeapon(self, enemyships, animations, sounds):
        dist = distance(self, enemyships[self.targeted])
        for weapon in self.weapons:
            if dist > weapon.range: continue
            charged = False
            if time.time() - weapon.lastfired >= weapon.chargetime:
                # weapon is charged

                weapon.lastfired = time.time()

                # fired weapon on target
                if enemyships[self.targeted].state != "attack_delay": enemyships[self.targeted].attackstart = time.time()
                enemyships[self.targeted].state = "attack_delay"

                enemyships[myship.targeted].hull -= 10
                pygame.mixer.Sound.play(sounds[0].mixer)
                if enemyships[myship.targeted].hull <= 0:
                    enemyships[myship.targeted].explode(animations)
                if enemyships[myship.targeted].hull <= 50 and enemyships[myship.targeted].state != "retreat":
                    enemyships[myship.targeted].state = "retreat"
                    enemyships[myship.targeted].startRetreat()
                enemyships[self.targeted].lastattacked = time.time()
                # add animation

                animation = Animation()
                animation.type = "laser"
                animation.colour = (255, 0, 0)
                animation.starttime = time.time()
                animation.endtime = time.time() + weapon.duration
                animation.startpos = (myship.x, myship.y)
                animation.endpos = (enemyships[self.targeted].x, enemyships[self.targeted].y)
                animations.append(animation)
    def explode(self, animations):
        self.vel = 0
        animation = Animation()
        animation.type = "explosion"
        animation.starttime = time.time()
        animation.endtime = time.time() + 0.25
        animation.startpos = (self.x, self.y)
        animation.targettype = "myship"
        animation.width = myship.width
        animations.append(animation)

def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = myfont.render(fps + " FPS", 1, pygame.Color("coral"))
    return fps_text

def get_fps():
    return int(clock.get_fps())


def detectKeyPresses(event_get, fullscreen, alt_pressed, enter_pressed, gameinfo, animations, sounds):
    for event in event_get:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
            if not fullscreen:
                screen = pygame.display.set_mode([width, height], pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode([width, height])
            fullscreen = not fullscreen
        if event.type == pygame.KEYDOWN:

            if (event.key == pygame.K_RALT or event.key == pygame.K_LALT):
                alt_pressed = True
            if event.key == pygame.K_RETURN:
                enter_pressed = True
            if gameinfo.alive:
                if event.key == pygame.K_t:
                    myship.nextTarget(enemyships)
                if event.key == pygame.K_c:
                    myship.closestTarget(enemyships)
                if event.key == pygame.K_r:
                    gameinfo.redalert = not gameinfo.redalert
                    if gameinfo.redalert == True:
                        gameinfo.timefactor = 0.5
                    else:
                        gameinfo.timefactor = 1
                if event.key == pygame.K_y:
                    myship.attackerTarget()
                if event.key == pygame.K_SPACE:
                   if myship.targeted != None:
                        myship.fireNextWeapon(enemyships, animations, sounds)
        # set alt and enter flags if the keys are pressed
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
    if gameinfo.alive:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            myship.rotaccel = -120
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            myship.rotaccel = 120
        else:
            myship.rotaccel = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            myship.accel = 250
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            myship.accel = -250
        else:
            myship.accel = 0
    if keys[pygame.K_ESCAPE]:
        sys.exit()
    if keys[pygame.K_SPACE]:
        pass
        #if myship.targeted != None:
         #   frameinfo.firingphasers = True
          #  frameinfo.phaserstart = time.time()

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
    centrex1 = ship1.x
    centrey1 = ship1.y
    centrex2 = ship2.x
    centrey2 = ship2.y
    return math.sqrt((abs(centrex1 - centrex2) ** 2) + (abs(centrey1 - centrey2) ** 2))

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

def drawTargetLine(screen, myship, enemyship, spacestation):
    # x1, y1 = point at edge of screen
    # x2, y2 = point which intersects with line between ships at (x1, y2 - 200)
    # x3, y3 = arrow one co-ord
    # x4, y4 = arrow two co-ord

    centre = (width / 2, height / 2)

    shiptype = enemyship.type
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
            lowest_dist = y_dist + width - height
    if enemyship.x >= myship.x:
        if x_dist >= lowest_dist:
            dir = "right"
            lowest_dist = x_dist
    if enemyship.y >= myship.y:
        if y_dist >= lowest_dist:
            dir = "top"
    x1, y1, x2, y2, x3, x4, y3, y4, m, c = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    dist = distance(myship, enemyship)
    a = 30 # arrow size
    # 10 + (distance / 30 * sensorrange_ships) # a goes from 10 to 30
    a = 10 + (1 - dist / myship.sensorrange_ships) * 20
    if enemyship.x - myship.x == 0: m = 0
    else: m = (enemyship.y - myship.y) / (enemyship.x - myship.x)
    if m == 0: m = 0.00001
    c = myship.y - m * myship.x
    if dir == "bottom":
        y1 = myship.y - height / 2 + 10
        x1 = (y1 - c) / m
        y2 = y1 + 150
        x2 = (y2 - c) / m
        x3 = x1 - a
        y3 = y1 + a
        x4 = x1 + a
        y4 = y1 + a
    elif dir == "top":
        y1 = myship.y + height / 2 - 10
        x1 = (y1 - c) / m
        y2 = y1 - 150
        x2 = (y2 - c) / m
        x3 = x1 - a
        y3 = y1 - a
        x4 = x1 + a
        y4 = y1 - a
    elif dir == "left":
        x1 = myship.x - width / 2 + 10
        y1 = m * x1 + c
        x2 = x1 + 150
        y2 = m * x2 + c
        x3 = x1 + a
        y3 = y1 + a
        x4 = x1 + a
        y4 = y1 - a
    elif dir == "right":
        x1 = myship.x + width / 2 - 10
        y1 = m * x1 + c
        x2 = x1 - 150
        y2 = m * x2 + c
        x3 = x1 - a
        y3 = y1 + a
        x4 = x1 - a
        y4 = y1 - a
    else: return
    draw_x1 = int(centre[0] + x1 - myship.x)
    draw_y1 = int(centre[1] - y1 + myship.y)
    draw_x2 = int(centre[0] + x2 - myship.x)
    draw_y2 = int(centre[1] - y2 + myship.y)
    draw_x3 = int(centre[0] + x3 - myship.x)
    draw_y3 = int(centre[1] - y3 + myship.y)
    draw_x4 = int(centre[0] + x4 - myship.x)
    draw_y4 = int(centre[1] - y4 + myship.y)

    colour = (192, 192, 192)
    if enemyship.type == "Space Station":
        colour = (0, 255, 0)
    elif enemyship.index == myship.targeted:
        colour = (0, 0, 192)

    #pygame.draw.line(screen, colour, (draw_x1, draw_y1), (draw_x2, draw_y2), 3)
    pygame.draw.line(screen, colour, (draw_x1, draw_y1), (draw_x3, draw_y3), 7)
    pygame.draw.line(screen, colour, (draw_x1, draw_y1), (draw_x4, draw_y4), 7)
    dist = distance(myship, enemyship)
    typeText = dir_label_font.render(shiptype, False, colour)
    distanceText = dir_label_font.render(str(int(dist)) + " km", False, colour)
    drawX_dist = -1000
    drawY_dist = -1000
    drawX_type = -1000
    drawY_type = -1000
    if dir == "top":
        drawX_dist = draw_x3 + 0
        drawY_dist = draw_y3 + 5
        drawX_type = draw_x3 + 0
        drawY_type = draw_y3 + 25
    if dir == "left":
        drawX_dist = draw_x3 + 5
        drawY_dist = draw_y3 + 0
        drawX_type = draw_x3 + 5
        drawY_type = draw_y3 + 20
    if dir == "bottom":
        drawX_dist = draw_x3 + 0
        drawY_dist = draw_y3 - 35
        drawX_type = draw_x3 + 0
        drawY_type = draw_y3 - 15
    if dir == "right":
        drawX_dist = draw_x3 - 105
        drawY_dist = draw_y3 + 0
        drawX_type = draw_x3 - 105
        drawY_type = draw_y3 + 20
    screen.blit(distanceText, (drawX_dist, drawY_dist))
    screen.blit(typeText, (drawX_type, drawY_type))

def enemyAITick(myship, enemyship, spacestation, animations, sounds):
    origstate = enemyship.state
    if enemyship.state == "retreat":
        if not myship.alive:
            enemyship.state = "patrol"
            return
        enemyship.fireNextWeapon(myship, animations, sounds)
        if enemyship.rotation != enemyship.patrolangle:
            enemyship.rotaccel = 120
        if abs(enemyship.patrolangle - enemyship.rotation) < 10:
            enemyship.rotation = enemyship.patrolangle
            enemyship.rotaccel = 0
        if enemyship.accel >= 0 and enemyship.vel >= enemyship.patrolspeed:
            enemyship.vel = enemyship.patrolspeed
            enemyship.accel = 0
        elif enemyship.accel < 0 and enemyship.vel <= enemyship.patrolspeed:
            enemyship.vel = enemyship.patrolspeed
            enemyship.accel = 0
        targetx = myship.x
        targety = myship.y
        dy = targety - enemyship.y
        dx = targetx - enemyship.x
        angle_deg = 360 - math.atan2(dy, dx) * 180 / math.pi - 90
        if angle_deg >= 180 and enemyship.rotaccel == 120:
            enemyship.rotaccel = -120
        enemyship.patrolangle = angle_deg
        if enemyship.patrolangle < 0: enemyship.patrolangle += 360
        if enemyship.patrolangle > 360: enemyship.patrolangle -= 360
        mypoint = Point()
        mypoint.x = enemyship.patrolstart[0]
        mypoint.y = enemyship.patrolstart[1]
        dist = distance(enemyship, mypoint)
        if dist >= enemyship.patroldist:
            enemyship.state == "patrol"
    if enemyship.state == "attack_delay":
        if not myship.alive:
            enemyship.state = "patrol"
            return
        if time.time() - enemyship.attackstart >= 1.0 or enemyship.substate == "attack":
            enemyship.state = "attack"
            enemyship.patrolspeed = random.randint(int(0.7 * enemyship.maxspeed), int(1 * enemyship.maxspeed))
            enemyship.patrolstart = [enemyship.x, enemyship.y]
            enemyship.accel = 250
            enemyship.rotaccel = 120
            targetx = myship.x + random.randint(-10,+10)
            targety = myship.y + random.randint(-10,+10)
            dy = targety - enemyship.y
            dx = targetx - enemyship.x
            angle_deg = 360 - math.atan2(dy, dx) * 180 / math.pi - 90
            if angle_deg >= 180:
                enemyship.rotaccel = -120
            enemyship.patrolangle = angle_deg
            if enemyship.patrolangle < 0: enemyship.patrolangle += 360
            if enemyship.patrolangle > 360: enemyship.patrolangle -= 360
            mypoint = Point()
            mypoint.x = targetx
            mypoint.y = targety
            dist = int(distance(enemyship, mypoint))
            enemyship.patroldist = dist - spacestation.radius - random.randint(30, 150)
    if enemyship.state == "attack":
        if not myship.alive:
            enemyship.state = "patrol"
            return
        enemyship.fireNextWeapon(myship, animations, sounds)
        #if enemyship.vel == 0 and enemyship.accel == 0:
        #    enemyship.startPatrol()
        if abs(enemyship.patrolangle - enemyship.rotation) < 10:
            enemyship.rotation = enemyship.patrolangle
            enemyship.rotaccel = 0
        if enemyship.rotation != enemyship.patrolangle:
            enemyship.rotaccel = 120
        if enemyship.accel >= 0 and enemyship.vel >= enemyship.patrolspeed:
            enemyship.vel = enemyship.patrolspeed
            enemyship.accel = 0
        elif enemyship.accel < 0 and enemyship.vel <= enemyship.patrolspeed:
            enemyship.vel = enemyship.patrolspeed
            enemyship.accel = 0
        targetx = myship.x + random.randint(-10, +10)
        targety = myship.y + random.randint(-10, +10)
        dy = targety - enemyship.y
        dx = targetx - enemyship.x
        angle_deg = 360 - math.atan2(dy, dx) * 180 / math.pi - 90 - 180
        if angle_deg >= 180:
            enemyship.rotaccel = -120
        enemyship.patrolangle = angle_deg
        if enemyship.patrolangle < 0: enemyship.patrolangle += 360
        if enemyship.patrolangle > 360: enemyship.patrolangle -= 360
        mypoint = Point()
        mypoint.x = enemyship.patrolstart[0]
        mypoint.y = enemyship.patrolstart[1]
        dist = distance(enemyship, mypoint)
        myshipdist = distance(enemyship, myship)
        if myshipdist >= 450:
            enemyship.patrolspeed = enemyship.maxspeed
        if myshipdist <= 250:
            enemyship.patrolspeed = myship.vel - 50
            if enemyship.patrolspeed >= enemyship.maxspeed: enemyship.patrolspeed = enemyship.maxspeed
        if enemyship.patrolspeed >= enemyship.vel:
            enemyship.accel = 250
        else:
            enemyship.accel = -250
        if dist >= enemyship.patroldist:
            pass
            #enemyship.state = "attack_delay"
            #if time.time() - enemyship.lastattacked >= 60.0:
             #   enemyship.state = "patrol"
              #  enemyship.startPatrol()
    if enemyship.state == "patrol":
        if enemyship.vel == 0 and enemyship.accel == 0:
            enemyship.startPatrol()
        if abs(enemyship.patrolangle - enemyship.rotation) < 10:
            enemyship.rotation = enemyship.patrolangle
            enemyship.rotaccel = 0
        #if enemyship.rotation != enemyship.patrolangle:
            #enemyship.rotaccel = 120
        if enemyship.vel >= enemyship.patrolspeed:
            enemyship.vel = enemyship.patrolspeed
            enemyship.accel = 0
        mypoint = Point()
        mypoint.x = enemyship.patrolstart[0]
        mypoint.y = enemyship.patrolstart[1]
        dist = distance(enemyship, mypoint)
        if dist >= enemyship.patroldist:
            enemyship.vel = 0
            enemyship.accel = 0
            if random.randint(0,3) == 0:
                enemyship.state = "gotostation"
                enemyship.startGoToStation(spacestation)
    elif enemyship.state == "leavestation_rot":
        if abs(enemyship.patrolangle - enemyship.rotation) < 10:
            enemyship.rotation = enemyship.patrolangle
            enemyship.rotaccel = 0
            enemyship.state = "leavestation_fly"
            enemyship.startLeaveStation_fly()
        if enemyship.rotation != enemyship.patrolangle:
            enemyship.rotaccel = 120
    elif enemyship.state == "leavestation_fly":
        if enemyship.vel >= enemyship.patrolspeed:
            enemyship.vel = enemyship.patrolspeed
            enemyship.accel = 0
        mypoint = Point()
        mypoint.x = enemyship.patrolstart[0]
        mypoint.y = enemyship.patrolstart[1]
        dist = distance(enemyship, mypoint)
        if dist >= enemyship.patroldist:
            enemyship.vel = 0
            enemyship.accel = 0
            enemyship.state = "patrol"
    elif enemyship.state == "gotostation":
        if abs(enemyship.patrolangle - enemyship.rotation) < 10:
            enemyship.rotation = enemyship.patrolangle
            enemyship.rotaccel = 0
        if enemyship.rotation != enemyship.patrolangle:
            enemyship.rotaccel = 120
        if enemyship.vel >= enemyship.patrolspeed:
            enemyship.vel = enemyship.patrolspeed
            enemyship.accel = 0
        mypoint = Point()
        mypoint.x = enemyship.patrolstart[0]
        mypoint.y = enemyship.patrolstart[1]
        dist = distance(enemyship, mypoint)
        if dist >= enemyship.patroldist:
            enemyship.vel = 0
            enemyship.accel = 0
            enemyship.rotaccel = 0
            enemyship.state = "gotostation_rest"
            enemyship.reststart = time.time()
            enemyship.resttime = random.randint(1, 20)
    elif enemyship.state == "gotostation_rest":
        time_elapsed = time.time() - enemyship.reststart
        if time_elapsed >= enemyship.resttime:
            enemyship.vel = 0
            enemyship.accel = 0
            enemyship.state = "leavestation_rot"
            enemyship.x = enemyship.lastx
            enemyship.y = enemyship.lasty
            enemyship.startLeaveStation_rot()
    enemyship.substate = origstate

def physicsTick(myship, enemyships, spacestation, time_since_phys_tick, gameinfo):

    timefactor = gameinfo.timefactor
    # Calculate new position
    myship.rotation += myship.rotaccel * time_since_phys_tick * timefactor
    spacestation.rotation += 15 * time_since_phys_tick * timefactor
    if myship.rotation > 360: myship.rotation -= 360
    if myship.rotation < 0: myship.rotation += 360
    rotation_rads = myship.rotation * math.pi / 180
    myship.vel = myship.vel + myship.accel * time_since_phys_tick * timefactor
    if myship.vel >= 500: myship.vel = 500
    if myship.vel <= 0: myship.vel = 0
    myship.lastx = myship.x
    myship.lasty = myship.y
    myship.x += (myship.vel) * math.sin(rotation_rads) * time_since_phys_tick * timefactor
    myship.y += (myship.vel) * math.cos(rotation_rads) * time_since_phys_tick * timefactor
    # enemy ships

    for enemyship in enemyships:
        enemyship.rotation += enemyship.rotaccel * time_since_phys_tick * timefactor
        if enemyship.rotation > 360: enemyship.rotation -= 360
        if enemyship.rotation < 0: enemyship.rotation += 360
        enemyship.totrotations += enemyship.rotaccel * time_since_phys_tick * timefactor
        rotation_rads = enemyship.rotation * math.pi / 180
        enemyship.vel = enemyship.vel + enemyship.accel * time_since_phys_tick * timefactor
        if enemyship.vel >= 500: enemyship.vel = 500
        if enemyship.vel <= 0: enemyship.vel = 0
        enemyship.lastx = enemyship.x
        enemyship.lasty = enemyship.y
        enemyship.x += (enemyship.vel) * math.sin(rotation_rads) * time_since_phys_tick * timefactor
        enemyship.y += (enemyship.vel) * math.cos(rotation_rads) * time_since_phys_tick * timefactor



def renderFrame(screen, stars, myship, enemyships, spacestation, frameinfo, shipIMG, enemyshipIMG, spacestationIMG):

    # Fill the background with white
    screen.fill((0, 0, 0))

    drawStars(screen, stars, myship)

    # Calculate centre

    centre = (width / 2, height / 2)

    i = -1
    enemytotarget = False
    targeteddrawX = 0
    targeteddrawY = 0
    targetedenemy = None
    for enemyship in enemyships:
        i += 1
        dist = distance(myship, enemyship)
        if enemyship.visible and myship.targeted == i:
            enemydrawX = centre[0] + enemyship.x - myship.x
            enemydrawY = centre[1] - enemyship.y + myship.y
            margin = 10
            pygame.draw.rect(screen, (255, 0, 0),
                             (enemydrawX - enemyship.width / 2 - 5, enemydrawY - enemyship.width / 2 - 5, enemyship.width + margin,
            enemyship.width + margin), 2)
            targeteddrawX = enemydrawX
            targeteddrawY = enemydrawY
            enemytotarget = True
            targetedenemy = enemyship

        if dist > 2000: continue
        if (not onScreen(enemyship, myship)):
            drawTargetLine(screen, myship, enemyship, spacestation)
            continue
        # Draw enemy ship
        enemydrawX = centre[0] + enemyship.x - myship.x
        enemydrawY = centre[1] - enemyship.y + myship.y
        if enemyship.visible:
            #screen.blit(enemyshipIMG, (enemydrawX, enemydrawY))
            es_centre = (enemydrawX, enemydrawY)
            (newIMG, es_centre) = rot_center(enemyship.shipIMG, enemyship.rotation, es_centre[0],
                                              es_centre[1])  # rotate ship appropriately
            screen.blit(newIMG, es_centre)
            #thisfont = pygame.font.SysFont('Fixedsys', 16)
            #indexText = thisfont.render(str(i), False, (255, 255, 255))
            #distanceText = thisfont.render(str(int(dist)), False, (255, 255, 255))
            #xyText = thisfont.render("xy: (" + str(int(enemyship.x)) + "," + str(int(enemyship.y)) + ")", False, (255, 255, 255))
            #screen.blit(indexText, (enemydrawX - 10, enemydrawY - 10))
            #screen.blit(distanceText, (enemydrawX - 10, enemydrawY + 20))
            #screen.blit(xyText, (enemydrawX - 10, enemydrawY + 50))

    # Draw space station
    spacestationX = centre[0] + spacestation.x - myship.x
    spacestationY = centre[1] - spacestation.y + myship.y
    dist = distance(myship, spacestation)
    if onScreen(spacestation, myship): # on screen
        (spacestationIMG, spacestationcentre) = rot_center(spacestationIMG, spacestation.rotation, spacestationX, spacestationY)
        screen.blit(spacestationIMG, spacestationcentre)
        spacestation.centre = spacestationcentre
    elif dist < 5000: # not on screen and within short range sensor range
        drawTargetLine(screen, myship, spacestation, spacestation)
    # Draw lasers
    '''
    if frameinfo.firingphasers and enemytotarget:
        pygame.draw.line(screen, (255, 0, 0), (centre[0], centre[1]), (targeteddrawX - enemyships[myship.targeted].width / 2 + 30, targeteddrawY - enemyships[myship.targeted].width / 2 + 30), 4)
        if (time.time() - frameinfo.phaserstart > 0.03):
            frameinfo.firingphasers = False
            targetedenemy.hull -= 10

    if frameinfo.enemyexploding and myship.targeted is not None:
        time_elapsed = time.time() - frameinfo.explodestart
        if time_elapsed >= 0.25:
            frameinfo.enemyexploding = False
            if targetedenemy.objtype == "enemy": targetedenemy.visible = False
            myship.targeted = None
            enemyships.pop(targetedenemy.index)
        else:
            circlesize = 160 * (0.25 - time_elapsed)
            pygame.draw.circle(screen, (255, 50, 50), (targeteddrawX - enemyships[myship.targeted].width / 2 + 30, targeteddrawY - enemyships[myship.targeted].width / 2 + 30), circlesize)

    if targetedenemy != None and targetedenemy.visible and not frameinfo.enemyexploding and targetedenemy.hull <= 0:
        frameinfo.enemyexploding = True
        frameinfo.explodestart = time.time()
    '''
    # Draw ship

    (shipIMG, newcentre) = rot_center(shipIMG, myship.rotation, centre[0], centre[1]) # rotate ship appropriately
    if myship.alive: screen.blit(shipIMG, newcentre)

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

    centre = (width / 2, height / 2)
    #enemyshipIMG = pygame.image.load(os.path.join('images', 'enemyship.png')).convert_alpha()
    #screen.blit(enemyshipIMG, (drawX, drawY))
    #screen.set_at((int(drawX), int(drawY)), (255, 255, 0))
    if gameinfo.redalert:
        redalert_text = myfont.render("Red Alert", 1, (255, 0, 0))
        screen.blit(redalert_text, (80, 5))
    i = -1
    for animation in animations:
        i+=1
        drawX = targeteddrawX
        drawY = targeteddrawY
        if animation.targettype == "myship":
            drawX = centre[0]
            drawY = centre[1]
        if animation.type == "laser":
            # draw red line for duration
            if time.time() >= animation.endtime:
                animations.pop(i)
                break
            enemydrawX = centre[0] + animation.endpos[0] - myship.x
            enemydrawY = centre[1] - animation.endpos[1] + myship.y
            pygame.draw.line(screen, animation.colour, (centre[0], centre[1]), (
            enemydrawX - enemyships[0].width / 2 + 30,
            enemydrawY - enemyships[0].width / 2 + 30), 4)
        if animation.type == "explosion":
            time_elapsed = time.time() - animation.starttime
            if time.time() >= animation.endtime:
                if animation.targettype != "myship": enemyships.pop(enemyships[myship.targeted].index)
                animations.pop(i)
                reIndexEnemies(enemyships)
                myship.targeted = None
                break
            circlesize = 160 * (0.25 - time_elapsed)
            pygame.draw.circle(screen, (255, 50, 50), (drawX - animation.width / 2 + 30,
                                                      drawY - animation.width / 2 + 30),
                               circlesize)

def reIndexEnemies(enemyships):
    i = -1
    for enemyship in enemyships:
        i+=1
        enemyship.index = i

def objectCollisionDetection(object1, object2):
    '''
    obj1_centre_x = object1.x
    obj1_centre_y = object1.y
    obj2_centre_x = object2.x
    obj2_centre_y = object2.y
    dx = obj1_centre_x - obj2_centre_x
    dy = obj1_centre_y - obj2_centre_y
    dist = math.sqrt(dx * dx + dy * dy)
    '''
    dist = distance(object1, object2)
    if dist < object1.radius + object2.radius:
        return True
    return False

def collisionDetection(myship, enemyships, spacestation):
    for enemyship in enemyships:
        if objectCollisionDetection(enemyship, spacestation):
            enemyship.vel = 0
            enemyship.accel = 0
            enemyship.substate = enemyship.state
            enemyship.state = "leavestation_rot"
            enemyship.x = enemyship.lastx
            enemyship.y = enemyship.lasty
            enemyship.startLeaveStation_rot()
    if objectCollisionDetection(myship, spacestation):
        myship.vel = 0
        myship.accel = 0
        myship.x = myship.lastx
        myship.y = myship.lasty



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

animations = []
music = []
sounds = []

path = 'music'

files = os.listdir(path)

i = -1
for f in files:
    i+=1
    music.append(Music())
    music[i].file = os.path.join('music', f)

sounds.append(Sound())
i = len(sounds) - 1
sounds[i].file = os.path.join('sounds', 'Laser-Shot-1.mp3')
sounds[i].mixer = pygame.mixer.Sound(sounds[i].file)


music_track = random.randint(0,len(music) - 1)
music_playing = music[music_track]
pygame.mixer.music.load(music_playing.file)
pygame.mixer.music.play(-100000)

# create game info

gameinfo = GameInfo()


# create space station object

spacestation = SpaceStation()

# create my ship object

myship = MyShip()
myship.weapons.append(Weapon())
myship.weapons[0].type = "laser"
myship.weapons[0].duration = 0.02
myship.weapons[0].chargetime = 0.5
myship.weapons[0].lastfired = 0
myship.weapons[0].range = 600
myship.respawn(spacestation)

# spawn enemies

enemyships = []
for i in range(200):
    enemyships.append(EnemyShip())
    enemyships[i].weapons.append(Weapon())
    enemyships[i].weapons[0].type = "laser"
    enemyships[i].weapons[0].duration = 0.02
    enemyships[i].weapons[0].chargetime = 1.0
    enemyships[i].weapons[0].lastfired = 0
    enemyships[i].weapons[0].range = 600
    #enemyships[i].x = 200
    #enemyships[i].y = 200
    enemyships[i].x = random.randint(-10000, 10000)
    enemyships[i].y = random.randint(-10000, 10000)
    enemyships[i].index = i
    enemyships[i].state = "patrol"
    enemyships[i].startPatrol()
    enemyships[i].patroldist = 20
    '''
    r = random.randint(1, 2)
    if r == 1:
        enemyships[i].x = spacestation.x + 1000 + random.randint(-3000, 3000)
        enemyships[i].y = spacestation.y + 1000 + random.randint(-3000, 3000)
    else:
        enemyships[i].x = -spacestation.x - 1000 + random.randint(-3000, 3000)
        enemyships[i].y = spacestation.y - 1000 + random.randint(-3000, 3000)
    '''
    enemyships[i].shipIMG = pygame.image.load(os.path.join('images', 'enemyship.png')).convert_alpha()

#enemyship = EnemyShip()

frameinfo = FrameInfo()
# Run until the user asks to quit
running = True
i = 0
curfps = 0
alt_pressed = False
enter_pressed = False
last_phys_tick = time.time()
last_keys_poll = time.time()

# main game loop

while running:
    i+= 1
    if not gameinfo.alive:
        time_since_died = time.time() - gameinfo.lastdied
        if time_since_died >= 5:
            gameinfo.alive = True
            myship.alive = True
            myship.respawn(spacestation)
    time_since_key_poll = time.time() - last_keys_poll
    detectKeyPresses(pygame.event.get(), fullscreen, alt_pressed, enter_pressed, gameinfo, animations, sounds)
    cur_time = time.time()
    time_since_phys_tick = cur_time - last_phys_tick
    physicsTick(myship, enemyships, spacestation, time_since_phys_tick, gameinfo)
    last_phys_tick = cur_time
    collisionDetection(myship, enemyships, spacestation)
    for enemyship in enemyships:
        enemyAITick(myship,enemyship, spacestation, animations, sounds)

    renderFrame(screen, stars, myship, enemyships, spacestation, frameinfo, shipIMG, enemyshipIMG, spacestationIMG)
    dy = myship.y - spacestation.y
    dx = myship.x - spacestation.x
    angle_deg = 360 - math.atan2(dy, dx) * 180 / math.pi - 90
    clock.tick(165)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()