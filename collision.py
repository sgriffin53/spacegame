import functions

def objectCollisionDetection(object1, object2):
    dist = functions.distance(object1, object2)
    if dist < object1.radius + object2.radius:
        return True
    return False

def collisionDetection(myship, enemyships, spacestations):
    allowedSectors = myship.allowedsectors
    for enemyship in enemyships:
        enemyshipsector = enemyship.gridsector
        if enemyshipsector not in allowedSectors:
            continue
        for spacestation in spacestations:
            spacestationsector = spacestation.gridsector
            if spacestationsector not in allowedSectors:
                continue
            if objectCollisionDetection(enemyship, spacestation):
                enemyship.vel = 0
                enemyship.accel = 0
                enemyship.substate = enemyship.state
                enemyship.state = "leavestation_rot"
                enemyship.x = enemyship.lastx
                enemyship.y = enemyship.lasty
                enemyship.startLeaveStation_rot()
    if not myship.warping:
        for spacestation in spacestations:
            spacestationsector = spacestation.gridsector
            if spacestationsector not in allowedSectors:
                continue
            if objectCollisionDetection(myship, spacestation):
                myship.vel = 0
                myship.accel = 0
                myship.x = myship.lastx
                myship.y = myship.lasty
