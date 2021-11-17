# Import and initialize the pygame library

import pygame
import os
import random
import time
import physics
import keypresses
import collision
import render
import AI
import station
import functions
import pygame_menu
import enemies
from myship import MyShip
from classes import Music, Sound, Weapon, GameInfo, FrameInfo, Shield, Button, Message, Resolution

pygame.init()
pygame.font.init()  # you have to call this at the start,
pygame.display.set_caption('Stardawg 3000')

# create game info

gameinfo = GameInfo()
gameinfo.credits = 1000
for i in range(5):
    gameinfo.resolutions.append(Resolution(i))

# generate warp map menu stars

for i in range(0, 200):
    thisX = random.randint(200, 800)
    thisY = random.randint(30, 630)
    gameinfo.mapstars.append((thisX, thisY))

nativewidth = 1280
nativeheight = 768
gameinfo.resolution = Resolution(3)
gameinfo.width = gameinfo.resolution.width
gameinfo.height = gameinfo.resolution.height
gameinfo.nativeheight = nativeheight
gameinfo.nativewidth = nativewidth
gameinfo.resindex = 3
gameinfo.resolution = gameinfo.resolutions[gameinfo.resindex]
width = gameinfo.resolution.width
height = gameinfo.resolution.height
gameinfo.clock = pygame.time.Clock()
fullscreen = False
gameinfo.fullscreen = fullscreen

screen = pygame.display.set_mode([width, height]) # don't set full screen mode to start or it messes up switching resolutions

# Set up the drawing window
if not fullscreen:
    pass
#    screen = pygame.display.set_mode([width, height])
else:
    screen = pygame.display.set_mode([width, height], pygame.FULLSCREEN)

spacestationIMG = pygame.image.load(os.path.join('images', 'station.png')).convert_alpha()
shipIMG = pygame.image.load(os.path.join('images','ship.png')).convert_alpha()
enemyshipIMG = pygame.image.load(os.path.join('images', 'enemyship.png')).convert_alpha()

# generate stars

stars = []
for i in range(1250):
  stars.append(dict({'x': 0, 'y': 0}))
  stars[i]['x'] = random.random()*width
  stars[i]['y'] = random.random()*height

animations = []
music = []
sounds = []

path = 'music'

files = os.listdir(path)

# load music files

i = -1
for f in files:
    i+=1
    music.append(Music())
    music[i].file = os.path.join('music', f)

sounds.append(Sound())
i = len(sounds) - 1
sounds[i].file = os.path.join('sounds', 'Laser-Shot-1.mp3')
sounds[i].mixer = pygame.mixer.Sound(sounds[i].file)

# spawn space stations

spacestations = []

station.spawnSpaceStations(spacestations)


# create my ship object

myship = MyShip()
myship.image = pygame.image.load(os.path.join('images','ship.png')).convert_alpha()
myship.weapons.append(Weapon("laser-c1"))
myship.weapons.append(Weapon("torpedo-c1"))
myship.weapons.append(None)
myship.weapons.append(None)
for i in range(4): myship.shields.append(Shield("shield-c2")) # generate 4 shields
for shield in myship.shields:
    shield.charge = 250
    shield.maxcharge = 250

myship.respawn(spacestations[7])

# spawn enemies

enemyships = []

# Run until the user asks to quit
running = True
i = 0
curfps = 0
alt_pressed = False
enter_pressed = False
last_phys_tick = time.time()
last_keys_poll = time.time()

gameinfo.screen = "mainmenu"

images = []
images.append(pygame.image.load(os.path.join('images','GUI','bg.png')))
images.append(pygame.image.load(os.path.join('images','GUI','Window.png')))
images.append(pygame.image.load(os.path.join('images','plasmabullet.png')))
images.append(pygame.image.load(os.path.join('images','plasmatorpedo.png')))
images.append(pygame.image.load(os.path.join('images','GUI','Backward_BTN.png')))
images.append(pygame.image.load(os.path.join('images','GUI','Backward_BTN_hover.png')))
images.append(pygame.image.load(os.path.join('images','GUI','Forward_BTN.png')))
images.append(pygame.image.load(os.path.join('images','GUI','Forward_BTN_hover.png')))

# create list of shields

for i in range(10):
    shieldstring = "shield-c" + str(i+1)
    gameinfo.allshields.append(Shield(shieldstring))

# create list of weapons

weaponnames = ["Laser", "Bullet", "Torpedo", "Flux Ray", "Disruptor", "Radial Burst", "Particle Beam"]
weaponshortnames = ["laser", "bullet", "torpedo", "fluxray", "disruptor", "radialburst", "particlebeam"]
maxclasses = {"laser": 2, "bullet": 1, "torpedo": 2, "fluxray": 3, "disruptor": 1, "particlebeam": 1, "radialburst": 1}
for weapon in weaponshortnames:
    for i in range(maxclasses[weapon]):
        id = weapon + "-c" + str(i+1)
        gameinfo.allweapons.append(Weapon(id))

# add buttons

defaultfont = pygame.font.SysFont('Calibri', 34)
smallfont = pygame.font.SysFont('Calibri', 22)

# main menu buttons

gameinfo.buttons.append(Button(500, 200, 300, 50, 80, 8, "Start Game", (255, 255, 255), "mainmenu", "startgame", defaultfont))
gameinfo.buttons.append(Button(500, 280, 300, 50, 100, 8, "Tutorial", (255, 255, 255), "mainmenu", None, defaultfont))
gameinfo.buttons.append(Button(500, 360, 300, 50, 105, 8, "Credits", (255, 255, 255), "mainmenu", "creditsclick", defaultfont))
gameinfo.buttons.append(Button(500, 440, 300, 50, 125, 8, "Exit", (255, 255, 255), "mainmenu", "exit", defaultfont))

# map buttons

gameinfo.buttons.append(Button(830, 120, 200, 50, 25, 8, "Warp Here", (255, 255, 255), "map", "warpclick", defaultfont))

# credits buttons

gameinfo.buttons.append(Button(520, 520, 300, 50, 55, 8, "Back to Menu", (255, 255, 255), "credits", "creditsbackclick", defaultfont))

# station menu buttons

gameinfo.buttons.append(Button(50, 230, 200, 50, 55, 8, "Repair", (255, 255, 255), "stationmenu", "repairclick", defaultfont))
gameinfo.buttons.append(Button(400, 230, 200, 50, 39, 8, "Upgrade", (255, 255, 255), "stationmenu", "upgradeclick", defaultfont))
gameinfo.buttons.append(Button(1000, 640, 250, 50, 30, 8, "Back to Game", (255, 255, 255), "stationmenu", "stationbackclick", defaultfont))

# upgrade menu buttons

gameinfo.buttons.append(Button(90, 230, 150, 50, 13, 8, "Upgrade", (255, 255, 255), "upgrademenu", "baseshipupgradeclick", defaultfont))
gameinfo.buttons.append(Button(1000, 640, 250, 50, 30, 8, "Back to Menu", (255, 255, 255), "upgrademenu", "upgradebackclick", defaultfont))
gameinfo.buttons.append(Button(660, 115, 150, 35, 35, 8, "Upgrade", (255, 255, 255), "upgrademenu", "upgradewarpenginesclick", smallfont))
gameinfo.buttons.append(Button(660, 155, 150, 35, 35, 8, "Upgrade", (255, 255, 255), "upgrademenu", "upgradecombatenginesclick", smallfont))
gameinfo.buttons.append(Button(660, 195, 150, 35, 35, 8, "Upgrade", (255, 255, 255), "upgrademenu", "upgradeshieldsclick", smallfont))
gameinfo.buttons.append(Button(835, 235, 150, 35, 35, 8, "Upgrade", (255, 255, 255), "upgrademenu", "upgradeweapons1stclick", smallfont))
gameinfo.buttons.append(Button(835, 275, 150, 35, 35, 8, "Upgrade", (255, 255, 255), "upgrademenu", "upgradeweapons2ndclick", smallfont))
gameinfo.buttons.append(Button(835, 315, 150, 35, 35, 8, "Upgrade", (255, 255, 255), "upgrademenu", "upgradeweapons3rdclick", smallfont))
gameinfo.buttons.append(Button(835, 355, 150, 35, 35, 8, "Upgrade", (255, 255, 255), "upgrademenu", "upgradeweapons4thclick", smallfont))

# shields upgrade menu buttons

gameinfo.buttons.append(Button(1000, 640, 250, 50, 30, 8, "Back to Menu", (255, 255, 255), "shieldsupgrademenu", "shieldsupgradebackclick", smallfont))

leftbutton = Button(560, 180, 210, 210, 80, 8, "", (255, 255, 255), "shieldsupgrademenu", "shieldselectionleft",
                    defaultfont)
leftbutton.image = images[4]
scalefactor = 6
leftbutton.width = 210 / scalefactor
leftbutton.height = 210 / scalefactor
gameinfo.buttons.append(leftbutton)

rightbutton = Button(720, 180, 210, 210, 80, 8, "", (255, 255, 255), "shieldsupgrademenu", "shieldselectionright",
                    defaultfont)
rightbutton.image = images[7]
scalefactor = 6
rightbutton.width = 210 / scalefactor
rightbutton.height = 210 / scalefactor
gameinfo.buttons.append(rightbutton)

leftbutton_weapons = Button(560, 220, 210, 210, 80, 8, "", (255, 255, 255), "weaponsupgrademenu", "weaponselectionleft",
                    defaultfont)
leftbutton_weapons.image = images[4]
scalefactor = 6
leftbutton_weapons.width = 210 / scalefactor
leftbutton_weapons.height = 210 / scalefactor
gameinfo.buttons.append(leftbutton_weapons)

rightbutton_weapons = Button(800, 220, 210, 210, 80, 8, "", (255, 255, 255), "weaponsupgrademenu", "weaponselectionright",
                    defaultfont)
rightbutton_weapons.image = images[6]
scalefactor = 6
rightbutton_weapons.width = 210 / scalefactor
rightbutton_weapons.height = 210 / scalefactor
gameinfo.buttons.append(rightbutton_weapons)

leftbutton_weapons2 = Button(560, 260, 210, 210, 80, 8, "", (255, 255, 255), "weaponsupgrademenu", "weaponclassselectionleft",
                    defaultfont)
leftbutton_weapons2.image = images[4]
scalefactor = 6
leftbutton_weapons2.width = 210 / scalefactor
leftbutton_weapons2.height = 210 / scalefactor
gameinfo.buttons.append(leftbutton_weapons2)

rightbutton_weapons2 = Button(800, 260, 210, 210, 80, 8, "", (255, 255, 255), "weaponsupgrademenu", "weaponclassselectionright",
                    defaultfont)
rightbutton_weapons2.image = images[6]
scalefactor = 6
rightbutton_weapons2.width = 210 / scalefactor
rightbutton_weapons2.height = 210 / scalefactor
gameinfo.buttons.append(rightbutton_weapons2)

gameinfo.buttons.append(Button(1000, 640, 250, 50, 30, 8, "Back to Menu", (255, 255, 255), "shieldsupgrademenu", "shieldsupgradebackclick", defaultfont))

# shield upgrade button

gameinfo.buttons.append(Button(500, 410, 200, 50, 39, 8, "Upgrade", (255, 255, 255), "shieldsupgrademenu", "shieldsupgradeclick", defaultfont))

# weapon upgrade button

gameinfo.buttons.append(Button(500, 510, 200, 50, 39, 8, "Upgrade", (255, 255, 255), "weaponsupgrademenu", "weaponsupgradeclick", defaultfont))

# back to menu button on weapons upgrade menu

gameinfo.buttons.append(Button(1000, 640, 250, 50, 30, 8, "Back to Menu", (255, 255, 255), "weaponsupgrademenu", "weaponsupgradebackclick", defaultfont))

# Add messages

gameinfo.messages.append(Message(50, 290, "No Repair Needed", "stationmenu", pygame.font.SysFont('Calibri', 30)))

# shields upgrade screen message

gameinfo.messages.append(Message(500, 480, "Shields upgraded", "shieldsupgrademenu", gameinfo.resolution.normalfont))

# weapon upgrade screen message

gameinfo.messages.append(Message(500, 590, "Weapon upgraded", "weaponsupgrademenu", gameinfo.resolution.normalfont))
#functions.setResolution(width, height, gameinfo, screen, stars, images, spacestationIMG, shipIMG, enemyshipIMG)

# main game loop

while running:
    i+= 1
    if not gameinfo.alive:
        # respawn if we're dead and 5 seconds have passed
        time_since_died = time.time() - gameinfo.lastdied
        if time_since_died >= 5:
            gameinfo.alive = True
            myship.alive = True
            myship.respawn(myship.closestStation(spacestations))
    time_since_key_poll = time.time() - last_keys_poll

    # Full screen (alt+enter)

    event_get = pygame.event.get()
    for event in event_get:
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RALT or event.key == pygame.K_LALT):
                alt_pressed = True
            if event.key == pygame.K_RETURN:
                enter_pressed = True
    if alt_pressed and enter_pressed: # full screen with alt+enter
        width = gameinfo.resolution.width
        height = gameinfo.resolution.height
        if not fullscreen:
            screen = pygame.display.set_mode([width, height], pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode([width, height])
        fullscreen = not fullscreen
        gameinfo.fullscreen = fullscreen
        functions.setResolution(width, height, gameinfo, screen, stars, images, spacestationIMG, shipIMG, enemyshipIMG)
    keys = pygame.key.get_pressed()
    if not keys[pygame.K_RALT] and not keys[pygame.K_LALT]:
        alt_pressed = False
    if not keys[pygame.K_RETURN]:
        enter_pressed = False

    keypresses.detectKeyPresses(event_get, fullscreen, myship, enemyships, gameinfo, animations, sounds, spacestations, music, screen, stars, images, spacestationIMG, shipIMG, enemyshipIMG)
    cur_time = time.time()
    time_since_phys_tick = cur_time - last_phys_tick
    physics.physicsTick(myship, enemyships, spacestations, time_since_phys_tick, gameinfo, animations)
    last_phys_tick = cur_time
    collision.collisionDetection(myship, enemyships, spacestations)
    for enemyship in enemyships:
        AI.enemyAITick(myship, enemyship, spacestations, animations, sounds, gameinfo)
    myship.autoTick(gameinfo, spacestations)
    render.renderFrame(screen, stars, myship, enemyships, spacestations, images, shipIMG, enemyshipIMG, spacestationIMG, gameinfo, animations)
    gameinfo.clock.tick(165000)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()