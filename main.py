# Simple pygame program

# Import and initialize the pygame library
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
from myship import MyShip
from classes import Animation, Music, Sound, Weapon, GameInfo, Point, FrameInfo
from enemies import EnemyShip
from datetime import datetime

pygame.init()

class SpaceStation():
    def __init__(self):
        self.objtype = "spacestation"
        self.x = -1000
        self.y = -1000
        self.rotation = 0
        self.width = 922
        self.type = "Space Station"
        self.radius = 922 / 2


def drawHealthBar(enemyship):
    percentage = enemyship.hull * 100 / enemyship.maxhull

# create game info

gameinfo = GameInfo()

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


music_track = random.randint(0,len(music) - 1)
music_playing = music[music_track]
pygame.mixer.music.load(music_playing.file)
pygame.mixer.music.play(-100000)


# create space station object

spacestation = SpaceStation()

# create my ship object

myship = MyShip()
myship.weapons.append(Weapon())
myship.weapons[0].type = "laser"
myship.weapons[0].duration = 0.02
myship.weapons[0].chargetime = 0.5
myship.weapons[0].lastfired = 0
myship.weapons[0].range = 600
myship.respawn(spacestation)

# spawn enemies

enemyships = []
for i in range(200):
    enemyships.append(EnemyShip())
    enemyships[i].weapons.append(Weapon())
    enemyships[i].weapons[0].type = "laser"
    enemyships[i].weapons[0].duration = 0.02
    enemyships[i].weapons[0].chargetime = 1.0
    enemyships[i].weapons[0].lastfired = 0
    enemyships[i].weapons[0].range = 600
    #enemyships[i].x = 200
    #enemyships[i].y = 200
    enemyships[i].x = random.randint(-10000, 10000)
    enemyships[i].y = random.randint(-10000, 10000)
    enemyships[i].index = i
    enemyships[i].state = "patrol"
    enemyships[i].startPatrol()
    enemyships[i].patroldist = 20
    '''
    r = random.randint(1, 2)
    if r == 1:
        enemyships[i].x = spacestation.x + 1000 + random.randint(-3000, 3000)
        enemyships[i].y = spacestation.y + 1000 + random.randint(-3000, 3000)
    else:
        enemyships[i].x = -spacestation.x - 1000 + random.randint(-3000, 3000)
        enemyships[i].y = spacestation.y - 1000 + random.randint(-3000, 3000)
    '''
    enemyships[i].shipIMG = pygame.image.load(os.path.join('images', 'enemyship.png')).convert_alpha()

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

# main game loop

while running:
    i+= 1
    if not gameinfo.alive:
        time_since_died = time.time() - gameinfo.lastdied
        if time_since_died >= 5:
            gameinfo.alive = True
            myship.alive = True
            myship.respawn(spacestation)
    time_since_key_poll = time.time() - last_keys_poll
    keypresses.detectKeyPresses(pygame.event.get(), fullscreen, alt_pressed, enter_pressed, myship, enemyships, gameinfo, animations, sounds)
    cur_time = time.time()
    time_since_phys_tick = cur_time - last_phys_tick
    physics.physicsTick(myship, enemyships, spacestation, time_since_phys_tick, gameinfo)
    last_phys_tick = cur_time
    collision.collisionDetection(myship, enemyships, spacestation)
    for enemyship in enemyships:
        AI.enemyAITick(myship,enemyship, spacestation, animations, sounds, gameinfo)

    render.renderFrame(screen, stars, myship, enemyships, spacestation, frameinfo, shipIMG, enemyshipIMG, spacestationIMG, gameinfo, animations)
    dy = myship.y - spacestation.y
    dx = myship.x - spacestation.x
    angle_deg = 360 - math.atan2(dy, dx) * 180 / math.pi - 90
    gameinfo.clock.tick(165)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()