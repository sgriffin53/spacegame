import math
import functions
import pygame
from classes import Point
import time

def physicsTick(myship, enemyships, spacestations, time_since_phys_tick, gameinfo, animations):
    if gameinfo.screen == "game":
        allowedSectors = myship.allowedsectors

        timefactor = gameinfo.timefactor
        # Calculate new position
        if myship.rotaccel != 0:
            myship.rotation += myship.rotaccel * time_since_phys_tick * timefactor
            if myship.rotation > 360: myship.rotation -= 360
            if myship.rotation < 0: myship.rotation += 360
        rotation_rads = myship.rotation * math.pi / 180
        if myship.turretrotaccel != 0:
            myship.turretrot += myship.turretrotaccel * time_since_phys_tick * timefactor
            if myship.turretrot > 360: myship.turretrot -= 360
            if myship.turretrot < 0: myship.turretrot += 360
        if myship.accel != 0:
            myship.vel = myship.vel + myship.accel * time_since_phys_tick * timefactor
            if not myship.warping:
                if myship.vel >= 500: myship.vel = 500
                if myship.vel <= 0: myship.vel = 0
        myship.lastx = myship.x
        myship.lasty = myship.y
        lastsector = myship.gridsector
        myship.x += (myship.vel) * math.sin(rotation_rads) * time_since_phys_tick * timefactor
        myship.y += (myship.vel) * math.cos(rotation_rads) * time_since_phys_tick * timefactor
        myship.gridsector = functions.gridSector(myship)

        # set ship turret

        mousepos = pygame.mouse.get_pos()
        mousePoint = Point()
        centre = (gameinfo.width / 2, gameinfo.height / 2)
        mouseX = - mousepos[0] + myship.x + centre[0]
        mouseY = + mousepos[1] + myship.y - centre[1]
        mousePoint.x = mouseX
        mousePoint.y = mouseY
        myship.turretrot = functions.angleBetween(myship, mousePoint)
        myship.turretrot = functions.clampAngle(myship.turretrot)

        if myship.gridsector != lastsector or myship.allowedsectors == []: myship.allowedsectors = functions.allowedSectors(myship.gridsector)
        # enemy ships

        for enemyship in enemyships:
            enemyship.gridsector = functions.gridSector(enemyship)
            enemysector = enemyship.gridsector
            if enemysector not in allowedSectors: continue
            if enemyship.rotaccel != 0:
                enemyship.rotation += enemyship.rotaccel * time_since_phys_tick * timefactor
                if enemyship.rotation > 360: enemyship.rotation -= 360
                if enemyship.rotation < 0: enemyship.rotation += 360
                #enemyship.totrotations += enemyship.rotaccel * time_since_phys_tick * timefactor
            rotation_rads = enemyship.rotation * math.pi / 180
            if enemyship.accel != 0:
                enemyship.vel = enemyship.vel + enemyship.accel * time_since_phys_tick * timefactor
                if enemyship.vel >= 500: enemyship.vel = 500
                if enemyship.vel <= 0: enemyship.vel = 0
            if enemyship.vel != 0:
                enemyship.lastx = enemyship.x
                enemyship.lasty = enemyship.y
                enemyship.x += (enemyship.vel) * math.sin(rotation_rads) * time_since_phys_tick * timefactor
                enemyship.y += (enemyship.vel) * math.cos(rotation_rads) * time_since_phys_tick * timefactor

        for spacestation in spacestations:
            stationsector = spacestation.gridsector
            if stationsector not in allowedSectors: continue
            spacestation.rotation += 15 * time_since_phys_tick * timefactor
        i = -1
        for animation in animations:
            i += 1
            if animation.type == "fluxray":
                x1 = animation.endpos[0]
                y1 = animation.endpos[1]
                x2 = animation.startpos[0]
                y2 = animation.startpos[1]
                '''
                print("y2", y2)
                m = (y2 - y1) / (x2 - x1)
                c = y1 - m * x1
                # y = mx + c
                # y - mx = c
                t = time.time() - animation.starttime
                # (x,y) = (0, c) + (m, 1)*t + (1, -m)*sin(t)
                x3 = x2 + 0 + m * t + (1 * math.sin(t))
                y3 = y2 + c + 1 * t + (-m * math.sin(t))
                print(x1, y1, x2, y2, "c", c, "m", m)
                animation.x = x3
                animation.y = y3
                animation.points.append([x3, y3])
                '''
                '''
                animation.t += 500 * time_since_phys_tick * timefactor
                t = animation.t
                angle_rads = animation.angle * math.pi / 180
                x3 = x2 + t * math.cos(angle_rads) - math.sin(angle_rads) * math.sin(t / 20) * 20
                y3 = y2 + t * math.sin(angle_rads) + math.cos(angle_rads) * math.sin(t / 20) * 20
                animation.points.append([x3, y3])
                '''

            if animation.type == "radialburst":
                for enemyship in gameinfo.checkships:
                    enemyship.gridsector = functions.gridSector(enemyship)
                    enemysector = enemyship.gridsector
                    if enemysector not in allowedSectors: continue
                    if enemyship in animation.hitships: continue
                    timerunning = time.time() - animation.starttime
                    radius = animation.velocity * timerunning
                    dist = functions.distance(myship, enemyship)
                    if dist <= radius:
                        animation.hitships.append(enemyship)
                        #animation.hashit = True
                        allshieldsdown = True

                        for j in range(4):
                            shield = enemyship.shields[j]
                            if shield.charge > 0: allshieldsdown = False
                        if allshieldsdown:
                            enemyship.hull -= animation.damage
                        for j in range(4):
                            shield = enemyship.shields[j]
                            shield.charge -= animation.damage
                            if shield.charge < 0: shield.charge = 0
                        if enemyship.state != "attack" and enemyship.state != "attack_delay" and enemyship.state != "attack_makedistance":
                            enemyship.state = "attack_delay"
                        if enemyship.hull <= 50 and enemyship.state != "retreat":
                            enemyship.state = "retreat"
                            enemyship.startRetreat(enemyship)
                        if enemyship.hull <= 0:
                            enemyship.visible = False
                            animation.hitship = enemyship
                            enemyship.explode(animations)

            if animation.type == "torpedo" or animation.type == "bullet":
                angle_rads = animation.angle * math.pi / 180
                animation.x += (animation.velocity) * math.sin(angle_rads) * time_since_phys_tick * timefactor
                animation.y += (animation.velocity) * math.cos(angle_rads) * time_since_phys_tick * timefactor
                if animation.firer == "myship":

                    # check for collision

                    for enemyship in gameinfo.checkships:
                        enemyship.gridsector = functions.gridSector(enemyship)
                        enemysector = enemyship.gridsector
                        if enemysector not in allowedSectors: continue
                        mypoint = Point()
                        mypoint.x = animation.x
                        mypoint.y = animation.y
                        dist = functions.distance(enemyship, mypoint)
                        r = enemyship.width / 2 + 10
                        if dist > r: continue
                        if dist <= r and enemyship.visible:
                            closesthit = Point()
                            closesthit.x = animation.x
                            closesthit.y = animation.y
                            animation.hitship = enemyship
                            animation.angle = functions.angleBetween(closesthit, myship)
                            angle = 360 - (animation.angle) + 90 + enemyship.rotation
                            angle = functions.clampAngle(angle)
                            shieldnum = int(((angle + 45) / 360) * 4)
                            if angle <= 45: shieldnum = 0
                            if angle >= 315: shieldnum = 0
                            if shieldnum >= 4: shieldnum = 3
                            shieldcharge = enemyship.shields[shieldnum].charge
                            if enemyship.state != "attack" and enemyship.state != "attack_delay" and enemyship.state != "attack_makedistance":
                                enemyship.state = "attack_delay"
                            if shieldcharge <= 0:
                                animation.shielddown = True
                                enemyship.hull -= animation.damage
                                if enemyship.hull <= 50 and enemyship.state != "retreat":
                                    enemyship.state = "retreat"
                                    enemyship.startRetreat(enemyship)
                                if enemyship.hull <= 0:
                                    enemyship.visible = False
                                    animation.hitship = enemyship
                                    enemyship.explode(animations)
                            else:
                                enemyship.shields[shieldnum].charge -= animation.damage
                            animations.pop(i)
                            i -= 1
                elif animation.firer == "enemyship":
                    enemyship = animation.target
                    mypoint = Point()
                    mypoint.x = animation.x
                    mypoint.y = animation.y
                    dist = functions.distance(myship, mypoint)
                    # line-circle intercept
                    r = myship.width / 2 + 10
                    if dist > r: continue
                    if dist <= r:
                        closesthit = Point()
                        closesthit.x = animation.x
                        closesthit.y = animation.y
                        animation.angle = functions.angleBetween(closesthit, enemyship)
                        angle = 360 - (animation.angle) + 90 + myship.rotation
                        angle = functions.clampAngle(angle)
                        shieldnum = int(((angle + 45) / 360) * 4)
                        if angle <= 45: shieldnum = 0
                        if angle >= 315: shieldnum = 0
                        if shieldnum >= 4: shieldnum = 3
                        shieldcharge = myship.shields[shieldnum].charge
                        if shieldcharge <= 0:
                            animation.shielddown = True
                            myship.hull -= animation.damage
                            if myship.hull <= 0:
                                myship.alive = False
                                gameinfo.alive = False
                                gameinfo.lastdied = time.time()
                                myship.vel = 0
                                myship.rotaccel = 0
                                myship.accel = 0
                                myship.explode(animations)
                        else:
                            myship.shields[shieldnum].charge -= animation.damage
                        animations.pop(i)
