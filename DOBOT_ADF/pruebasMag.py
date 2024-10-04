from adf_api import eduRobot
import time

#DECLARAR MAGICIAN
homeX, homeY, homeZ = 250, 0, 50
magician = eduRobot(homeX, homeY, homeZ, "COM5")
magician.stopConveyor(1)
magician.configColorSensor(1, 1, 1)
time.sleep(2)
magician.configColorSensor(0, 1, 1)

magician.configInfraredSensor(1,2,1)
while True:
    magician.moveConveyor(1, 1, -6000)
    infra = magician.getInfraredSensorInfo(2)
    print(infra)
    if infra == 1:
        magician.delay(400)
        magician.moveConveyor(1, 1, 0)
        break