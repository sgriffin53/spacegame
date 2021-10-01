import math

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
