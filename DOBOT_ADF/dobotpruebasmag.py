import time
import socket

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

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = "localhost"
port = 8000
server.bind((server_ip, port))
server.listen(0)
print("Escuchando en server")
client_socket, client_address = server.accept()
print("CONEXIÓN ACEPTADA")

while True:
    request = client_socket.recv(1024)
    request = request.decode("utf-8")
    print(request)
    if request == "1":
        print("AQUI ESTOOOOOOOOOOOOOY")
        while True:
            dType.SetColorSensor(api, 0, 0, 1)
            dType.SetEMotor(api, 0, 1, -6000,  isQueued=1)

            dType.SetInfraredSensor(api,  1, 2, version=1)

            while True:
                infra = dType.GetInfraredSensor(api, 2)
                if infra == [1]:
                    dType.dSleep(400)
                    dType.SetEMotor(api, 0, 1, 0,  isQueued=1)
                    break
            

            dType.SetColorSensor(api, 0, 1, version=1)
            dType.SetPTPCmd(api, 1, 192, 74, 127, -4, isQueued=1)
            print("SOY EL DOBOT CHINGA TU MADRE")
            dType.SetPTPCmd(api, 1, 256, -21, 55, -4, isQueued=1)
            dType.SetPTPCmd(api, 1, 256, -21, 8, -4, isQueued=1)
            dType.SetEndEffectorSuctionCup(api, 1,  1, isQueued=1)
            dType.SetPTPCmd(api, 1, 256, -21, 55, -4, isQueued=1)
            dType.SetPTPCmd(api, 1, 185, 58, 61, -4, isQueued=1)
            dType.SetPTPCmd(api, 1, 185, 58, 24, -4, isQueued=1)
            dType.dSleep(2500)
            dType.SetColorSensor(api, 1 ,1, 1)
            dType.dSleep(5000)
            colorDetected = dType.GetColorSensor(api)
            print(colorDetected)
            dType.SetPTPCmd(api, 1, 185, 58, 61, -4, isQueued=1)

            dType.SetColorSensor(api, 0, 0, 1)



            def colorRed(cuenta, lastPos):
                print(cuenta)
                if cuenta > 0:
                    print(lastPos)
                    dType.SetPTPCmd(api, 1, lastPos, yRed, zAltoDejar, -4, isQueued=1)
                    dType.SetPTPCmd(api, 1, lastPos, yRed, zBajoDejar, -4, isQueued=1)
                    dType.SetEndEffectorSuctionCup(api, 1,  0, isQueued=1)
                    dType.SetPTPCmd(api, 1, lastPos, yRed, zAltoDejar, -4, isQueued=1)
                    dType.dSleep(2500)

                else:
                    dType.SetPTPCmd(api, 1, xPrimeroDejar, yRed, zAltoDejar, -4, isQueued=1)
                    dType.SetPTPCmd(api, 1, xPrimeroDejar, yRed, zBajoDejar, -4, isQueued=1)
                    dType.dSleep(2000)
                    dType.SetEndEffectorSuctionCup(api, 1,  0, isQueued=1)
                    dType.SetPTPCmd(api, 1, xPrimeroDejar, yRed, zAltoDejar, -4, isQueued=1)
                    dType.dSleep(2500)

            def colorBlue(cuenta, lastPos):
                print(cuenta)
                if cuenta > 0:
                    print(lastPos)
                    dType.SetPTPCmd(api, 1, lastPos, yBlue, zAltoDejar, -4, isQueued=1)
                    dType.SetPTPCmd(api, 1, lastPos, yBlue, zBajoDejar, -4, isQueued=1)
                    dType.SetEndEffectorSuctionCup(api, 1,  0, isQueued=1)
                    dType.SetPTPCmd(api, 1, lastPos, yBlue, zAltoDejar, -4, isQueued=1)
                    dType.dSleep(2500)

                else:
                    dType.SetPTPCmd(api, 1, xPrimeroDejar, yBlue, zAltoDejar, -4, isQueued=1)
                    dType.SetPTPCmd(api, 1, xPrimeroDejar, yBlue, zBajoDejar, -4, isQueued=1)
                    dType.dSleep(2000)
                    dType.SetEndEffectorSuctionCup(api, 1,  0, isQueued=1)
                    dType.SetPTPCmd(api, 1, xPrimeroDejar, yBlue, zAltoDejar, -4, isQueued=1)
                    dType.dSleep(2500)

            if colorDetected == [1,0,0]:
                if countRed > 0:
                    lastPosRed -= diffBtwBlocks
                    colorRed(1, lastPosRed)
                else:
                    colorRed(0, lastPosRed)
                countRed += 1
                break

            elif colorDetected == [0,0,1]:
                if countBlue > 0:
                    lastPosBlue -= diffBtwBlocks
                    colorBlue(1, lastPosBlue)
                else:
                    colorBlue(0, lastPosBlue)
                countBlue += 1
                break
