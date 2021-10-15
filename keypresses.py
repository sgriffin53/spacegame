import pygame
import sys
import functions
from classes import Point, Button

def handleMouseButtonUp(gameinfo, myship, mousepos, enemyships, spacestations, music):
    if gameinfo.screen == "map":
        onmap = False
        if mousepos[0] < 200 or mousepos[1] < 30 or mousepos[0] > 800 or mousepos[1] > 630:
            onmap = False
        else:
            onmap = True
        onWarpButton = False
        '''
        if mousepos[0] < 842 or mousepos[1] < 30 or mousepos[0] > 1042 or mousepos[1] > 80:
            onWarpButton = False
        else:
            onWarpButton = True
        if onWarpButton and gameinfo.selectedstation != None:
            myship.autostate = "warp_rot"
            myship.warping = True
            myship.startWarpRot(spacestations[gameinfo.selectedstation])
            gameinfo.screen = "game"
        '''
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
    for button in gameinfo.buttons:
        if button.screen == gameinfo.screen:
            buttonRect = pygame.Rect((button.x, button.y, button.width, button.height))
            if buttonRect.collidepoint(mousepos):
                button.onClick(gameinfo, myship, enemyships, spacestations, music)

def handleMouseOver(gameinfo):
    mousepos = pygame.mouse.get_pos()
    for button in gameinfo.buttons:
        buttonRect = pygame.Rect((button.x, button.y, button.width, button.height))
        if buttonRect.collidepoint(mousepos):
            button.textcol = (0, 255, 0)
        else:
            button.textcol = (255, 255, 255)

def detectKeyPresses(event_get, fullscreen, myship, enemyships, gameinfo, animations, sounds, spacestations, music):
    handleMouseOver(gameinfo)
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
            handleMouseButtonUp(gameinfo, myship, pos, enemyships, spacestations, music)
        if event.type == pygame.KEYDOWN:
            if gameinfo.alive:
                if gameinfo.screen == "game":
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
                if event.key == pygame.K_m:
                    newscreen = "game"
                    if gameinfo.screen == "game": newscreen = "map"
                    gameinfo.screen = newscreen
                if event.key == pygame.K_RETURN:
                    dist = functions.distance(myship.closestStation(spacestations), myship)
                    if dist <= spacestations[0].width / 2 + 400:
                        newscreen = "game"
                        if gameinfo.screen == "game": newscreen = "stationmenu"
                        gameinfo.screen = newscreen

    keys = pygame.key.get_pressed()  # checking pressed keys

    # unset alt and enter flags if they're not pressed

    if gameinfo.alive and not myship.warping and gameinfo.screen == "game":
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
        if keys[pygame.K_SPACE]:
            dist = functions.distance(myship.closestStation(spacestations), myship)
            if myship.targeted != None and dist > 900:
                myship.fireNextWeapon(enemyships, animations, sounds, spacestations)
    if keys[pygame.K_ESCAPE]:
        sys.exit()
    if keys[pygame.K_SPACE]:
        pass
        #if myship.targeted != None:
         #   frameinfo.firingphasers = True
          #  frameinfo.phaserstart = time.time()