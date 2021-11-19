import random
import time
import math
import functions
import pygame
import os
from classes import Animation, Point, Weapon, Shield

class EnemyShip():
    def __init__(self):
        self.objtype = "enemy"
        self.hull = 100
        self.maxhull = 100
        self.x = 800
        self.y = 800
        self.visible = True
        self.width = 90
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
        self.gridsector = 0
        self.shields = []
        self.lastveltested = 0
        self.lastvel = 0
    def startPatrol(self):
        self.totrotations = 0
        self.accel = 250
        self.rotaccel = 120
        if random.randint(0,1) == 0:
            self.rotaccel = -120
        self.patrolstart = [self.x, self.y]
        self.patrolangle = random.randint(-360, 360)
        self.origangle = self.patrolangle
        self.patroltotrotations = abs(self.patrolangle - self.rotation)
        self.patrolangle = functions.clampAngle(self.patrolangle)
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
        self.patrolangle = functions.clampAngle(self.patrolangle)
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
        angle_deg = functions.angleBetween(self, spacestation) - 90
        self.patrolangle = angle_deg
        self.origangle = self.patrolangle
        self.patroltotrotations = abs(self.patrolangle - self.rotation)
        self.patrolangle = functions.clampAngle(self.patrolangle)
        mypoint = Point()
        mypoint.x = spacestation.x
        mypoint.y = spacestation.y
        dist = int(functions.distance(self, mypoint))
        self.patroldist = dist - spacestation.radius - random.randint(30,150)
        self.patrolspeed = random.randint(120, 300)
    def closestStation(self, spacestations):
        closestdist = math.inf
        closeststation = None
        i = -1
        for station in spacestations:
            i += 1
            dist = functions.distance(station, self)
            if dist < closestdist:
                closestdist = dist
                closeststation = station
        return closeststation
    def startRetreat(self, myship):
        self.patrolspeed = self.maxspeed
        self.patrolstart = [self.x, self.y]
        self.patroldist = 5000
        self.accel = 250
        angle_deg = functions.angleBetween(self, myship) - 90 - 180
        self.patrolangle = angle_deg
        self.rotaccel = 120
        if angle_deg >= 180:
            self.rotaccel = -120
    def startMakeDistance(self):
        self.state = "attack_makedistance"
        self.patrolspeed = random.randint(int(0.7 * self.maxspeed), int(1 * self.maxspeed))
        self.patrolstart = [self.x, self.y]
        self.accel = 250
        self.rotaccel = 120
        targetx = self.x + random.randint(-1300, 1300)
        targety = self.y + random.randint(-1300, 1300)
        dy = targety - self.y
        dx = targetx - self.x
        angle_deg = 360 - math.atan2(dy, dx) * 180 / math.pi - 90
        if angle_deg >= 180:
            self.rotaccel = -120
        self.patrolangle = angle_deg
        if self.patrolangle < 0: self.patrolangle += 360
        if self.patrolangle > 360: self.patrolangle -= 360
        mypoint = Point()
        mypoint.x = targetx
        mypoint.y = targety
        dist = int(functions.distance(self, mypoint))
        self.patroldist = 200
    def explode(self, animations):
        self.vel = 0
        animation = Animation()
        animation.type = "explosion"
        animation.starttime = time.time()
        animation.endtime = time.time() + 0.25
        animation.startpos = (self.x, self.y)
        animation.targettype = "enemyship"
        animation.width = self.width
        animation.hitship = self
        animations.append(animation)

    def fireNextWeapon(self, myship, animations, sounds, gameinfo, spacestations):
        dist = functions.distance(self, myship)
        for weapon in self.weapons:
            if dist > weapon.range: continue
            closeststation = self.closestStation(spacestations)
            if functions.distance(self, closeststation) <= closeststation.width / 2 + 400: continue
            if functions.distance(myship, closeststation) <= closeststation.width / 2 + 400: continue
            if time.time() - weapon.lastfired >= weapon.chargetime:
                # weapon is charged

                weapon.lastfired = time.time()
                #pygame.mixer.Sound.play(sounds[0].mixer)
                # fired weapon on target

                myship.lastattacker = self.index
                # add animation
                angle_deg = functions.angleBetween(myship, self)
                angle_deg += 90
                if weapon.type == "laser":
                    angle_deg = angle_deg - 90
                animation = Animation()
                chance_of_miss = 0
                if weapon.type == "laser": chance_of_miss = 50
                if weapon.type == "bullet": chance_of_miss = 50
                if weapon.type == "torpedo": chance_of_miss = 50
                if weapon.type == "fluxray" or weapon.type == "disruptor": chance_of_miss = 0
                if random.randint(1,100) <= chance_of_miss:
                    if weapon.type == "bullet": continue
                    rand = random.randint(0,1)
                    if rand == 0:
                        angle_deg += random.randint(15, 60)
                    elif rand == 1:
                        angle_deg -= random.randint(15, 60)
                angle_rads = angle_deg * math.pi / 180
                animation.angle = angle_deg
                animation.type = weapon.type
                animation.colour = (255, 0, 0)
                animation.starttime = time.time()
                animation.endtime = time.time() + weapon.duration
                animation.startpos = (self.x, self.y)
                animation.duration = weapon.duration
                animation.damage = weapon.damage
                animation.classnum = weapon.classnum
                animation.endpos[0] = self.x + math.cos(angle_rads) * weapon.range
                animation.endpos[1] = self.y - math.sin(angle_rads) * weapon.range
                animation.x = self.x
                animation.y = self.y
                animation.targetship = self
                animation.target = self
                animation.firer = "enemyship"
                animation.velocity = weapon.velocity
                animation.imgrot = animation.angle
                if animation.type == "laser" or animation.type == "fluxray" or animation.type == "disruptor":
                    r = myship.width / 2 + 10
                    x5 = myship.x
                    y5 = myship.y
                    x3 = animation.endpos[0] - x5
                    y3 = animation.endpos[1] - y5
                    x4 = self.x - x5
                    y4 = self.y - y5
                    intercept = functions.lineCircleIntercept(x3, y3, x4, y4, x5, y5, r)
                    animation.missed = True
                    if intercept != None:
                        animation.missed = False
                if animation.type == "fluxray" or animation.type == "disruptor":
                    animation.angle -= 90
                animations.append(animation)
                break
