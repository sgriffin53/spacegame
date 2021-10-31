import random
import time
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
        self.shields = []
        self.image = None
        self.turretrot = 0
        self.turretrotaccel = 0
        self.turrentpos = (0, 0)
    def respawn(self, spacestation):
        dist = spacestation.width / 2 + 75
        angle = random.randint(0, 360)
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
        for shield in self.shields:
            shield.charge = shield.maxcharge
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
    def fireNextWeapon(self, enemyships, animations, sounds, spacestations):
       # dist = functions.distance(self, enemyships[self.targeted])
        for weapon in self.weapons:
            if weapon == None: continue
            for animation in animations:
                if animation.firer == "myship":
                    break
            if time.time() - weapon.lastfired >= weapon.chargetime:

                # weapon is charged
                weapon.lastfired = time.time()

                # use this code for when we hit a ship with a weapon
                pygame.mixer.Sound.play(sounds[0].mixer)

                # add animation

                animation = Animation()
                animation.type = weapon.type
                animation.colour = (0, 255, 0)
                animation.starttime = time.time()
                animation.endtime = time.time() + weapon.duration
                animation.duration = weapon.duration
                animation.startpos = self.turrentpos
                animation.range = weapon.range
                endpos = [0, 0]
                turret_ang_rads = self.turretrot * math.pi / 180

                endpos[0] = self.x + math.cos(turret_ang_rads) * weapon.range
                endpos[1] = self.y - math.sin(turret_ang_rads) * weapon.range
                animation.endpos = endpos
                animation.firer = "myship"
                animation.damage = weapon.damage
                animation.classnum = weapon.classnum
                animations.append(animation)
                closesthit = None
                closesthit_dist = 99999999999999
                for enemyship in enemyships:
                    dist = functions.distance(self, enemyship)
                    if dist > 2000: continue
                    endpos = animation.endpos
                    r = enemyship.width / 2 + 10
                    # x ^ 2 + b x + c
                    x5 = enemyship.x
                    y5 = enemyship.y
                    x3 = endpos[0] - x5
                    y3 = endpos[1] - y5
                    x4 = self.x - x5
                    y4 = self.y - y5
                    dx = x4 - x3
                    dy = y4 - y3
                    dr = math.sqrt(dx ** 2 + dy ** 2)
                    D = x3 * y4 - x4 * y3
                    discriminant = r ** 2 * dr ** 2 - D ** 2
                    if discriminant >= 0:
                        # laser line intersects shield circle
                        mypoint = Point()
                        sgn = -1
                        if dy > 0: sgn = 1
                        x1 = (D * dy + sgn * dx * math.sqrt(discriminant)) / dr ** 2
                        x2 = (D * dy - sgn * dx * math.sqrt(discriminant)) / dr ** 2
                        y1 = (-D * dx + abs(dy) * math.sqrt(discriminant)) / dr ** 2
                        y2 = (-D * dx - abs(dy) * math.sqrt(discriminant)) / dr ** 2
                        x1 += x5
                        y1 += y5
                        x2 += x5
                        y2 += y5
                        x3 += x5
                        y3 += y5
                        x4 += x5
                        y4 += y5
                        mypoint.x = x1
                        mypoint.y = y1
                        dist1 = functions.distance(mypoint, self)
                        mypoint2 = Point()
                        mypoint2.x = x2
                        mypoint2.y = y2
                        dist2 = functions.distance(mypoint2, self)
                        pointA = Point()
                        pointB = Point()
                        pointC = Point()
                        pointA.x = x3
                        pointA.y = y3
                        pointB.x = x4
                        pointB.y = y4
                        pointC.x = x1
                        pointC.y = y1
                        if not functions.isBetween(pointA, pointB, pointC):
                            continue
                        pointC.x = x2
                        pointC.y = y2
                        if not functions.isBetween(pointA, pointB, pointC):
                            continue
                        if dist1 < closesthit_dist:
                            closesthit_dist = dist1
                            closesthit = mypoint
                            animation.hitship = enemyship
                        if dist2 < closesthit_dist:
                            closesthit_dist = dist2
                            closesthit = mypoint2
                            animation.hitship = enemyship
                if closesthit != None:
                    animation.hitpoint = [closesthit.x, closesthit.y]
                    animation.angle = functions.angleBetween(closesthit, self)
                    enemyship = animation.hitship
                    angle = 360 - (animation.angle) + 90 + enemyship.rotation
                    angle = functions.clampAngle(angle)
                    shieldnum = int(((angle + 45) / 360) * 4)
                    if angle <= 45: shieldnum = 0
                    if angle >= 315: shieldnum = 0
                    if shieldnum >= 4: shieldnum = 3
                    shieldcharge = enemyship.shields[shieldnum].charge
                    if enemyship.state != "attack" and enemyship.state != "attack_delay":
                        enemyship.state = "attack_delay"
                    if shieldcharge <= 0:
                        enemyship.hull -= 10
                        if enemyship.hull <= 50 and enemyship.state != "retreat":
                            enemyship.state = "retreat"
                            enemyship.startRetreat(enemyship)
                        if enemyship.hull <= 0:
                            enemyship.explode(animations)
                    else:
                        enemyship.shields[shieldnum].charge -= 20
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
    def startWarpRot(self, spacestation):
        self.autostate = "warp_rot"
        self.vel = 0
        self.rotaccel = 120
        angle_deg = functions.angleBetween(self, spacestation) - 90
        angle_deg = functions.clampAngle(angle_deg)
        if abs(angle_deg - self.rotation) >= 180:
            self.rotaccel = -120
        self.warpangle = angle_deg
        self.warpangle = functions.clampAngle(self.warpangle)
    def repair(self, gameinfo):
        repaircost = functions.repairCost(self)
        if repaircost == 0:
            gameinfo.messages[0].visible = True
            gameinfo.messages[0].message = "No Repairs Needed"
        elif gameinfo.credits < repaircost:
            gameinfo.messages[0].visible = True
            gameinfo.messages[0].message = "Cannot Afford repairs"
        else:
            for i in range(4): self.shields[i].charge = self.shields[i].maxcharge
            self.hull = self.maxhull
            gameinfo.messages[0].visible = True
            gameinfo.messages[0].message = "Ship repaired"
            gameinfo.credits -= repaircost