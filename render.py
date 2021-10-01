import time
import functions
import pygame

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

def drawTargetLine(screen, myship, enemyship, spacestation, gameinfo):
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

def renderFrame(screen, stars, myship, enemyships, spacestation, frameinfo, shipIMG, enemyshipIMG, spacestationIMG, gameinfo, animations):

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
    for enemyship in enemyships:
        i += 1
        dist = functions.distance(myship, enemyship)
        if enemyship.visible and myship.targeted == i:
            enemydrawX = centre[0] + enemyship.x - myship.x
            enemydrawY = centre[1] - enemyship.y + myship.y
            margin = 10
            pygame.draw.rect(screen, (255, 0, 0),
                             (enemydrawX - enemyship.width / 2 - 5, enemydrawY - enemyship.width / 2 - 5, enemyship.width + margin,
            enemyship.width + margin), 2)
            targeteddrawX = enemydrawX
            targeteddrawY = enemydrawY
            enemytotarget = True
            targetedenemy = enemyship

        if dist > 2000: continue
        if (not onScreen(enemyship, myship, gameinfo)):
            drawTargetLine(screen, myship, enemyship, spacestation, gameinfo)
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
            #thisfont = pygame.font.SysFont('Fixedsys', 16)
            #indexText = thisfont.render(str(i), False, (255, 255, 255))
            #distanceText = thisfont.render(str(int(dist)), False, (255, 255, 255))
            #xyText = thisfont.render("xy: (" + str(int(enemyship.x)) + "," + str(int(enemyship.y)) + ")", False, (255, 255, 255))
            #screen.blit(indexText, (enemydrawX - 10, enemydrawY - 10))
            #screen.blit(distanceText, (enemydrawX - 10, enemydrawY + 20))
            #screen.blit(xyText, (enemydrawX - 10, enemydrawY + 50))

    # Draw space station
    spacestationX = centre[0] + spacestation.x - myship.x
    spacestationY = centre[1] - spacestation.y + myship.y
    dist = functions.distance(myship, spacestation)
    if onScreen(spacestation, myship, gameinfo): # on screen
        (spacestationIMG, spacestationcentre) = rot_center(spacestationIMG, spacestation.rotation, spacestationX, spacestationY)
        screen.blit(spacestationIMG, spacestationcentre)
        spacestation.centre = spacestationcentre
    elif dist < 5000: # not on screen and within short range sensor range
        drawTargetLine(screen, myship, spacestation, spacestation, gameinfo)

    # Draw ship

    (shipIMG, newcentre) = rot_center(shipIMG, myship.rotation, centre[0], centre[1]) # rotate ship appropriately
    if myship.alive: screen.blit(shipIMG, newcentre)

    # Draw text:

    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    myfont = gameinfo.myfont
    velText = myfont.render('Velocity: ' + str(round(myship.vel,1)), False, (255, 255, 255))
    shipXText = myfont.render('X: ' + str(round(myship.x,0)), False, (255, 255, 255))
    shipYText = myfont.render('Y: ' + str(round(myship.y,0)), False, (255, 255, 255))
    screen.blit(shipXText, (2, 540))
    screen.blit(shipYText, (2, 560))
    screen.blit(velText, (2, 580))
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
                animations.pop(i)
                break
            enemydrawX = centre[0] + animation.endpos[0] - myship.x
            enemydrawY = centre[1] - animation.endpos[1] + myship.y
            pygame.draw.line(screen, animation.colour, (centre[0], centre[1]), (
            enemydrawX - enemyships[0].width / 2 + 30,
            enemydrawY - enemyships[0].width / 2 + 30), 4)
        if animation.type == "explosion":
            time_elapsed = time.time() - animation.starttime
            if time.time() >= animation.endtime:
                if animation.targettype != "myship": enemyships.pop(enemyships[myship.targeted].index)
                animations.pop(i)
                functions.reIndexEnemies(enemyships)
                myship.targeted = None
                break
            circlesize = 160 * (0.25 - time_elapsed)
            pygame.draw.circle(screen, (255, 50, 50), (drawX - animation.width / 2 + 30,
                                                      drawY - animation.width / 2 + 30),
                               circlesize)
