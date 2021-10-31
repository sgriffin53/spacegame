import pygame
import os
import functions

class SpaceStation():
    def __init__(self):
        self.objtype = "spacestation"
        self.x = -1000
        self.y = -1000
        self.rotation = 0
        self.width = 922
        self.type = "Space Station"
        self.radius = 922 / 2
        self.image = None
        self.index = -1
        self.gridsector = 0

def spawnSpaceStations(spacestations):
    station_coords = [ # spawn locations
        (480000, 220000),
        (280000, 660000),
        (280000, 1200000),
        (480000, 1700000),
        (1200000, 220000),
        (1500000, 660000),
        (1500000, 1200000),
        (1200000, 1700000),
    ]
    stationIMG = pygame.image.load(os.path.join('images', 'station.png')).convert_alpha()
    for i in range(8):
        spacestations.append(SpaceStation())
        spacestations[i].x = station_coords[i][0]
        spacestations[i].y = station_coords[i][1]
        spacestations[i].image = stationIMG
        spacestations[i].index = i
        spacestations[i].gridsector = functions.gridSector(spacestations[i])