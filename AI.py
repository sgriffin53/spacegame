
import functions
import random
import time
import math

class Point():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0

def enemyAITick(myship, enemyship, spacestations, animations, sounds, gameinfo):
    if enemyship.rotation == 0:
        enemyship.rotation = 1
    if enemyship not in gameinfo.checkships: return
    freeze_enemies = False
    if freeze_enemies:
        enemyship.accel = 0
        enemyship.vel = 0
        enemyship.rotaccel = 0
        return
    if gameinfo.screen != "game": return
    allowedSectors = myship.allowedsectors
    if enemyship.gridsector not in allowedSectors: return
    origstate = enemyship.state
    if enemyship.state == "retreat":
        if not myship.alive:
            enemyship.state = "patrol"
            return
        enemyship.fireNextWeapon(myship, animations, sounds, gameinfo, spacestations)
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
        dist = functions.distance(enemyship, mypoint)
        if dist >= enemyship.patroldist:
            enemyship.state == "patrol"
    if enemyship.state == "attack_delay":
        if not myship.alive:
            enemyship.state = "patrol"
            return
        if time.time() - enemyship.attackstart >= 1.0 or enemyship.substate == "attack":
            spacestation = spacestations[0]
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
            dist = int(functions.distance(enemyship, mypoint))
            enemyship.patroldist = dist - spacestation.radius - random.randint(30, 150)
    if enemyship.state == "attack":
        if not myship.alive:
            enemyship.state = "patrol"
            return
        enemyship.fireNextWeapon(myship, animations, sounds, gameinfo, spacestations)
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
        targetx = myship.x + random.randint(-50, +50)
        targety = myship.y + random.randint(-50, +50)
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
        dist = functions.distance(enemyship, mypoint)
        myshipdist = functions.distance(enemyship, myship)
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
    if enemyship.state == "patrol":
        if enemyship.vel == 0 and enemyship.accel == 0:
            enemyship.startPatrol()
        if abs(enemyship.patrolangle - enemyship.rotation) < 10:
            enemyship.rotation = enemyship.patrolangle
            enemyship.rotaccel = 0
        if enemyship.vel >= enemyship.patrolspeed:
            enemyship.vel = enemyship.patrolspeed
            enemyship.accel = 0
        mypoint = Point()
        mypoint.x = enemyship.patrolstart[0]
        mypoint.y = enemyship.patrolstart[1]
        dist = functions.distance(enemyship, mypoint)
        if dist >= enemyship.patroldist:
            enemyship.vel = 0
            enemyship.accel = 0
            if random.randint(0,3) == 0:
                enemyship.state = "gotostation"
                enemyship.startGoToStation(enemyship.closestStation(spacestations))
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
        dist = functions.distance(enemyship, mypoint)
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
        dist = functions.distance(enemyship, mypoint)
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