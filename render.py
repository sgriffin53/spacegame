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
    pointB_y = pointA_y
    pointC_x = pointA_x
    pointC_y = ship.y - height / 2
    pointD_x = pointB_x
    pointD_y = pointC_y
    if obj_right >= pointA_x and obj_left <= pointB_x and obj_top >= pointC_y and obj_bottom <= pointA_y:
        return True
    return False

def drawMyShields(screen, myship, gameinfo):
    myship_rotation_rads = (360 - myship.rotation) * math.pi / 180
    start_ang = 43
    start_ang_rads = start_ang * math.pi / 180 + myship_rotation_rads
    end_ang_rads = (start_ang + 88) * math.pi / 180 + myship_rotation_rads
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

def drawEnemyShields(screen, enemyship, myship, gameinfo):
    enemyship_rotation_rads = (360 - enemyship.rotation) * math.pi / 180
    centre = (gameinfo. width / 2, gameinfo.height / 2)
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


def renderFrame(screen, stars, myship, enemyships, spacestations, frameinfo, images, shipIMG, enemyshipIMG, spacestationIMG, gameinfo, animations):
    if gameinfo.screen == "stationmenu":
        screen.fill((0, 0, 0))
        bg = images[1]
        bg = pygame.transform.scale(bg, (gameinfo.width, gameinfo.height))
        screen.blit(bg, (0, 0))
        titlefont = pygame.font.SysFont('Calibri', 60, 1)
        titleText = titlefont.render("Space station " + str(myship.closestStation(spacestations).index), False,
                                     (255, 255, 255))
        screen.blit(titleText, (460, 30))
        menulabelfont = pygame.font.SysFont('Calibri', 30)
        repaircost = (myship.maxhull - myship.hull) * 0.5
        repaircost += (myship.shields[0].maxcharge - myship.shields[0].charge) * 0.2
        repaircost += (myship.shields[1].maxcharge - myship.shields[1].charge) * 0.2
        repaircost += (myship.shields[2].maxcharge - myship.shields[2].charge) * 0.2
        repaircost += (myship.shields[3].maxcharge - myship.shields[3].charge) * 0.2
        repaircost = int(repaircost)
        repairText = menulabelfont.render("Repair Ship (Cost " + str(repaircost) + ")", False, (255, 255, 255))
        screen.blit(repairText, (50, 130))
    if gameinfo.screen == "mainmenu":
        screen.fill((0, 0, 0))
        bg = images[0]
        bg = pygame.transform.scale(bg, (gameinfo.width, gameinfo.height))
        screen.blit(bg, (0, 0))
        titlefont = pygame.font.SysFont('Calibri Bold', 70 )
        titleText = titlefont.render("Space Shooter Game", False,
                                 (255, 255, 255))
        screen.blit(titleText, (gameinfo.width / 2 - 230, 30))
    if gameinfo.screen == "credits":
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
        musicByText = creditsfont.render("Music and sound effects by: Eric Matyas (www.soundimage.com)", False, (255, 255, 255))
        screen.blit(musicByText, (350, 220))
        artByText = creditsfont.render("Art by:", False, (255, 255, 255))
        screen.blit(artByText, (420, 290))
        millionthVectorText = creditsfont.render("MillionthVector (http://millionthvector.blogspot.de)", False, (255, 255, 255))
        screen.blit(millionthVectorText, (495, 290))
        eikesterText = creditsfont.render("Eikester", False, (255, 255, 255))
        screen.blit(eikesterText, (495, 330))
        craftpixText = creditsfont.render("CraftPix.net 2D Game Assets", False, (255, 255, 255))
        screen.blit(craftpixText, (495, 370))
        attributionText = creditsfont.render("See attribution.txt for full attribution information.", False, (255, 255, 255))
        screen.blit(attributionText, (440, 440))
    if gameinfo.screen == "map":
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
        thisfont = pygame.font.SysFont('Calibri', 24 )
        noStationText = stationInfoText = thisfont.render("No Station Selected", False,
                                 (255, 255, 255))
        stationInfoText = thisfont.render("Space Station " + str(gameinfo.selectedstation), False,
                                 (255, 255, 255))
        dispdist = int(dist)
        if (dist >= 1000000): dispdist = str(round(dist / 1000000,2)) + "M"
        elif (dist >= 1000): dispdist = str(round(dist / 1000,2)) + "K"
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


    if gameinfo.screen == "game":
        # Fill the background with white
        screen.fill((0, 0, 0))

        drawStars(screen, stars, myship, gameinfo)

        # Calculate centre

        centre = (gameinfo.width / 2, gameinfo.height / 2)

        i = -1
        enemytotarget = False
        targeteddrawX = 0
        targeteddrawY = 0
        targetedenemy = None
        targetedship = None
        for enemyship in enemyships:
            i += 1
            dist = functions.distance(myship, enemyship)
            if dist > 2000: continue
            if (not onScreen(enemyship, myship, gameinfo)):
                drawTargetLine(screen, myship, enemyship, spacestations, gameinfo)
                continue
            # Draw enemy ship
            enemydrawX = centre[0] + enemyship.x - myship.x
            enemydrawY = centre[1] - enemyship.y + myship.y
            if enemyship.visible:
                #screen.blit(enemyshipIMG, (enemydrawX, enemydrawY))
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
                                     (enemydrawX - enemyship.width / 2 - margin / 2, enemydrawY - enemyship.width / 2 - margin / 2,
                                      enemyship.width + margin,
                                      enemyship.width + margin), 2)
                    targeteddrawX = enemydrawX
                    targeteddrawY = enemydrawY
                    targetedship = enemyships[myship.targeted]
                    enemytotarget = True
                    targetedenemy = enemyship

                #thisfont = pygame.font.SysFont('Fixedsys', 16)
                #indexText = thisfont.render(str(i), False, (255, 255, 255))
                #distanceText = thisfont.render(str(int(dist)), False, (255, 255, 255))
                #xyText = thisfont.render("xy: (" + str(int(enemyship.x)) + "," + str(int(enemyship.y)) + ")", False, (255, 255, 255))
                #screen.blit(indexText, (enemydrawX - 10, enemydrawY - 10))
                #screen.blit(distanceText, (enemydrawX - 10, enemydrawY + 20))
                #screen.blit(xyText, (enemydrawX - 10, enemydrawY + 50))

        # Draw space station
        for spacestation in spacestations:
            spacestationX = centre[0] + spacestation.x - myship.x
            spacestationY = centre[1] - spacestation.y + myship.y
            dist = functions.distance(myship, spacestation)
            img = spacestation.image
            if onScreen(spacestation, myship, gameinfo): # on screen
                (img, spacestationcentre) = rot_center(img, spacestation.rotation, spacestationX, spacestationY)
                screen.blit(img, spacestationcentre)
                spacestation.centre = spacestationcentre
            if dist < 3000:
                pygame.draw.circle(screen, (0, 0, 255), (spacestationX, spacestationY), spacestation.radius + 400, 1)
            elif dist < 5000: # not on screen and within short range sensor range
                drawTargetLine(screen, myship, spacestation, spacestations, gameinfo)

        # Draw my ship

        (shipIMG, newcentre) = rot_center(shipIMG, myship.rotation, centre[0], centre[1]) # rotate ship appropriately
        if myship.alive:
            screen.blit(shipIMG, newcentre) # draw ship
            drawMyHealthBar(screen, myship, gameinfo)
            drawMyShields(screen, myship, gameinfo)

        # Draw text:

        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        myfont = gameinfo.myfont
        velText = myfont.render('Velocity: ' + str(round(myship.vel,1)), False, (255, 255, 255))
        shipXText = myfont.render('X: ' + str(round(myship.x,0)), False, (255, 255, 255))
        shipYText = myfont.render('Y: ' + str(round(myship.y,0)), False, (255, 255, 255))
        sectorText = myfont.render('Sector: ' + str(myship.gridsector), False, (255, 255, 255))
        screen.blit(shipXText, (2, 540))
        screen.blit(shipYText, (2, 560))
        screen.blit(velText, (2, 580))
        screen.blit(sectorText, (2, 600))
        curfps = get_fps(gameinfo)
        fps_text = myfont.render(str(curfps) + " FPS", 1, pygame.Color("coral"))
        screen.blit(fps_text, (10, 5))
        width = gameinfo.width
        height = gameinfo.height
        centre = (width / 2, height / 2)
        #enemyshipIMG = pygame.image.load(os.path.join('images', 'enemyship.png')).convert_alpha()
        #screen.blit(enemyshipIMG, (drawX, drawY))
        #screen.set_at((int(drawX), int(drawY)), (255, 255, 0))
        if gameinfo.redalert:
            redalert_text = myfont.render("Red Alert", 1, (255, 0, 0))
            screen.blit(redalert_text, (80, 5))
        i = -1
        for animation in animations:
            i+=1
            drawX = targeteddrawX
            drawY = targeteddrawY
            if animation.targettype == "myship":
                drawX = centre[0]
                drawY = centre[1]
            if animation.type == "laser":
                # draw red line for duration
                if time.time() >= animation.endtime:
                    if animation.firer == "enemyship":
                        angle = 360 - (animation.angle) + 90 + myship.rotation
                        if angle < 0: angle += 360
                        if angle >= 360: angle -= 360
                        shieldnum = int(((angle + 45)/ 360) * 4)
                        if angle <= 45: shieldnum = 0
                        if angle >= 315: shieldnum = 0
                        if shieldnum >= 4: shieldnum = 3
                        shieldcharge = myship.shields[shieldnum].charge
                        if shieldcharge <= 0:
                            myship.hull -= 10
                            if myship.hull <= 0:
                                myship.alive = False
                                gameinfo.alive = False
                                gameinfo.lastdied = time.time()
                                myship.vel = 0
                                myship.rotaccel = 0
                                myship.accel = 0
                                myship.explode(animations)
                        else:
                            myship.shields[shieldnum].charge -= 20
                    if animation.firer == "myship":
                        enemyship = animation.target
                        angle = 360 - (animation.angle) + 90 + enemyship.rotation
                        if angle < 0: angle += 360
                        if angle >= 360: angle -= 360
                        shieldnum = int(((angle + 45)/ 360) * 4)
                        if angle <= 45: shieldnum = 0
                        if angle >= 315: shieldnum = 0
                        if shieldnum >= 4: shieldnum = 3
                        shieldcharge = enemyship.shields[shieldnum].charge
                        if shieldcharge <= 0:
                            enemyship.hull -= 10
                            if enemyship.hull <= 50 and enemyship.state != "retreat":
                                enemyship.state = "retreat"
                                enemyship.startRetreat(enemyship)
                            if enemyship.hull <= 0:
                                enemyship.explode(animations)
                        else:
                            enemyship.shields[shieldnum].charge -= 20
                    animations.pop(i)
                    break
                if animation.firer == "myship" and myship.targeted != None:
                    enemyship = enemyships[myship.targeted]
                    angle_deg = animation.angle - 180
                    angle_rads = angle_deg * math.pi / 180

                    enemydrawX = centre[0] + animation.target.x - myship.x + math.cos(angle_rads) * (enemyship.width / 2 + 10)
                    enemydrawY = centre[1] - animation.target.y + myship.y + math.sin(angle_rads) * (enemyship.width / 2 + 10)
                    angle = 360 - (animation.angle) + 90 + enemyship.rotation
                    if angle < 0: angle += 360
                    if angle >= 360: angle -= 360
                    shieldnum = int(((angle + 45) / 360) * 4)
                    if shieldnum >= 4: shieldnum = 3
                    if angle <= 45: shieldnum = 0
                    if angle >= 315: shieldnum = 0
                    shieldcharge = enemyship.shields[shieldnum].charge
                    if shieldcharge <= 0:
                        enemydrawX = centre[0] + animation.target.x - myship.x
                        enemydrawY = centre[1] - animation.target.y + myship.y
                    lineendX = centre[0]
                    lineendY = centre[1]
                    pygame.draw.line(screen, animation.colour, (lineendX, lineendY), (
                    enemydrawX - enemyships[0].width / 2 + 30,
                    enemydrawY - enemyships[0].width / 2 + 30), 4)
                elif animation.firer == "enemyship":
                    enemydrawX = centre[0] + animation.target.x - myship.x
                    enemydrawY = centre[1] - animation.target.y + myship.y
                    angle_deg = animation.angle - 180
                    angle_rads = angle_deg * math.pi / 180
                    lineendX = centre[0] + math.cos(angle_rads) * (myship.width / 2 + 10)
                    lineendY = centre[1] + math.sin(angle_rads) * (myship.width / 2 + 10)
                    angle = 360 - (animation.angle) + 90 + myship.rotation

                    if angle < 0: angle += 360
                    if angle >= 360: angle -= 360
                    shieldnum = int(((angle + 45) / 360) * 4)
                    if shieldnum >= 4: shieldnum = 3
                    if myship.shields[shieldnum].charge <= 0:
                        lineendX = centre[0]
                        lineendY = centre[1]
                    pygame.draw.line(screen, animation.colour, (lineendX, lineendY), (
                    enemydrawX - enemyships[0].width / 2 + 30,
                    enemydrawY - enemyships[0].width / 2 + 30), 4)

            if animation.type == "explosion":
                time_elapsed = time.time() - animation.starttime
                if time.time() >= animation.endtime:
                    if animation.targettype != "myship" and myship.targeted != None: enemyships.pop(enemyships[myship.targeted].index)
                    animations.pop(i)
                    functions.reIndexEnemies(enemyships)
                    myship.targeted = None
                    break
                circlesize = 160 * (0.25 - time_elapsed)
                pygame.draw.circle(screen, (255, 50, 50), (drawX - animation.width / 2 + 30,
                                                          drawY - animation.width / 2 + 30),
                                   circlesize)
            elif animation.type == "torpedo":
                if time.time() >= animation.endtime:
                    if animation.firer == "enemyship":
                        angle = 360 - (animation.angle) + 90 + myship.rotation
                        if angle < 0: angle += 360
                        if angle >= 360: angle -= 360
                        shieldnum = int(((angle + 45)/ 360) * 4)
                        if shieldnum >= 4: shieldnum = 3
                        if angle <= 45: shieldnum = 0
                        if angle >= 315: shieldnum = 0
                        shieldcharge = myship.shields[shieldnum].charge
                        if shieldcharge <= 0:
                            myship.hull -= 20
                            if myship.hull <= 0:
                                myship.alive = False
                                gameinfo.alive = False
                                gameinfo.lastdied = time.time()
                                myship.vel = 0
                                myship.rotaccel = 0
                                myship.accel = 0
                                myship.explode(animations)
                        else:
                            myship.shields[shieldnum].charge -= 20
                    if animation.firer == "myship" and targetedship != None:
                        enemyship = animation.target
                        angle = 360 - (animation.angle) + 90 + enemyship.rotation
                        if angle < 0: angle += 360
                        if angle >= 360: angle -= 360
                        shieldnum = int(((angle + 45)/ 360) * 4)
                        if shieldnum >= 4: shieldnum = 3
                        if angle <= 45: shieldnum = 0
                        if angle >= 315: shieldnum = 0
                        shieldcharge = enemyship.shields[shieldnum].charge
                        if shieldcharge <= 0:
                            enemyship.hull -= 10
                            if enemyship.hull <= 50 and enemyship.state != "retreat":
                                enemyship.state = "retreat"
                                enemyship.startRetreat(enemyship)
                            if enemyship.hull <= 0:
                                enemyship.explode(animations)
                        else:
                            enemyship.shields[shieldnum].charge -= 20
                    animations.pop(i)
                    break
                if animation.firer == "myship":
                    targetx = myship.x
                    targety = myship.y
                    dy = targety - animation.targetship.y
                    dx = targetx - animation.targetship.x
                    angle_deg = 360 - math.atan2(dy, dx) * 180 / math.pi - 90
                    angle_rads = angle_deg * math.pi / 180
                    completed = (time.time() - animation.starttime) / animation.duration
                    endpoint = Point()
                    endpoint.x = myship.x
                    endpoint.y = myship.y
                    startpoint = Point()
                    startpoint.x = animation.startpos[0]
                    startpoint.y = animation.startpos[1]
                    dist = functions.distance(myship, animation.targetship)
                    drawX = centre[0] + math.sin(angle_rads) * dist * completed
                    drawY = centre[1] - math.cos(angle_rads) * dist * completed
                    pygame.draw.circle(screen, (255, 0, 0), (drawX, drawY), 3)
                elif animation.firer == "enemyship":
                    targetx = myship.x
                    targety = myship.y
                    dy = targety - animation.startpos[1]
                    dx = targetx - animation.startpos[0]
                    angle_deg = 360 - math.atan2(dy, dx) * 180 / math.pi - 270
                    angle_rads = angle_deg * math.pi / 180
                    completed = (time.time() - animation.starttime) / animation.duration
                    endpoint = Point()
                    endpoint.x = myship.x
                    endpoint.y = myship.y
                    startpoint = Point()
                    startpoint.x = animation.startpos[0]
                    startpoint.y = animation.startpos[1]
                    dist = functions.distance(myship, startpoint)
                    enemydrawX = centre[0] + startpoint.x - myship.x
                    enemydrawY = centre[1] - startpoint.y + myship.y
                    drawX = enemydrawX + math.sin(angle_rads) * dist * completed
                    drawY = enemydrawY - math.cos(angle_rads) * dist * completed
                    pygame.draw.circle(screen, (255, 0, 0), (drawX, drawY), 3)
    for button in gameinfo.buttons:
        if button.screen == gameinfo.screen:
            button.render(screen, gameinfo)


