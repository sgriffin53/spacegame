import random
import time
import math
import render
import functions
import pygame
import math
from classes import Animation, Point
import collision

class MyShip():
    def __init__(self):
        self.hull = 500
        self.maxhull = 500
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
        self.autostate = None
        self.warping = False
        self.warpdist = 0
        self.warpangle = 0
        self.warpdist = 0
        self.warpstart = [0,0]
        self.gridsector = 0
        self.allowedsectors = []
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
            dist = functions.distance(self, next_target)
            if dist > 2000:
                continue
            else:
                self.targeted = tgt - 1
                break
    def closestTarget(self, enemyships, gameinfo):
        closestship = None
        closestdist = math.inf
        for enemyship in enemyships:
            if not render.onScreen(enemyship, self, gameinfo): continue
            dist = functions.distance(enemyship, self)
            if dist < closestdist:
                closestdist = dist
                closestship = enemyship.index
        self.targeted = closestship
    def attackerTarget(self):
        self.targeted = self.lastattacker
    def fireNextWeapon(self, enemyships, animations, sounds):
        dist = functions.distance(self, enemyships[self.targeted])
        for weapon in self.weapons:
            if dist > weapon.range: continue
            charged = False
            if time.time() - weapon.lastfired >= weapon.chargetime:
                # weapon is charged

                weapon.lastfired = time.time()

                # fired weapon on target
                if enemyships[self.targeted].state != "attack_delay": enemyships[self.targeted].attackstart = time.time()
                enemyships[self.targeted].state = "attack_delay"

                if weapon.type == "laser": enemyships[self.targeted].hull -= 10
                pygame.mixer.Sound.play(sounds[0].mixer)
                if enemyships[self.targeted].hull <= 0:
                    enemyships[self.targeted].explode(animations)
                if enemyships[self.targeted].hull <= 50 and enemyships[self.targeted].state != "retreat":
                    enemyships[self.targeted].state = "retreat"
                    enemyships[self.targeted].startRetreat(self)
                enemyships[self.targeted].lastattacked = time.time()
                # add animation

                animation = Animation()
                animation.type = weapon.type
                animation.colour = (255, 0, 0)
                animation.starttime = time.time()
                animation.endtime = time.time() + weapon.duration
                animation.duration = weapon.duration
                animation.startpos = (self.x, self.y)
                animation.endpos = (enemyships[self.targeted].x, enemyships[self.targeted].y)
                animation.targetship = enemyships[self.targeted]
                animation.firer = "myship"
                animation.target = enemyships[self.targeted]
                animations.append(animation)
                break
    def explode(self, animations):
        self.vel = 0
        animation = Animation()
        animation.type = "explosion"
        animation.starttime = time.time()
        animation.endtime = time.time() + 0.25
        animation.startpos = (self.x, self.y)
        animation.targettype = "myship"
        animation.width = self.width
        animations.append(animation)
    def autoTick(self, gameinfo, spacestations):
        if self.autostate == "warp_rot":
            if abs(self.warpangle - self.rotation) < 10:
                self.rotation = self.warpangle
                self.rotaccel = 0
                self.autostate = "warp_fly"
                self.warpstart = [self.x, self.y]
                self.warpdist = functions.distance(spacestations[gameinfo.selectedstation], self) - 700
                self.vel = 200000
        if self.autostate == "warp_fly":
            point1 = Point()
            point1.x = self.warpstart[0]
            point1.y = self.warpstart[1]
            dist = functions.distance(point1, self)
            if dist > self.warpdist:
                if (collision.objectCollisionDetection(self, spacestations[gameinfo.selectedstation])):
                    self.x = spacestations[gameinfo.selectedstation].x - 700
                    self.y = spacestations[gameinfo.selectedstation].y - 700
                self.autostate = None
                self.warping = False
                self.vel = 0
    def startWarpRot(self, spacestation):
        self.autostate = "warp_rot"
        self.vel = 0
        self.rotaccel = 120
        targetx = self.x
        targety = self.y
        dy = targety - spacestation.y
        dx = targetx - spacestation.x
        angle_deg = 360 - math.atan2(dy, dx) * 180 / math.pi - 90
        if angle_deg > 360: angle_deg -= 360
        if angle_deg < 0: angle_deg += 360
        if abs(angle_deg - self.rotation) >= 180:
            self.rotaccel = -120

        self.warpangle = angle_deg
        if self.warpangle > 360: self.warpangle -= 360
        if self.warpangle < 0: self.warpangle += 360
        '''
        mypoint = Point()
        mypoint.x = spacestation.x
        mypoint.y = spacestation.y
        dist = int(functions.distance(self, mypoint))
        self.warpdist = dist - spacestation.radius - random.randint(30, 150)
        '''