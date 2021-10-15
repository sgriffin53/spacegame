# Simple pygame program

# Import and initialize the pygame library
import copy
import pygame
import os
import math
import random
import time
import sys
import physics
import keypresses
import collision
import functions
import render
import AI
import station
import enemies
from station import SpaceStation
from myship import MyShip
from classes import Animation, Music, Sound, Weapon, GameInfo, Point, FrameInfo, Shield, Button
from enemies import EnemyShip
from datetime import datetime

pygame.init()

# create game info

gameinfo = GameInfo()

# draw stars

for i in range(0, 200):
    thisX = random.randint(200, 800)
    thisY = random.randint(30, 630)
    gameinfo.mapstars.append((thisX, thisY))


width = 1280
height = 720
gameinfo.width = width
gameinfo.height = height
gameinfo.clock = pygame.time.Clock()
# Set up the drawing window
screen = pygame.display.set_mode([width, height])

spacestationIMG = pygame.image.load(os.path.join('images', 'station.png')).convert_alpha()
shipIMG = pygame.image.load(os.path.join('images','ship.png')).convert_alpha()
enemyshipIMG = pygame.image.load(os.path.join('images', 'enemyship.png')).convert_alpha()

fullscreen = False
stars = []
for i in range(250):
  stars.append(dict({'x': 0, 'y': 0}))
  stars[i]['x'] = random.random()*width
  stars[i]['y'] = random.random()*height

animations = []
music = []
sounds = []

path = 'music'

files = os.listdir(path)

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

myship.shields.append(copy.deepcopy(Shield()))
myship.shields.append(copy.deepcopy(Shield()))
myship.shields.append(copy.deepcopy(Shield()))
myship.shields.append(copy.deepcopy(Shield()))
for shield in myship.shields:
    shield.charge = 250
    shield.maxcharge = 250

myship.respawn(spacestations[7])

# spawn enemies

enemyships = []

enemies.spawnEnemyShips(enemyships, spacestations)
'''
for i in range(200):
    enemyships.append(EnemyShip())
    enemyships[i].weapons.append(Weapon())
    enemyships[i].weapons[0].type = "torpedo"
    enemyships[i].weapons[0].duration = 0.5
    enemyships[i].weapons[0].chargetime = 3
    enemyships[i].weapons[0].lastfired = 0
    enemyships[i].weapons[0].range = 600
    enemyships[i].weapons.append(Weapon())
    enemyships[i].weapons[1].type = "laser"
    enemyships[i].weapons[1].duration = 0.2
    enemyships[i].weapons[1].chargetime = 1
    enemyships[i].weapons[1].lastfired = 0
    enemyships[i].weapons[1].range = 600
    #enemyships[i].x = 200
    #enemyships[i].y = 200
    enemyships[i].x = random.randint(-10000, 10000)
    enemyships[i].y = random.randint(-10000, 10000)
    enemyships[i].index = i
    enemyships[i].state = "patrol"
    enemyships[i].startPatrol()
    enemyships[i].shipIMG = pygame.image.load(os.path.join('images', 'enemyship.png')).convert_alpha()
'''
#enemyship = EnemyShip()

frameinfo = FrameInfo()
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

startButton = Button()
startButton.x = 500
startButton.y = 200
startButton.width = 300
startButton.height = 50
startButton.textx = 80
startButton.texty = 8
startButton.textcol = (255, 255, 255)
startButton.text = "Start Game"
startButton.screen = "mainmenu"
startButton.onclick = "startgame"
startButton.render(screen, gameinfo)
gameinfo.buttons.append(startButton)

tutorialButton = Button()
tutorialButton.x = 500
tutorialButton.y = 280
tutorialButton.width = 300
tutorialButton.height = 50
tutorialButton.textx = 100
tutorialButton.texty = 8
tutorialButton.textcol = (255, 255, 255)
tutorialButton.text = "Tutorial"
tutorialButton.screen = "mainmenu"
tutorialButton.onclick = None
tutorialButton.render(screen, gameinfo)
gameinfo.buttons.append(tutorialButton)

creditsButton = Button()
creditsButton.x = 500
creditsButton.y = 360
creditsButton.width = 300
creditsButton.height = 50
creditsButton.textx = 105
creditsButton.texty = 8
creditsButton.textcol = (255, 255, 255)
creditsButton.text = "Credits"
creditsButton.screen = "mainmenu"
creditsButton.onclick = "creditsclick"
creditsButton.render(screen, gameinfo)
gameinfo.buttons.append(creditsButton)

exitButton = Button()
exitButton.x = 500
exitButton.y = 440
exitButton.width = 300
exitButton.height = 50
exitButton.textx = 125
exitButton.texty = 8
exitButton.textcol = (255, 255, 255)
exitButton.text = "Exit"
exitButton.screen = "mainmenu"
exitButton.onclick = "exit"
exitButton.render(screen, gameinfo)
gameinfo.buttons.append(exitButton)

warpButton = Button()
warpButton.x = 830
warpButton.y = 120
warpButton.width = 200
warpButton.height = 50
warpButton.textx = 25
warpButton.texty = 8
warpButton.textcol = (255, 255, 255)
warpButton.text = "Warp Here"
warpButton.screen = "map"
warpButton.onclick = "warpclick"
warpButton.render(screen, gameinfo)
gameinfo.buttons.append(warpButton)

creditsbackButton = Button()
creditsbackButton.x = 520
creditsbackButton.y = 520
creditsbackButton.width = 300
creditsbackButton.height = 50
creditsbackButton.textx = 55
creditsbackButton.texty = 8
creditsbackButton.textcol = (255, 255, 255)
creditsbackButton.text = "Back to Menu"
creditsbackButton.screen = "credits"
creditsbackButton.onclick = "creditsbackclick"
creditsbackButton.render(screen, gameinfo)
gameinfo.buttons.append(creditsbackButton)

repairButton = Button()
repairButton.x = 90
repairButton.y = 180
repairButton.width = 200
repairButton.height = 50
repairButton.textx = 55
repairButton.texty = 8
repairButton.textcol = (255, 255, 255)
repairButton.text = "Repair"
repairButton.screen = "stationmenu"
repairButton.onclick = "repairclick"
repairButton.render(screen, gameinfo)
gameinfo.buttons.append(repairButton)

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
    physics.physicsTick(myship, enemyships, spacestations, time_since_phys_tick, gameinfo)
    last_phys_tick = cur_time
    collision.collisionDetection(myship, enemyships, spacestations)
    for enemyship in enemyships:
        AI.enemyAITick(myship,enemyship, spacestations, animations, sounds, gameinfo)
    myship.autoTick(gameinfo, spacestations)
    render.renderFrame(screen, stars, myship, enemyships, spacestations, frameinfo, images, shipIMG, enemyshipIMG, spacestationIMG, gameinfo, animations)
    gameinfo.clock.tick(165000)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()