import pygame
import sys
import functions
from classes import Point

def handleMouseButtonUp(gameinfo, myship, mousepos, spacestations):
    if gameinfo.screen == "map":
        onmap = False
        if mousepos[0] < 200 or mousepos[1] < 30 or mousepos[0] > 800 or mousepos[1] > 630:
            onmap = False
        else:
            onmap = True
        onWarpButton = False
        if mousepos[0] < 842 or mousepos[1] < 30 or mousepos[0] > 1042 or mousepos[1] > 80:
            onWarpButton = False
        else:
            onWarpButton = True
        if onWarpButton and gameinfo.selectedstation != None:
            myship.autostate = "warp_rot"
            myship.warping = True
            myship.startWarpRot(spacestations[gameinfo.selectedstation])
            gameinfo.screen = "game"
        if onmap:
            i = -1
            for spacestation in spacestations:
                i += 1
                drawX = 200 + (spacestation.x / 2000000) * 600
                drawY = 630 - (spacestation.y / 2000000) * 600
                point1 = Point()
                point1.x = drawX
                point1.y = drawY
                point2 = Point()
                point2.x = mousepos[0]
                point2.y = mousepos[1]
                dist = functions.distance(point1, point2)
                if dist <= 25:
                    gameinfo.selectedstation = i
                    return
            gameinfo.selectedstation = None

def detectKeyPresses(event_get, fullscreen, myship, enemyships, gameinfo, animations, sounds, spacestations):
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
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            handleMouseButtonUp(gameinfo, myship, pos, spacestations)
        if event.type == pygame.KEYDOWN:
            if gameinfo.alive:
                if event.key == pygame.K_m:
                    newscreen = "game"
                    if gameinfo.screen == "game": newscreen = "map"
                    gameinfo.screen = newscreen
                if event.key == pygame.K_t:
                    myship.nextTarget(enemyships)
                if event.key == pygame.K_c:
                    myship.closestTarget(enemyships, gameinfo)
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

    keys = pygame.key.get_pressed()  # checking pressed keys

    # unset alt and enter flags if they're not pressed

    if gameinfo.alive and not myship.warping:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            myship.rotaccel = -120
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            myship.rotaccel = 120
        elif not myship.warping:
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