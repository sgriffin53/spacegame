import pygame
import sys
import functions
from classes import Point, Weapon

def handleMouseButtonUp(gameinfo, myship, mousepos, enemyships, spacestations, music):
    if gameinfo.screen == "map":
        onmap = False
        factorx = gameinfo.width / gameinfo.nativewidth
        factory = gameinfo.height / gameinfo.nativeheight
        if mousepos[0] < 200 * factorx or mousepos[1] < 30 * factory or mousepos[0] > 800* factorx or mousepos[1] > 630 * factory:
            onmap = False
        else:
            onmap = True
        if onmap:
            i = -1
            for spacestation in spacestations:
                i += 1
                drawX = 200 + (spacestation.x / 2000000) * 600
                drawY = 630 - (spacestation.y / 2000000) * 600
                drawX = drawX * factorx
                drawY = drawY * factory
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
            factorx = gameinfo.width / gameinfo.nativewidth
            factory = gameinfo.height / gameinfo.nativeheight
            buttonRect = pygame.Rect((button.x * factorx, button.y * factory, button.width * factorx, button.height * factory))
            if buttonRect.collidepoint(mousepos):
                button.onClick(gameinfo, myship, enemyships, spacestations, music)

def handleMouseOver(gameinfo, images):
    mousepos = pygame.mouse.get_pos()
    for button in gameinfo.buttons:
        factorx = gameinfo.width / gameinfo.nativewidth
        factory = gameinfo.height / gameinfo.nativeheight
        buttonRect = pygame.Rect(
            (button.x * factorx, button.y * factory, button.width * factorx, button.height * factory))
        if buttonRect.collidepoint(mousepos):
            button.textcol = (0, 255, 0)
        else:
            button.textcol = (255, 255, 255)
        if button.onclick == "shieldselectionleft":
            if buttonRect.collidepoint(mousepos):
                button.image = images[5]
            else:
                button.image = images[4]
        if button.onclick == "shieldselectionright":
            if buttonRect.collidepoint(mousepos):
                button.image = images[7]
            else:
                button.image = images[6]

def detectKeyPresses(event_get, fullscreen, myship, enemyships, gameinfo, animations, sounds, spacestations, music, screen, stars, images, spacestationIMG, shipIMG, enemyshipIMG):
    handleMouseOver(gameinfo, images)
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
            game.fullscreen = fullscreen
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
                    if dist <= spacestations[0].width / 2 + 400 and (gameinfo.screen == "game" or gameinfo.screen == "stationmenu"):
                        newscreen = "game"
                        if gameinfo.screen == "game": newscreen = "stationmenu"
                        gameinfo.screen = newscreen
                        gameinfo.messages[0].visible = False
                if event.key == pygame.K_F8:
                    gameinfo.resindex += 1
                    if gameinfo.resindex > 4: gameinfo.resindex = 0
                    gameinfo.resolution = gameinfo.resolutions[gameinfo.resindex]
                    width = gameinfo.resolution.width
                    height = gameinfo.resolution.height
                    '''
                    index = gameinfo.resindex
                    if index == 1:
                        width = 800
                        height = 600
                    elif index == 2:
                        width = 1920
                        height = 1080
                    elif index == 3:
                        width = 2560
                        height = 1440
                    else:
                        width = 1280
                        height = 768
                    '''
                    functions.setResolution(width, height, gameinfo, screen, stars, images, spacestationIMG, shipIMG, enemyshipIMG)
                if event.key == pygame.K_F9 or event.key == pygame.K_F10 or event.key == pygame.K_F11 or event.key == pygame.K_F12:
                    if gameinfo.screen == "upgrademenu":
                        slotindex = -1
                        if event.key == pygame.K_F9: slotindex = 0
                        elif event.key == pygame.K_F10: slotindex = 1
                        elif event.key == pygame.K_F11: slotindex = 2
                        elif event.key == pygame.K_F12: slotindex = 3
                        weaponlist = [None, "laser-c1", "laser-c2", "bullet-c1", "torpedo-c1", "torpedo-c2", "fluxray-c1", "fluxray-c2", "fluxray-c3", "disruptor-c1",
                                      "radialburst-c1", "particlebeam-c1"]
                        index = -1
                        for i in range(len(weaponlist)):
                            if myship.weapons[slotindex].fulltype == weaponlist[i]: index = i
                        if index >= 0:
                            index += 1
                            if index >= len(weaponlist):
                                index = 0
                            myship.weapons[slotindex] = Weapon(weaponlist[index])

    keys = pygame.key.get_pressed()  # checking pressed keys

    if gameinfo.alive and not myship.warping and gameinfo.screen == "game":
        if keys[pygame.K_LEFT]:
            myship.rotaccel = -160
        elif keys[pygame.K_RIGHT]:
            myship.rotaccel = 160
        elif not myship.warping:
            myship.rotaccel = 0
        if keys[pygame.K_a]:
            myship.turretrotaccel = -180
        elif keys[pygame.K_d]:
            myship.turretrotaccel = 180
        else:
            myship.turretrotaccel = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            myship.accel = 250
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            myship.accel = -250
        else:
            myship.accel = 0
        if keys[pygame.K_SPACE]:
            myship.fireNextWeapon(enemyships, animations, sounds, spacestations)
    if keys[pygame.K_ESCAPE]:
        sys.exit()
    if keys[pygame.K_SPACE]:
        pass