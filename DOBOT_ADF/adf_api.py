from dobot_api import DobotApiDashboard, DobotApi, DobotApiMove
import magician_api.DobotDllType as dType

class robot():

    def __init__(self, ip: str, dashboardPort: int, movePort: int, feedPort: int):
        self.ip = ip
        self.dashboardPort = dashboardPort
        self.movePort = movePort
        self.feedPort = feedPort
        self.userparam="User=1"
        self.LorR = 1

    def connect_robot(self):
        try:
            print("CONECTANDO...")
            print(self.ip, self.dashboardPort, self.movePort, self.feedPort)
            self.dashboard = DobotApiDashboard(self.ip, self.dashboardPort)
            self.move = DobotApiMove(self.ip, self.movePort)
            self.feed = DobotApi(self.ip, self.feedPort)
            print("( ͡• ͜ʖ ͡•) CONEXIÓN ESTABLECIDA EXITOSAMENTE ( ͡• ‿‿ ͡•)")
            return self.dashboard, self.move, self.feed
        except Exception as e:
            print("LA CONEXIÓN FALLÓ ( ͡ಠ ‿‿ ͡ಠ)")

    def enableRobot(self):
        self.dashboard.EnableRobot()

    def disableRobot(self):
        self.dashboard.DisableRobot()

    def linearMove(self, x,y,z,r):
       self.move.MovL(x,y,z,r,self.userparam)

    def armOrientation(self, dir: int):
        self.dashboard.SetArmOrientation(dir)

    def getPosition(self):
        self.dashboard.GetPose()

    def activateOutput(self, index: int, status: int):
        self.dashboard.DO(index,status)
    
    def waitSecs(self, sec):
        self.dashboard.wait(sec)

CON_STR = {
            dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
            dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
            dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

class eduRobot():

    def __init__(self, homeX, homeY, homeZ, com):
        self.suction = False
        self.picking = False
        self.api = dType.load()
        self.homeX = homeX
        self.homeY = homeY
        self.homeZ = homeZ
        self.connected = False
        self.connect_robot()
        self.COM = com

    def __del__(self):
        self.dobotDisconnect()

    def connect_robot(self):
        if(self.connected):
            print("You're already connected")
        else:
            state = dType.ConnectDobot(self.api, "COM5", 115200)[0]
            if(state == dType.DobotConnect.DobotConnect_NoError):
                print("Connect status:",CON_STR[state])
                dType.SetQueuedCmdClear(self.api)

                dType.SetHOMEParams(self.api, self.homeX, self.homeY, self.homeZ, 0, isQueued = 1)
                dType.SetPTPJointParams(self.api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
                dType.SetPTPCommonParams(self.api, 100, 100, isQueued = 1)

                dType.SetHOMECmd(self.api, temp = 0, isQueued = 1)
                self.connected = True
                return self.connected
            else:
                print("Unable to connect")
                print("Connect status:",CON_STR[state])
                return self.connected
            
    def dobotDisconnect(self):
        self.moveHome()
        dType.DisconnectDobot(self.api)

    def commandDelay(self, lastIndex):
        dType.SetQueuedCmdStartExec(self.api)
        while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
            dType.dSleep(200)
        dType.SetQueuedCmdStopExec(self.api)

    def toggleSuction(self):
        lastIndex = 0
        if(self.suction):
            lastIndex = dType.SetEndEffectorSuctionCup( self.api, True, False, isQueued = 0)[0]
            self.suction = False
        else:
            lastIndex = dType.SetEndEffectorSuctionCup(self.api, True, True, isQueued = 0)[0]
            self.suction = True
        self.commandDelay(lastIndex)

    def move(self, PTPMode:int, x:float, y:float, z:float, r:float):
        if PTPMode == 1:
            lastIndex = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVJXYZMode, x, y, z, r, isQueued = 1)[0]
            self.commandDelay(lastIndex)
        elif PTPMode == 2:
            self.lastIndex = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, x, y, z, r, isQueued = 1)[0]
            self.commandDelay(lastIndex)

    def moveHome(self):
        lastIndex = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, self.homeX, self.homeY, self.homeZ, 0)[0]
        self.commandDelay(lastIndex)

    def configColorSensor(self, isEnable, colorPort, version = 0):
        dType.SetColorSensor(self.api, isEnable, colorPort, version)

    def getColorSensorInfo(self):

        if dType.GetColorSensor(self.api) == [1,0,0]:
            return "red"
        elif dType.GetColorSensor(self.api) == [0,1,0]:
            return "green"
        elif dType.GetColorSensor(self.api) == [0,0,1]:
            return "blue"
        else:
            return "other"
        
    def configInfraredSensor(self, isEnable, infraredPort, version=0):
        dType.SetInfraredSensor(self.api, isEnable, infraredPort, version)

    def getInfraredSensorInfo(self, infraredPort):
        lastIndex = dType.GetInfraredSensor(self.api, infraredPort)[0]
        self.commandDelay(lastIndex)
        return lastIndex

    def moveConveyor(self, stepper, isEnabled, speed):
        lastIndex = dType.SetEMotor(self.api, stepper-1, isEnabled, speed, isQueued=1)[0]
        self.commandDelay(lastIndex)

    def moveConveyorByDistance(self, stepper, isEnabled, speed, distance):
        lastIndex = dType.SetEMotorSEx(self.api, stepper-1,isEnabled,speed,distance, isQueued=1)[0]
        self.commandDelay(lastIndex)

    def stopConveyor(self, stepper):
        lastIndex = dType.SetEMotor(self.api, stepper-1, 0, 0,  isQueued = 1)[0]
        self.commandDelay(lastIndex)
    
    def delay(self, ms):
        lastIndex = dType.SetWAITCmd(self.api, 400, isQueued=1)[0]
        self.commandDelay(lastIndex)

    def clearAlarms(self):
        dType.ClearAllAlarmsState(self.api)