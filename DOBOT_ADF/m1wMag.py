from adf_api import robot, eduRobot
import time

#DECLARAR MAGICIAN
homeX, homeY, homeZ = 250, 0, 50
magician = eduRobot(homeX, homeY, homeZ, "COM5")
magician.clearAlarms()
magician.move(1, 192, 74, 127, -4)
time.sleep(5)

#DECLARAR M1
m1 = robot("192.168.1.6", 29999, 30003, 30004)
m1.connect_robot()
m1.enableRobot()
print("M1 ROBOT HABILITADO")

#----------- VARIABLES MAGICIAN --------------------
yRed = 289
yBlue = 253
yGreen = 213
yYellow = 179

xPrimeroDejar = 84
diffBtwBlocks = xPrimeroDejar - 36

zAltoDejar = 0
zBajoDejar = -55

countRed = 0
countGreen = 0
countBlue = 0
countYellow = 0

lastPosRed = xPrimeroDejar
lastPosBlue = xPrimeroDejar

#----------- VARIABLES M1 ----------------
zAbajoRecoger = 62
zArribaRecoger = 120 #210
agarrarPrimerCubo = [172, 33] #x,y
diffSegCube = 29
diffColorCube = 26
diffFinal = 0

def checkCubeWinfrared():
    magician.configColorSensor(0, 1, 1)
    magician.configInfraredSensor(1,2,1)
    while True:
        magician.moveConveyor(1, 1, -6000)
        infra = magician.getInfraredSensorInfo(2)
        if infra == 1:
            magician.delay(400)
            magician.stopConveyor(1)
            break

def colorRed(cuenta, lastPos):
    print(cuenta)
    if cuenta > 0:
        print(lastPos)
        magician.move(1, lastPos, yRed, zAltoDejar, -4)
        magician.move(1, lastPos, yRed, zBajoDejar, -4)
        magician.toggleSuction()
        magician.move(1, lastPos, yRed, zAltoDejar, -4)
        magician.delay(2500)
    else:
        magician.move(1, xPrimeroDejar, yRed, zAltoDejar, -4)
        magician.move(1, xPrimeroDejar, yRed, zBajoDejar, -4)
        magician.delay(2000)
        magician.toggleSuction()
        magician.move(1, xPrimeroDejar, yRed, zAltoDejar, -4)
        magician.delay(2500)

def colorBlue(cuenta, lastPos):
    print(cuenta)
    if cuenta > 0:
        print(lastPos)
        magician.move(1, lastPos, yBlue, zAltoDejar, -4)
        magician.move(1, lastPos, yBlue, zBajoDejar, -4)
        magician.toggleSuction()
        magician.move(1, lastPos, yBlue, zAltoDejar, -4)
        magician.delay(2500)
    else:
        magician.move(1, xPrimeroDejar, yBlue, zAltoDejar, -4)
        magician.move(1, xPrimeroDejar, yBlue, zBajoDejar, -4)
        magician.delay(2000)
        magician.toggleSuction()
        magician.move(1, xPrimeroDejar, yBlue, zAltoDejar, -4)
        magician.delay(2500)

def magicianFunction(countRed, countGreen, countBlue, countYellow, lastPosRed, lastPosBlue):
    checkCubeWinfrared()
    magician.move(1, 192, 74, 127, -4)
    magician.move(1,241, -7, 55, -4)
    magician.move(1, 241, -7, 8, -4)
    magician.toggleSuction()
    magician.move(1, 241, -7, 55, -4)
    magician.move(1, 160, 64, 50, -4)
    magician.move(1, 160, 64, 20, -4)
    magician.delay(2500)
    magician.configColorSensor(1,1,1)
    magician.delay(5000)
    colorDetected = magician.getColorSensorInfo()
    print(f'Color detectado: {colorDetected}')
    magician.move(1, 160, 64, 50, -4)
    magician.configColorSensor(0,0,1)

    if colorDetected == "red":
        if countRed > 0:
            lastPosRed -= diffBtwBlocks
            colorRed(1, lastPosRed)
        else:
            colorRed(0, lastPosRed)
        countRed += 1
    elif colorDetected == "blue":
        if countBlue > 0:
            lastPosBlue -= diffBtwBlocks
            colorBlue(1, lastPosBlue)
        else:
            colorBlue(0, lastPosBlue)
        countBlue += 1
            

def dejarEnBanda(countRed, countGreen, countBlue, countYellow, lastPosRed, lastPosBlue):
    m1.linearMove(194,184,150,309)
    m1.linearMove(334,173,178,309)
    m1.linearMove(334,173,122,309)
    m1.activateOutput(15, 0)
    time.sleep(0.1)
    m1.activateOutput(16, 1)
    time.sleep(5)
    m1.linearMove(334,173,178,309)
    m1.activateOutput(16, 0)
    m1.linearMove(194,184,150,309)
    time.sleep(2)
    m1.linearMove(194,184,150,309)
    magicianFunction(countRed, countGreen, countBlue, countYellow, lastPosRed, lastPosBlue)
    time.sleep(5)


m1.armOrientation(1) #1 right, 2 left
m1.linearMove(194,184,150,309)

for n in range(4):
    cuenta = agarrarPrimerCubo[1]
    print(n)
    if n <= 3:
        m1.linearMove(agarrarPrimerCubo[0] + diffFinal, agarrarPrimerCubo[1], zArribaRecoger, 309)
        m1.linearMove(agarrarPrimerCubo[0] + diffFinal, agarrarPrimerCubo[1], zAbajoRecoger, 309)
        time.sleep(2)
        m1.activateOutput(15, 1)
        m1.linearMove(agarrarPrimerCubo[0] + diffFinal, agarrarPrimerCubo[1], zArribaRecoger, 309)
        dejarEnBanda(countRed, countGreen, countBlue, countYellow, lastPosRed, lastPosBlue)
    for n in range(3):
        cuenta -= diffSegCube
        m1.linearMove(agarrarPrimerCubo[0] + diffFinal, cuenta, zArribaRecoger,309)
        m1.linearMove(agarrarPrimerCubo[0] + diffFinal, cuenta, zAbajoRecoger,309)
        time.sleep(2)
        m1.activateOutput(15, 1)
        m1.linearMove(agarrarPrimerCubo[0] + diffFinal, cuenta, zArribaRecoger,309)
        dejarEnBanda(countRed, countGreen, countBlue, countYellow, lastPosRed, lastPosBlue)
        time.sleep(2)

    diffFinal += diffColorCube

time.sleep(5)
m1.disableRobot()