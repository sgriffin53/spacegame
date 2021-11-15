import math
from classes import *
from myship import *
import station
import enemies

def midpoint(x1, y1, x2, y2):
    mid_x = (x2 + x1) / 2
    mid_y = (y2 + y1) / 2
    return [mid_x, mid_y]

def lineCircleIntercept(x3, y3, x4, y4, x5, y5, r):
    # returns x4, x5
    # see notes diagram
    # inputs:
    # r = radius
    # x5, y5 = circle centre
    # x3, y3 = line start
    # x4, y4 = line end
    # outputs:
    # x1, y1, x2, y2 = intercept points
    # returns just x1, y1 (closest intercept to x4, y4
    closesthit = None
    dx = x4 - x3
    dy = y4 - y3
    dr = math.sqrt(dx ** 2 + dy ** 2)
    D = x3 * y4 - x4 * y3
    discriminant = r ** 2 * dr ** 2 - D ** 2
    closesthit_dist = 999999999999
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
        point4 = Point()
        point4.x = x4
        point4.y = y5
        dist1 = functions.distance(mypoint, point4)
        mypoint2 = Point()
        mypoint2.x = x2
        mypoint2.y = y2
        dist2 = functions.distance(mypoint2, point4)
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
            return
        pointC.x = x2
        pointC.y = y2
        if not functions.isBetween(pointA, pointB, pointC):
            return
        if dist1 < closesthit_dist:
            closesthit_dist = dist1
            closesthit = mypoint
        if dist2 < closesthit_dist:
            closesthit_dist = dist2
            closesthit = mypoint2
    if closesthit == None: return None
    return closesthit.x, closesthit.y

def repairCost(myship):
    repaircost = (myship.maxhull - myship.hull) * 0.5
    repaircost += (myship.shields[0].maxcharge - myship.shields[0].charge) * 0.2
    repaircost += (myship.shields[1].maxcharge - myship.shields[1].charge) * 0.2
    repaircost += (myship.shields[2].maxcharge - myship.shields[2].charge) * 0.2
    repaircost += (myship.shields[3].maxcharge - myship.shields[3].charge) * 0.2
    return int(repaircost)

def angleBetween(a, b):
    dy = a.y - b.y
    dx = a.x - b.x
    angle_deg = 360 - math.atan2(dy, dx) * 180 / math.pi
    return angle_deg

def clampAngle(a):
    if a < 0: return a + 360
    if a > 360: return a - 360
    return a

def isBetween(a, b, c):
    minx = a.x
    maxx = b.x
    if minx > maxx:
        minx = b.x
        maxx = a.x
    miny = a.y
    maxy = b.y
    if miny > maxy:
        miny = b.y
        maxy = a.y
    if c.x >= minx and c.x <= maxx and c.y >= miny and c.y <= maxy:
        return True
    return False

def distance(ship1, ship2):
    return math.sqrt((abs(ship1.x - ship2.x) ** 2) + (abs(ship1.y - ship2.y) ** 2))

def reIndexEnemies(enemyships):
    i = -1
    for enemyship in enemyships:
        i+=1
        enemyship.index = i

def gridSector(ship):
    gridsize = 40000
    galaxysize = 2000000
    totsidegrids = galaxysize / gridsize
    x = int(ship.x / gridsize)
    y = int(ship.y / gridsize)
    sector = y * totsidegrids + x
    return int(sector)

def allowedSectors(sector):
    gridsize = 40000
    galaxysize = 2000000
    totsidegrids = int(galaxysize / gridsize)
    sector = sector
    allowed = []
    allowed.append(sector)
    allowed.append(sector - 1) # left
    allowed.append(sector + 1) # right
    allowed.append(sector - totsidegrids) # north
    allowed.append(sector - totsidegrids - 1) # northwest
    allowed.append(sector - totsidegrids + 1) # northeast
    allowed.append(sector + totsidegrids) # south
    allowed.append(sector + totsidegrids - 1) # southwest
    allowed.append(sector + totsidegrids + 1) # southeast
    return allowed

def scaleImages(screen, images, spacestationIMG, shipIMG, enemyshipIMG, gameinfo):
   # pass
   pygame.transform.scale(spacestationIMG, (screen.get_width() / 2560, screen.get_height() / 1440))
   pygame.transform.scale(shipIMG, (screen.get_width() / 2560, screen.get_height() / 1440))

def playMusic(music):
    music_track = random.randint(0, len(music) - 1)
    music_playing = music[music_track]
    pygame.mixer.music.load(music_playing.file)
    pygame.mixer.music.play(-100000)

def setResolution(width, height, gameinfo, screen, stars, images, spacestationIMG, shipIMG, enemyshipIMG):
    gameinfo.width = width
    gameinfo.height = height
    fullscreen = gameinfo.fullscreen
    if fullscreen:
        screen = pygame.display.set_mode([width, height], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([width, height])
    scaleImages(screen, images, spacestationIMG, shipIMG, enemyshipIMG, gameinfo)
    del stars[:]
    for i in range(1250):
        stars.append(dict({'x': 0, 'y': 0}))
        stars[i]['x'] = random.random() * width
        stars[i]['y'] = random.random() * height
    for button in gameinfo.buttons:
        button.font = gameinfo.resolution.buttonfont
        smallbuttons = ["upgradecombatenginesclick", "upgradeshieldsclick", "upgradewarpenginesclick"]
        if button.onclick in smallbuttons:
            button.font = gameinfo.resolution.smallbuttonfont

def scaleToScreen(width, height, gameinfo):
    newwidth = width * (gameinfo.width / gameinfo.nativewidth)
    newheight = height * (gameinfo.height / gameinfo.nativeheight)
    return newwidth, newheight

def startGame(gameinfo, myship, enemyships, spacestations, music):
    # spawn space stations

    spacestations = []

    station.spawnSpaceStations(spacestations)

    # create my ship object
    del myship.weapons[:]

    myship.weapons.append(Weapon("bullet-c1"))
    myship.weapons.append(Weapon("torpedo-c1"))
    myship.weapons.append(Weapon("fluxray-c1"))
    myship.weapons.append(Weapon("disruptor-c1"))
    for i in range(4): myship.shields.append(Shield("shield-c2"))

    myship.respawn(spacestations[7])

    # spawn enemies

    enemyships = enemies.spawnEnemyShips(enemyships, spacestations)
    functions.playMusic(music)
    gameinfo.screen = "game"
    # should be -> actually is
    # 0 -> 1
    # 1 -> 2
    # 2 -> 3
    # 3 -> 0
    #myship.shields[3].charge = 0