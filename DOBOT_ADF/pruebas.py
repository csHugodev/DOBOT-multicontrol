from adf_api import robot
import time
import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = "localhost"
server_port = 2424
client.connect((server_ip, server_port))

zAbajoRecoger = 62
zArribaRecoger = 120 #210
agarrarPrimerCubo = [172, 33] #x,y
diffSegCube = 29
diffColorCube = 26
diffFinal = 0

m1 = robot("192.168.1.6", 29999, 30003, 30004)

m1.connect_robot()
m1.enableRobot()
print("ROBOT HABILITADO")
time.sleep(3)
#print(m1.getPosition())

def dejarEnBanda():
    m1.linearMove(194,184,150,309)
    m1.linearMove(334,173,178,309)
    m1.linearMove(334,173,122,309)
    time.sleep(2)
    m1.activateOutput(15, 0)
    time.sleep(2)
    m1.activateOutput(16, 1)
    time.sleep(2)
    time.sleep(1)
    m1.linearMove(334,173,178,309)
    m1.linearMove(194,184,150,309)
    m1.activateOutput(16, 0)
    msg = "1"
    client.send(msg.encode("utf-8")[:1024])
    time.sleep(20)

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
        dejarEnBanda()
    for n in range(3):
        cuenta -= diffSegCube
        m1.linearMove(agarrarPrimerCubo[0] + diffFinal, cuenta, zArribaRecoger,309)
        m1.linearMove(agarrarPrimerCubo[0] + diffFinal, cuenta, zAbajoRecoger,309)
        time.sleep(2)
        m1.activateOutput(15, 1)
        m1.linearMove(agarrarPrimerCubo[0] + diffFinal, cuenta, zArribaRecoger,309)
        dejarEnBanda()
        time.sleep(2)

    diffFinal += diffColorCube

time.sleep(5)
m1.disableRobot()