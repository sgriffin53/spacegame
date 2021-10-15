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
    # spawn locations:
    # (480000, 220000)
    # (280000, 660000)
    # (280000, 1200000)
    # (480000, 1700000)
    # (1200000, 220000)
    # (1500000, 660000)
    # (1500000, 1200000)
    # (1200000, 1700000)

    stationIMG = pygame.image.load(os.path.join('images', 'station.png')).convert_alpha()
    i = 0
    spacestations.append(SpaceStation())
    spacestations[i].x = 480000
    spacestations[i].y = 220000
    spacestations[i].image = stationIMG
    spacestations[i].index = i
    spacestations[i].gridsector = functions.gridSector(spacestations[i])
    i = 1
    spacestations.append(SpaceStation())
    spacestations[i].x = 280000
    spacestations[i].y = 660000
    spacestations[i].image = stationIMG
    spacestations[i].index = i
    spacestations[i].gridsector = functions.gridSector(spacestations[i])
    i = 2
    spacestations.append(SpaceStation())
    spacestations[i].x = 280000
    spacestations[i].y = 1200000
    spacestations[i].image = stationIMG
    spacestations[i].index = i
    spacestations[i].gridsector = functions.gridSector(spacestations[i])
    i = 3
    spacestations.append(SpaceStation())
    spacestations[i].x = 480000
    spacestations[i].y = 1700000
    spacestations[i].image = stationIMG
    spacestations[i].index = i
    spacestations[i].gridsector = functions.gridSector(spacestations[i])
    i = 4
    spacestations.append(SpaceStation())
    spacestations[i].x = 1200000
    spacestations[i].y = 220000
    spacestations[i].image = stationIMG
    spacestations[i].index = i
    spacestations[i].gridsector = functions.gridSector(spacestations[i])
    i = 5
    spacestations.append(SpaceStation())
    spacestations[i].x = 1500000
    spacestations[i].y = 660000
    spacestations[i].image = stationIMG
    spacestations[i].index = i
    spacestations[i].gridsector = functions.gridSector(spacestations[i])
    i = 6
    spacestations.append(SpaceStation())
    spacestations[i].x = 1500000
    spacestations[i].y = 1200000
    spacestations[i].image = stationIMG
    spacestations[i].index = i
    spacestations[i].gridsector = functions.gridSector(spacestations[i])
    i = 7
    spacestations.append(SpaceStation())
    spacestations[i].x = 1200000
    spacestations[i].y = 1700000
    spacestations[i].image = stationIMG
    spacestations[i].index = i
    spacestations[i].gridsector = functions.gridSector(spacestations[i])