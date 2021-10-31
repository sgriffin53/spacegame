import math
from classes import *
from myship import *
import station
import enemies

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

def playMusic(music):
    music_track = random.randint(0, len(music) - 1)
    music_playing = music[music_track]
    pygame.mixer.music.load(music_playing.file)
    pygame.mixer.music.play(-100000)

def startGame(gameinfo, myship, enemyships, spacestations, music):
    # spawn space stations

    spacestations = []

    station.spawnSpaceStations(spacestations)

    # create my ship object

    myship = MyShip()
    myship.weapons.append(Weapon("laser"))
    myship.weapons.append(Weapon("torpedo"))
    for i in range(4): myship.shields.append(ShipShield())
    for shield in myship.shields:
        shield.charge = 250
        shield.maxcharge = 250

    myship.respawn(spacestations[7])

    # spawn enemies

    enemyships = []

    enemies.spawnEnemyShips(enemyships, spacestations)
    functions.playMusic(music)
    gameinfo.screen = "game"