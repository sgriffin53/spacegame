import time
import functions
import pygame
import math
import random
from classes import Point, Button

def drawStars(screen, stars, myship, gameinfo):
    for i in range(0,len(stars)):
        thisX = (stars[i]['x'] - myship.x) % gameinfo.width
        thisY = (stars[i]['y'] + myship.y) % gameinfo.height
        screen.set_at((int(thisX), int(thisY)), (255, 255, 255))

def rot_center(image, angle, x, y):
    angle = 360 - angle
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect

def update_fps(gameinfo):
    fps = str(int(gameinfo.clock.get_fps()))
    fps_text = gameinfo.myfont.render(fps + " FPS", 1, pygame.Color("coral"))
    return fps_text

def get_fps(gameinfo):
    return int(gameinfo.clock.get_fps())

def drawMyHealthBar(screen, myship, gameinfo):
    percentage = myship.hull * 100 / myship.maxhull
    centre = (gameinfo.width / 2, gameinfo.height / 2)
    drawX = centre[0] - myship.width / 2 + 10
    drawY = centre[1] + myship.width / 2 + 8

    drawW = (myship.width - 10) * (percentage / 100)
    # draw health bar
    colour = (0, 168, 0)
    if percentage <= 50: colour = (168, 0, 0)

    pygame.draw.rect(screen, colour, (drawX, drawY, drawW, 12), 0)

    # draw border

    pygame.draw.rect(screen, (0, 0 , 128), (drawX, drawY, myship.width - 10, 12), 2)

def drawEnemyHealthBar(screen, enemyship, myship, gameinfo):


    percentage = enemyship.hull * 100 / enemyship.maxhull
    centre = (gameinfo.width / 2, gameinfo.height / 2)

    drawX = centre[0] + enemyship.x - myship.x  - enemyship.width / 2 + 10
    drawY = centre[1] - enemyship.y + myship.y  +  myship.width / 2 + 8

    drawW = (myship.width - 10) * (percentage / 100)
    # draw health bar
    colour = (0, 168, 0)
    if percentage <= 50: colour = (168, 0, 0)

    pygame.draw.rect(screen, colour, (drawX, drawY, drawW, 12), 0)

    # draw border

    pygame.draw.rect(screen, (0, 0 , 128), (drawX, drawY, enemyship.width - 10, 12), 2)

def drawTargetLine(screen, myship, enemyship, spacestations, gameinfo):
    # x1, y1 = point at edge of screen
    # x2, y2 = point which intersects with line between ships at (x1, y2 - 200)
    # x3, y3 = arrow one co-ord
    # x4, y4 = arrow two co-ord
    width = gameinfo.width
    height = gameinfo.height
    centre = (width / 2, height / 2)

    shiptype = enemyship.type
    # find direction
    lowest_dist = 0
    x_dist = abs(enemyship.x - myship.x)
    y_dist = abs(enemyship.y - myship.y)
    dir = "left"
    if enemyship.x <= myship.x:
        dir = "left"
        lowest_dist = x_dist
    if enemyship.y <= myship.y:
        if y_dist >= lowest_dist:
            dir = "bottom"
            lowest_dist = y_dist + width - height
    if enemyship.x >= myship.x:
        if x_dist >= lowest_dist:
            dir = "right"
            lowest_dist = x_dist
    if enemyship.y >= myship.y:
        if y_dist >= lowest_dist:
            dir = "top"
    x1, y1, x2, y2, x3, x4, y3, y4, m, c = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    dist = functions.distance(myship, enemyship)
    a = 30 # arrow size
    # 10 + (distance / 30 * sensorrange_ships) # a goes from 10 to 30
    a = 10 + (1 - dist / myship.sensorrange_ships) * 20
    if enemyship.x - myship.x == 0: m = 0
    else: m = (enemyship.y - myship.y) / (enemyship.x - myship.x)
    if m == 0: m = 0.00001
    c = myship.y - m * myship.x
    if dir == "bottom":
        y1 = myship.y - height / 2 + 10
        x1 = (y1 - c) / m
        y2 = y1 + 150
        x2 = (y2 - c) / m
        x3 = x1 - a
        y3 = y1 + a
        x4 = x1 + a
        y4 = y1 + a
    elif dir == "top":
        y1 = myship.y + height / 2 - 10
        x1 = (y1 - c) / m
        y2 = y1 - 150
        x2 = (y2 - c) / m
        x3 = x1 - a
        y3 = y1 - a
        x4 = x1 + a
        y4 = y1 - a
    elif dir == "left":
        x1 = myship.x - width / 2 + 10
        y1 = m * x1 + c
        x2 = x1 + 150
        y2 = m * x2 + c
        x3 = x1 + a
        y3 = y1 + a
        x4 = x1 + a
        y4 = y1 - a
    elif dir == "right":
        x1 = myship.x + width / 2 - 10
        y1 = m * x1 + c
        x2 = x1 - 150
        y2 = m * x2 + c
        x3 = x1 - a
        y3 = y1 + a
        x4 = x1 - a
        y4 = y1 - a
    else: return
    draw_x1 = int(centre[0] + x1 - myship.x)
    draw_y1 = int(centre[1] - y1 + myship.y)
    draw_x2 = int(centre[0] + x2 - myship.x)
    draw_y2 = int(centre[1] - y2 + myship.y)
    draw_x3 = int(centre[0] + x3 - myship.x)
    draw_y3 = int(centre[1] - y3 + myship.y)
    draw_x4 = int(centre[0] + x4 - myship.x)
    draw_y4 = int(centre[1] - y4 + myship.y)

    colour = (192, 192, 192)
    if enemyship.type == "Space Station":
        colour = (0, 255, 0)
    elif enemyship.index == myship.targeted:
        colour = (0, 0, 192)

    #pygame.draw.line(screen, colour, (draw_x1, draw_y1), (draw_x2, draw_y2), 3)
    pygame.draw.line(screen, colour, (draw_x1, draw_y1), (draw_x3, draw_y3), 7)
    pygame.draw.line(screen, colour, (draw_x1, draw_y1), (draw_x4, draw_y4), 7)
    dist = functions.distance(myship, enemyship)
    dir_label_font = gameinfo.dir_label_font
    typeText = dir_label_font.render(shiptype, False, colour)
    distanceText = dir_label_font.render(str(int(dist)) + " km", False, colour)
    drawX_dist = -1000
    drawY_dist = -1000
    drawX_type = -1000
    drawY_type = -1000
    if dir == "top":
        drawX_dist = draw_x3 + 0
        drawY_dist = draw_y3 + 5
        drawX_type = draw_x3 + 0
        drawY_type = draw_y3 + 25
    if dir == "left":
        drawX_dist = draw_x3 + 5
        drawY_dist = draw_y3 + 0
        drawX_type = draw_x3 + 5
        drawY_type = draw_y3 + 20
    if dir == "bottom":
        drawX_dist = draw_x3 + 0
        drawY_dist = draw_y3 - 35
        drawX_type = draw_x3 + 0
        drawY_type = draw_y3 - 15
    if dir == "right":
        drawX_dist = draw_x3 - 105
        drawY_dist = draw_y3 + 0
        drawX_type = draw_x3 - 105
        drawY_type = draw_y3 + 20
    screen.blit(distanceText, (drawX_dist, drawY_dist))
    screen.blit(typeText, (drawX_type, drawY_type))

def onScreen(obj, ship, gameinfo):
    # detects whether a circle with radius obj.width is on the screen

    # screen:
    # A ---- B
    # |      |
    # C ---- D
    width = gameinfo.width
    height = gameinfo.height

    obj_left = obj.x - obj.width / 2
    obj_right = obj.x + obj.width / 2
    obj_top = obj.y + obj.width / 2
    obj_bottom = obj.y - obj.width / 2
    pointA_x = ship.x - width / 2
    pointA_y = ship.y + height / 2
    pointB_x = ship.x + width / 2
    pointC_y = ship.y - height / 2
    if obj_right >= pointA_x and obj_left <= pointB_x and obj_top >= pointC_y and obj_bottom <= pointA_y:
        return True
    return False

def drawMyShields(screen, myship, gameinfo):
    myship_rotation_rads = (360 - myship.rotation) * math.pi / 180
    start_ang = 43
    centre = (gameinfo.width / 2, gameinfo.height / 2)
    margin = 10
    # draw all four shields
    n = -1
    for i in range(45, 403, 90):
        n += 1
        start_ang_rads = (i + 5) * math.pi / 180 + myship_rotation_rads
        end_ang_rads = (i + 85) * math.pi / 180 + myship_rotation_rads
        redcolour = 0
        greencolour = 0
        percent = myship.shields[n].charge * 100 / myship.shields[n].maxcharge
        if percent > 50: greencolour = myship.shields[n].charge * 255 / myship.shields[n].maxcharge
        else: redcolour = myship.shields[n].charge * 255 / myship.shields[n].maxcharge
        if greencolour < 0: greencolour = 0
        if redcolour < 0: redcolour = 0
        pygame.draw.arc(screen, (redcolour, greencolour, 0), (
        centre[0] - myship.width / 2 - margin, centre[1] - myship.width / 2 - margin, myship.width + margin * 2,
        myship.width + margin * 2), start_ang_rads, end_ang_rads, 2)

def drawMyTurret(screen, myship, gameinfo):
    centre = (gameinfo.width / 2, gameinfo.height / 2)
    ang_rads = myship.turretrot * math.pi / 180
    margin = 5
    dist1 = myship.width / 2 + margin * 2
    dist2 = myship.width / 2 + margin * 2 + 50
    drawX = centre[0] + dist1 * math.cos(ang_rads)
    drawY = centre[1] + dist1 * math.sin(ang_rads)
    pygame.draw.circle(screen, (255, 0, 0), (drawX, drawY), 6, 3)
    drawX = centre[0] + dist2 * math.cos(ang_rads)
    drawY = centre[1] + dist2 * math.sin(ang_rads)
    pygame.draw.circle(screen, (255, 0, 0), (drawX, drawY), 6, 3)
    myship.turrentpos = (drawX, drawY)

def drawEnemyShields(screen, enemyship, myship, gameinfo):
    enemyship_rotation_rads = (360 - enemyship.rotation) * math.pi / 180
    centre = (gameinfo.width / 2, gameinfo.height / 2)
    margin = 10
    n = -1
    for i in range(45, 403, 90):
        n += 1
        start_ang_rads = (i + 5) * math.pi / 180 + enemyship_rotation_rads
        end_ang_rads = (i + 85) * math.pi / 180 + enemyship_rotation_rads
        redcolour = 0
        greencolour = 0
        percent = enemyship.shields[n].charge * 100 / enemyship.shields[n].maxcharge
        if percent > 50:
            greencolour = enemyship.shields[n].charge * 255 / enemyship.shields[n].maxcharge
        else:
            redcolour = enemyship.shields[n].charge * 255 / enemyship.shields[n].maxcharge
            greencolour = redcolour / 2
        if greencolour < 0: greencolour = 0
        if redcolour < 0: redcolour = 0
        enemydrawX = centre[0] + enemyship.x - myship.x
        enemydrawY = centre[1] - enemyship.y + myship.y
        pygame.draw.arc(screen, (redcolour, greencolour, 0), (
        enemydrawX - enemyship.width / 2 - margin, enemydrawY - myship.width / 2 - margin, enemyship.width + margin * 2,
        enemyship.width + margin * 2), start_ang_rads, end_ang_rads, 2)

def renderUpgradeMenu(screen, images, gameinfo, myship):
    screen.fill((0, 0, 0))

    bg = images[1]
    bg = pygame.transform.scale(bg, (gameinfo.width, gameinfo.height))
    screen.blit(bg, (0, 0))
    titlefont = pygame.font.SysFont('Calibri', 60, 1)
    titleText = titlefont.render("Upgrade Ship", False,
                                 (255, 255, 255))
    screen.blit(titleText, (460, 30))
    menulabelfont = pygame.font.SysFont('Calibri', 30)
    baseshipText = menulabelfont.render("Base Ship", False, (255, 255, 255))
    screen.blit(baseshipText, (100, 120))
    screen.blit(myship.image, (130, 160))
    warpenginesText = menulabelfont.render("Warp Engines: Class 3", False, (255, 255, 255))
    screen.blit(warpenginesText, (381, 120))
    combatenginesText = menulabelfont.render("Combat Engines: Class 1", False, (255, 255, 255))
    screen.blit(combatenginesText, (350, 160))
    shield = myship.shields[0]
    shieldsText = None
    if shield == None:
        shieldsText = menulabelfont.render("Shields: None", False, (255, 255, 255))
    else:
        shieldsText = menulabelfont.render("Shields: Class " + str(myship.shields[0].classnum), False, (255, 255, 255))
    screen.blit(shieldsText, (461, 200))
    weaponText = []
    for i in range(4):
        rendertext = "Weapon " + str(i + 1) + ": "
        if myship.weapons[i] == None:
            rendertext += "None"
        else:
            rendertext += myship.weapons[i].fullname
        weaponText.append(menulabelfont.render(rendertext, False, (255, 255, 255)))
        screen.blit(weaponText[i], (424, 240 + (i * 40)))

def renderStationMenu(screen, images, gameinfo, myship, spacestations):
    screen.fill((0, 0, 0))
    bg = images[1]
    bg = pygame.transform.scale(bg, (gameinfo.width, gameinfo.height))
    screen.blit(bg, (0, 0))
    titlefont = pygame.font.SysFont('Calibri', 60, 1)
    titleText = titlefont.render("Space station " + str(myship.closestStation(spacestations).index), False,
                                 (255, 255, 255))
    screen.blit(titleText, (460, 30))
    menulabelfont = pygame.font.SysFont('Calibri', 30)
    creditsText = menulabelfont.render("Credits: " + str(gameinfo.credits), False, (255, 255, 255))
    screen.blit(creditsText, (50, 130))
    repaircost = functions.repairCost(myship)
    repairText = menulabelfont.render("Repair Ship (Cost " + str(repaircost) + ")", False, (255, 255, 255))
    screen.blit(repairText, (50, 180))
    upgradeText = menulabelfont.render("Upgrade Ship", False, (255, 255, 255))
    screen.blit(upgradeText, (400, 180))

def renderMainMenu(screen, images, gameinfo):
    screen.fill((0, 0, 0))
    bg = images[0]
    bg = pygame.transform.scale(bg, (gameinfo.width, gameinfo.height))
    screen.blit(bg, (0, 0))
    titlefont = pygame.font.SysFont('Calibri Bold', 70)
    titleText = titlefont.render("Stardawg 3000", False,
                                 (255, 255, 255))
    screen.blit(titleText, (gameinfo.width / 2 - 170, 30))

def renderCredits(screen, images, gameinfo):
    screen.fill((0, 0, 0))
    bg = images[0]
    bg = pygame.transform.scale(bg, (gameinfo.width, gameinfo.height))
    screen.blit(bg, (0, 0))
    titlefont = pygame.font.SysFont('Calibri', 70, 1)
    titleText = titlefont.render("Credits", False,
                                 (255, 255, 255))
    screen.blit(titleText, (560, 30))
    creditsfont = pygame.font.SysFont('Calibri', 25, 1)
    createdByText = creditsfont.render("Created by: Steve Griffin", False, (255, 255, 255))
    screen.blit(createdByText, (525, 150))
    musicByText = creditsfont.render("Music and sound effects by: Eric Matyas (www.soundimage.com)", False,
                                     (255, 255, 255))
    screen.blit(musicByText, (350, 220))
    artByText = creditsfont.render("Art by:", False, (255, 255, 255))
    screen.blit(artByText, (420, 290))
    millionthVectorText = creditsfont.render("MillionthVector (http://millionthvector.blogspot.de)", False,
                                             (255, 255, 255))
    screen.blit(millionthVectorText, (495, 290))
    eikesterText = creditsfont.render("Eikester", False, (255, 255, 255))
    screen.blit(eikesterText, (495, 330))
    craftpixText = creditsfont.render("CraftPix.net 2D Game Assets", False, (255, 255, 255))
    screen.blit(craftpixText, (495, 370))
    attributionText = creditsfont.render("See attribution.txt for full attribution information.", False,
                                         (255, 255, 255))
    screen.blit(attributionText, (440, 440))

def renderMap(screen, gameinfo, myship, spacestations):
    screen.fill((0, 0, 0))

    titlefont = gameinfo.map_title_font
    titleText = titlefont.render("Map:", False,
                                 (255, 255, 255))
    screen.blit(titleText, (100, 30))
    pygame.draw.rect(screen, (255, 255, 255), (200, 30, 600, 600), 1)

    for (x, y) in gameinfo.mapstars:
        screen.set_at((x, y), (255, 255, 255))
    i = -1
    # draw each space station
    for spacestation in spacestations:
        i += 1
        x = spacestation.x
        y = spacestation.y
        drawX = 200 + (x / 2000000) * 600
        drawY = 630 - (y / 2000000) * 600
        img = spacestation.image
        img = pygame.transform.scale(img, (64, 64))
        (img, spacestationcentre) = rot_center(img, spacestation.rotation, drawX, drawY)
        screen.blit(img, spacestationcentre)
        spacestation.centre = spacestationcentre
        if i == gameinfo.selectedstation:
            pygame.draw.rect(screen, (255, 0, 0), (drawX - 32, drawY - 32, 64, 64), 1)

    # draw red circle for my ship

    x = myship.x
    y = myship.y
    drawX = 200 + (x / 2000000) * 600
    drawY = 630 - (y / 2000000) * 600
    pygame.draw.circle(screen, (255, 0, 0), (drawX, drawY), 5)
    dist = 0
    if gameinfo.selectedstation != None:
        dist = functions.distance(spacestations[gameinfo.selectedstation], myship)
    else:
        dist = 0
    thisfont = pygame.font.SysFont('Calibri', 24)
    noStationText = thisfont.render("No Station Selected", False,
                                                      (255, 255, 255))
    stationInfoText = thisfont.render("Space Station " + str(gameinfo.selectedstation), False,
                                      (255, 255, 255))
    dispdist = int(dist)
    if (dist >= 1000000):
        dispdist = str(round(dist / 1000000, 2)) + "M"
    elif (dist >= 1000):
        dispdist = str(round(dist / 1000, 2)) + "K"
    distanceText = thisfont.render("Distance: " + str(dispdist) + " km", False, (255, 255, 255))
    warptime = dist / 200000
    disptime = warptime
    if disptime < 1:
        disptime = round(disptime, 5)
    else:
        disptime = int(disptime)
    timeText = thisfont.render("Warp Time: " + str(disptime) + " seconds", False, (255, 255, 255))
    if gameinfo.selectedstation != None:
        screen.blit(stationInfoText, (830, 30))
        screen.blit(distanceText, (830, 60))
        screen.blit(timeText, (830, 90))
    else:
        screen.blit(noStationText, (830, 30))

def renderGame(screen, stars, myship, gameinfo, spacestations, enemyships, shipIMG, animations, images):
    # Fill the background with white
    screen.fill((0, 0, 0))

    drawStars(screen, stars, myship, gameinfo)

    # Calculate centre

    centre = (gameinfo.width / 2, gameinfo.height / 2)
    del gameinfo.checkships[:]
    i = -1
    for enemyship in enemyships:
        i += 1
        dist = functions.distance(myship, enemyship)
        if dist > 2000: continue
        if not onScreen(enemyship, myship, gameinfo):
            drawTargetLine(screen, myship, enemyship, spacestations, gameinfo)
            continue
        gameinfo.checkships.append(enemyship)
        # Draw enemy ship
        if enemyship.visible:
            enemydrawX = centre[0] + enemyship.x - myship.x
            enemydrawY = centre[1] - enemyship.y + myship.y
            es_centre = (enemydrawX, enemydrawY)
            (newIMG, es_centre) = rot_center(enemyship.shipIMG, enemyship.rotation, es_centre[0],
                                             es_centre[1])  # rotate ship appropriately
            screen.blit(newIMG, es_centre)
            drawEnemyHealthBar(screen, enemyship, myship, gameinfo)
            drawEnemyShields(screen, enemyship, myship, gameinfo)
            if enemyship.visible and myship.targeted == i:
                enemydrawX = centre[0] + enemyship.x - myship.x
                enemydrawY = centre[1] - enemyship.y + myship.y
                margin = 40
                pygame.draw.rect(screen, (255, 0, 0),
                                 (enemydrawX - enemyship.width / 2 - margin / 2,
                                  enemydrawY - enemyship.width / 2 - margin / 2,
                                  enemyship.width + margin,
                                  enemyship.width + margin), 2)

    # Draw space station
    for spacestation in spacestations:
        spacestationX = centre[0] + spacestation.x - myship.x
        spacestationY = centre[1] - spacestation.y + myship.y
        dist = functions.distance(myship, spacestation)
        img = spacestation.image
        if onScreen(spacestation, myship, gameinfo):  # on screen
            (img, spacestationcentre) = rot_center(img, spacestation.rotation, spacestationX, spacestationY)
            screen.blit(img, spacestationcentre)
            spacestation.centre = spacestationcentre
        if dist < 3000:
            pygame.draw.circle(screen, (0, 0, 255), (spacestationX, spacestationY), spacestation.radius + 400, 1)
        elif dist < 5000:  # not on screen and within short range sensor range
            drawTargetLine(screen, myship, spacestation, spacestations, gameinfo)

    # Draw my ship

    (shipIMG, newcentre) = rot_center(shipIMG, myship.rotation, centre[0], centre[1])  # rotate ship appropriately
    if myship.alive:
        screen.blit(shipIMG, newcentre)  # draw ship
        drawMyHealthBar(screen, myship, gameinfo)
        drawMyShields(screen, myship, gameinfo)
        drawMyTurret(screen, myship, gameinfo)

    # Draw text:

    myfont = gameinfo.myfont
    velText = myfont.render('Velocity: ' + str(round(myship.vel, 1)), False, (255, 255, 255))
    shipXText = myfont.render('X: ' + str(round(myship.x, 0)), False, (255, 255, 255))
    shipYText = myfont.render('Y: ' + str(round(myship.y, 0)), False, (255, 255, 255))
    sectorText = myfont.render('Sector: ' + str(myship.gridsector), False, (255, 255, 255))
    screen.blit(shipXText, (2, 540))
    screen.blit(shipYText, (2, 560))
    screen.blit(velText, (2, 580))
    screen.blit(sectorText, (2, 600))
    curfps = get_fps(gameinfo)
    fps_text = myfont.render(str(curfps) + " FPS", 1, pygame.Color("coral"))
    screen.blit(fps_text, (10, 5))
    if gameinfo.redalert:
        redalert_text = myfont.render("Red Alert", 1, (255, 0, 0))
        screen.blit(redalert_text, (80, 5))
    renderAnimations(screen, animations, myship, gameinfo, enemyships)
    if time.time() - gameinfo.gamemessagedisplayed < 5:
        messageText = gameinfo.gamemessage_font.render(gameinfo.gamemessage, False, (255, 255, 255))
        screen.blit(messageText, ((170, 110)))

def renderAnimations(screen, animations, myship, gameinfo, enemyships):
    centre = (gameinfo.width / 2, gameinfo.height / 2)
    x5 = 0
    y5 = 0
    i = -1
    for animation in animations:
        i += 1
        if animation.type == "fluxray":
            if time.time() >= animation.endtime:
                if animation.firer == "enemyship" and animation.missed != False:
                    angle = (animation.angle) + 90 + myship.rotation
                    angle = functions.clampAngle(angle)
                    shieldnum = int(((angle + 45) / 360) * 4)
                    if angle <= 45: shieldnum = 0
                    if angle >= 315: shieldnum = 0
                    if shieldnum >= 4: shieldnum = 3
                    shieldcharge = myship.shields[shieldnum].charge
                    if shieldcharge <= 0:
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
            if animation.firer == "myship" or animation.firer == "enemyship":
                del animation.points[:]
                lastx = None
                lasty = None
                x1 = animation.endpos[0]
                y1 = animation.endpos[1]
                x2 = myship.x
                y2 = myship.y
                if animation.firer == "enemyship":
                    x2 = animation.target.x
                    y2 = animation.target.y
                animation.offset = random.randint(1, 30)
                offset = animation.offset
               # offset = 1 # for sine
                #offset2 = random.randint(1,6) # for sine
                animation.t = 1000
                tot = animation.t
                for t in range(0, tot, 5):
                    angle_rads = (360 - animation.angle) * math.pi / 180
                    x3 = x2 + (t * offset) * math.cos(angle_rads) - math.sin(angle_rads) * math.sin((t * offset) / 20) * 20
                    y3 = y2 + (t * offset) * math.sin(angle_rads) + math.cos(angle_rads) * math.sin((t * offset) / 20) * 20
                    '''
                    for sine waves:
                    x3 = x2 + (t * offset) * math.cos(angle_rads) - math.sin(angle_rads) * math.sin((t * offset2 + offset) / 20) * 20
                    y3 = y2 + (t * offset) * math.sin(angle_rads) + math.cos(angle_rads) * math.sin((t * offset2 + offset) / 20) * 20
                    '''
                    animation.points.append([x3, y3])

                for point in animation.points:
                    x = point[0]
                    y = point[1]
                    drawX = centre[0] + x - myship.x
                    drawY = centre[1] - y + myship.y
                    #pygame.draw.circle(screen, animation.colour, (drawX,
                                   #                               drawY),
                                  #     2)
                    if lastx != None:
                        drawXlast = centre[0] + lastx - myship.x
                        drawYlast = centre[1] - lasty + myship.y
                        width = 2
                        if animation.classnum >= 2: width = 5
                        pygame.draw.line(screen, animation.colour, (drawX, drawY), (
                            drawXlast,
                            drawYlast), width)
                    lastx = x
                    lasty = y

        if animation.type == "laser":
            # draw red line for duration
            if time.time() >= animation.endtime:
                if animation.firer == "enemyship" and animation.missed != False:
                    angle = 360 - (animation.angle) + 90 + myship.rotation
                    angle = functions.clampAngle(angle)
                    shieldnum = int(((angle + 45) / 360) * 4)
                    if angle <= 45: shieldnum = 0
                    if angle >= 315: shieldnum = 0
                    if shieldnum >= 4: shieldnum = 3
                    shieldcharge = myship.shields[shieldnum].charge
                    if shieldcharge <= 0:
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
                if animation.firer == "myship":
                    # already gets handled on myship.fireNextWeapon code
                    pass
                animations.pop(i)
            if animation.firer == "myship":
                if animation.hitship != None:
                    r = animation.hitship.width / 2 + 10
                    x5 = animation.hitship.x
                    y5 = animation.hitship.y
                    x3 = animation.endpos[0] - x5
                    y3 = animation.endpos[1] - y5
                    x4 = myship.x - x5
                    y4 = myship.y - y5
                    intercept = functions.lineCircleIntercept(x3, y3, x4, y4, x5, y5, r)
                    if intercept != None:
                        closesthit = Point()
                        closesthit.x, closesthit.y = intercept
                        animation.hitpoint = [closesthit.x, closesthit.y]
                if len(animation.hitpoint) == 0:
                    enemydrawX = centre[0] + animation.endpos[0] - myship.x
                    enemydrawY = centre[1] - animation.endpos[1] + myship.y
                elif animation.hit and animation.shielddown:
                    midpoint = functions.midpoint(animation.hitpoint[0], animation.hitpoint[1], x5, y5)
                    animation.hitpoint[0] = midpoint[0]
                    animation.hitpoint[1] = midpoint[1]
                    enemydrawX = centre[0] + animation.hitpoint[0] - myship.x
                    enemydrawY = centre[1] - animation.hitpoint[1] + myship.y
                else:
                    enemydrawX = centre[0] + animation.hitpoint[0] - myship.x
                    enemydrawY = centre[1] - animation.hitpoint[1] + myship.y
                lineendX = centre[0]
                lineendY = centre[1]
                linewidth = 2
                if animation.classnum == 2: linewidth = 6
                pygame.draw.line(screen, animation.colour, (lineendX, lineendY), (
                    enemydrawX, enemydrawY), linewidth)
            elif animation.firer == "enemyship":
                enemydrawX = centre[0] + animation.target.x - myship.x
                enemydrawY = centre[1] - animation.target.y + myship.y
                endposdrawX = centre[0] + animation.endpos[0] - myship.x
                endposdrawY = centre[1] - animation.endpos[1] + myship.y
                angle_deg = animation.angle - 180
                angle_rads = angle_deg * math.pi / 180
                lineendX = centre[0] + math.cos(angle_rads) * (myship.width / 2 + 10)
                lineendY = centre[1] + math.sin(angle_rads) * (myship.width / 2 + 10)
                angle = 360 - (animation.angle) + 90 + myship.rotation
                angle = functions.clampAngle(angle)
                shieldnum = int(((angle + 45) / 360) * 4)
                if angle <= 45: shieldnum = 0
                if angle >= 315: shieldnum = 0
                if shieldnum >= 4: shieldnum = 3
                if myship.shields[shieldnum].charge <= 0 and animation.missed == False:
                    lineendX = centre[0]
                    lineendY = centre[1]
                elif animation.missed:
                    lineendX = endposdrawX
                    lineendY = endposdrawY
                linewidth = 2
                if animation.classnum == 2: linewidth = 6
                pygame.draw.line(screen, animation.colour, (lineendX, lineendY), (
                    enemydrawX - animation.target.width / 2 + 30,
                    enemydrawY - animation.target.width / 2 + 30), linewidth)

        if animation.type == "explosion":
            time_elapsed = time.time() - animation.starttime
            if time.time() >= animation.endtime:
                if animation.targettype != "myship":
                    enemyships.pop(animation.hitship.index)
                    loot = random.randint(500, 1500)
                    gameinfo.credits += loot
                    gameinfo.gamemessage = "Looted " + str(loot) + " credits"
                    gameinfo.gamemessagedisplayed = time.time()
                animations.pop(i)
                functions.reIndexEnemies(enemyships)
                myship.targeted = None
                break
            if animation.targettype == "myship":
                drawX = centre[0]
                drawY = centre[1]
            else:
                drawX = centre[0] + animation.hitship.x - myship.x
                drawY = centre[1] - animation.hitship.y + myship.y
            circlesize = 160 * (0.25 - time_elapsed)
            pygame.draw.circle(screen, (255, 50, 50), (drawX - animation.width / 2 + 30,
                                                       drawY - animation.width / 2 + 30),
                               circlesize)
        elif animation.type == "torpedo" or animation.type == "bullet":
            if time.time() >= animation.endtime:
                # collision code here
                animations.pop(i)
                i-=1
            if animation.firer == "myship" or True:
                drawX = centre[0] + animation.x - myship.x
                drawY = centre[1] - animation.y + myship.y
                width = 5
                if animation.type == "bullet": width = 2
                pygame.draw.circle(screen, animation.colour, (drawX,
                                                           drawY),
                                   width)


def renderFrame(screen, stars, myship, enemyships, spacestations, images, shipIMG, enemyshipIMG, spacestationIMG, gameinfo, animations):
    if gameinfo.screen == "upgrademenu":
        renderUpgradeMenu(screen, images, gameinfo, myship)
    if gameinfo.screen == "stationmenu":
        renderStationMenu(screen, images, gameinfo, myship, spacestations)
    if gameinfo.screen == "mainmenu":
        renderMainMenu(screen, images, gameinfo)
    if gameinfo.screen == "credits":
        renderCredits(screen, images, gameinfo)
    if gameinfo.screen == "map":
        renderMap(screen, gameinfo, myship, spacestations)

    if gameinfo.screen == "game":
        renderGame(screen, stars, myship, gameinfo, spacestations, enemyships, shipIMG, animations, images)
    for button in gameinfo.buttons:
        if button.screen == gameinfo.screen:
            button.render(screen, gameinfo)
    for message in gameinfo.messages:
        if message.screen == gameinfo.screen and message.visible == True:
            messageText = message.font.render(message.message, False, (255, 255, 255))
            screen.blit(messageText, (message.x, message.y))