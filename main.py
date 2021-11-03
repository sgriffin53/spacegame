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
import enemies
from myship import MyShip
from classes import Music, Sound, Weapon, GameInfo, FrameInfo, Shield, Button, Message

pygame.init()
pygame.font.init()  # you have to call this at the start,
pygame.display.set_caption('Stardawg 3000')

# create game info

gameinfo = GameInfo()
gameinfo.credits = 1000

# generate warp map menu stars

for i in range(0, 200):
    thisX = random.randint(200, 800)
    thisY = random.randint(30, 630)
    gameinfo.mapstars.append((thisX, thisY))


width = 1280
height = 768
#width = 800
#height = 600
gameinfo.width = width
gameinfo.height = height
gameinfo.clock = pygame.time.Clock()

# Set up the drawing window
screen = pygame.display.set_mode([width, height])

spacestationIMG = pygame.image.load(os.path.join('images', 'station.png')).convert_alpha()
shipIMG = pygame.image.load(os.path.join('images','ship.png')).convert_alpha()
enemyshipIMG = pygame.image.load(os.path.join('images', 'enemyship.png')).convert_alpha()

fullscreen = False

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

# add buttons

defaultfont = pygame.font.SysFont('Calibri', 34)
smallfont = pygame.font.SysFont('Calibri', 22)
gameinfo.buttons.append(Button(500, 200, 300, 50, 80, 8, "Start Game", (255, 255, 255), "mainmenu", "startgame", defaultfont))
gameinfo.buttons.append(Button(500, 280, 300, 50, 100, 8, "Tutorial", (255, 255, 255), "mainmenu", None, defaultfont))
gameinfo.buttons.append(Button(500, 360, 300, 50, 105, 8, "Credits", (255, 255, 255), "mainmenu", "creditsclick", defaultfont))
gameinfo.buttons.append(Button(500, 440, 300, 50, 125, 8, "Exit", (255, 255, 255), "mainmenu", "exit", defaultfont))
gameinfo.buttons.append(Button(830, 120, 200, 50, 25, 8, "Warp Here", (255, 255, 255), "map", "warpclick", defaultfont))
gameinfo.buttons.append(Button(520, 520, 300, 50, 55, 8, "Back to Menu", (255, 255, 255), "credits", "creditsbackclick", defaultfont))
gameinfo.buttons.append(Button(50, 230, 200, 50, 55, 8, "Repair", (255, 255, 255), "stationmenu", "repairclick", defaultfont))
gameinfo.buttons.append(Button(400, 230, 200, 50, 39, 8, "Upgrade", (255, 255, 255), "stationmenu", "upgradeclick", defaultfont))
gameinfo.buttons.append(Button(1000, 640, 250, 50, 30, 8, "Back to Game", (255, 255, 255), "stationmenu", "stationbackclick", defaultfont))
gameinfo.buttons.append(Button(90, 230, 150, 50, 13, 8, "Upgrade", (255, 255, 255), "upgrademenu", "baseshipupgradeclick", defaultfont))
gameinfo.buttons.append(Button(1000, 640, 250, 50, 30, 8, "Back to Menu", (255, 255, 255), "upgrademenu", "upgradebackclick", defaultfont))
gameinfo.buttons.append(Button(660, 115, 150, 35, 35, 8, "Upgrade", (255, 255, 255), "upgrademenu", "upgradewarpenginesclick", smallfont))
gameinfo.buttons.append(Button(660, 155, 150, 35, 35, 8, "Upgrade", (255, 255, 255), "upgrademenu", "upgradecombatenginesclick", smallfont))
gameinfo.buttons.append(Button(660, 195, 150, 35, 35, 8, "Upgrade", (255, 255, 255), "upgrademenu", "upgradeshieldsclick", smallfont))

# Add messages

gameinfo.messages.append(Message(50, 290, "No Repair Needed", "stationmenu", pygame.font.SysFont('Calibri', 30)))

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
        if not fullscreen:
            screen = pygame.display.set_mode([width, height], pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode([width, height])
        fullscreen = not fullscreen
    keys = pygame.key.get_pressed()
    if not keys[pygame.K_RALT] and not keys[pygame.K_LALT]:
        alt_pressed = False
    if not keys[pygame.K_RETURN]:
        enter_pressed = False

    keypresses.detectKeyPresses(event_get, fullscreen, myship, enemyships, gameinfo, animations, sounds, spacestations, music)
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