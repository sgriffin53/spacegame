import random
import time
import math
import render
import functions
import pygame
from classes import Animation, Point

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
        dist = int(functions.distance(self, mypoint))
        self.patroldist = dist - spacestation.radius - random.randint(30,150)
        #r = random.randint(1,2)
        #if r == 1:
         #   self.patroldist += random.randint(20, 50)
        #elif r == 2:
            #self.patroldist -= random.randint(20, 50)
        self.patrolspeed = random.randint(120, 300)
    def startRetreat(self, myship):
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
        animation.width = self.width
        animations.append(animation)

    def fireNextWeapon(self, myship, animations, sounds, gameinfo):
        dist = functions.distance(self, myship)
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