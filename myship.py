import random
import time
import math
import render
import functions
import pygame
from classes import Animation

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

                enemyships[self.targeted].hull -= 10
                pygame.mixer.Sound.play(sounds[0].mixer)
                if enemyships[self.targeted].hull <= 0:
                    enemyships[self.targeted].explode(animations)
                if enemyships[self.targeted].hull <= 50 and enemyships[self.targeted].state != "retreat":
                    enemyships[self.targeted].state = "retreat"
                    enemyships[self.targeted].startRetreat(self)
                enemyships[self.targeted].lastattacked = time.time()
                # add animation

                animation = Animation()
                animation.type = "laser"
                animation.colour = (255, 0, 0)
                animation.starttime = time.time()
                animation.endtime = time.time() + weapon.duration
                animation.startpos = (self.x, self.y)
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
        animation.width = self.width
        animations.append(animation)