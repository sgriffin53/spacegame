import math
import functions

def physicsTick(myship, enemyships, spacestations, time_since_phys_tick, gameinfo):
    if gameinfo.screen == "game":
        sector = myship.gridsector
        allowedSectors = functions.allowedSectors(sector)

        timefactor = gameinfo.timefactor
        # Calculate new position
        myship.rotation += myship.rotaccel * time_since_phys_tick * timefactor
        if myship.rotation > 360: myship.rotation -= 360
        if myship.rotation < 0: myship.rotation += 360
        rotation_rads = myship.rotation * math.pi / 180
        myship.vel = myship.vel + myship.accel * time_since_phys_tick * timefactor
        if not myship.warping:
            if myship.vel >= 500: myship.vel = 500
            if myship.vel <= 0: myship.vel = 0
        myship.lastx = myship.x
        myship.lasty = myship.y
        myship.x += (myship.vel) * math.sin(rotation_rads) * time_since_phys_tick * timefactor
        myship.y += (myship.vel) * math.cos(rotation_rads) * time_since_phys_tick * timefactor
        myship.gridsector = functions.gridSector(myship)
        # enemy ships

        for enemyship in enemyships:
            enemysector = enemyship.gridsector
            if enemysector not in allowedSectors: continue
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
            enemyship.gridsector = functions.gridSector(enemyship)
            enemyship.x += (enemyship.vel) * math.sin(rotation_rads) * time_since_phys_tick * timefactor
            enemyship.y += (enemyship.vel) * math.cos(rotation_rads) * time_since_phys_tick * timefactor

        for spacestation in spacestations:
            stationsector = spacestation.gridsector
            if stationsector not in allowedSectors: continue
            spacestation.rotation += 15 * time_since_phys_tick * timefactor