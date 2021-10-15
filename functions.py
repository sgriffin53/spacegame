import math
from classes import *
from myship import *
import station
import enemies

def distance(ship1, ship2):
    # c ^ 2 = a ^ 2 + b ^ 2
    # c = sqrt(a ^ 2 + b ^ 2)
    centrex1 = ship1.x
    centrey1 = ship1.y
    centrex2 = ship2.x
    centrey2 = ship2.y
    return math.sqrt((abs(centrex1 - centrex2) ** 2) + (abs(centrey1 - centrey2) ** 2))

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
    myship.weapons.append(Weapon())
    '''
    myship.weapons[0].type = "laser"
    myship.weapons[0].duration = 0.02
    myship.weapons[0].chargetime = 0.5
    myship.weapons[0].lastfired = 0
    myship.weapons[0].range = 600
    '''
    myship.weapons[0].type = "torpedo"
    myship.weapons[0].duration = 0.5
    myship.weapons[0].chargetime = 3
    myship.weapons[0].lastfired = 0
    myship.weapons[0].range = 600

    myship.weapons.append(Weapon())
    myship.weapons[1].type = "laser"
    myship.weapons[1].duration = 0.2
    myship.weapons[1].chargetime = 1
    myship.weapons[1].lastfired = 0
    myship.weapons[1].range = 600

    myship.shields.append(Shield())
    myship.shields.append(Shield())
    myship.shields.append(Shield())
    myship.shields.append(Shield())
    for shield in myship.shields:
        shield.charge = 250
        shield.maxcharge = 250

    myship.respawn(spacestations[7])

    # spawn enemies

    enemyships = []

    enemies.spawnEnemyShips(enemyships, spacestations)
    functions.playMusic(music)
    gameinfo.screen = "game"