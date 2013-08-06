__author__ = 'chang-ning'

import socket
import re
import time
from serial_observer import UltrasonicData
import random


class robot:

    def __init__(self, ultrasonicData):

        self.host = "127.0.0.1"
        self.userName = "crazyguitar"
        self.password = "******"
        self.port = 4444
        self.oculusSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.oculusFileIO = None
        self.isChanging = False
        self.moveForwardTime = 0
        self.stop = False
        self.ultrasonicData = ultrasonicData
        self.ultrasonicData.registerObserver(self)

    def connectRobot(self):

        self.oculusSocket.connect((self.host, self.port))
        self.oculusFileIO = self.oculusSocket.makefile()
        print 'connect success'

    def loginRobot(self):

        self.waitForRobotReplySearch("<telnet> LOGIN")
        self.sendRobotString(self.userName + ":" + self.password)
        print 'login robot'

    def waitForRobotReplySearch(self, reply):

        msg = None
        while True:
            msg = (self.oculusFileIO.readline()).strip()
            print(msg)
            if re.search(reply, msg):
                break
        return msg

    def sendRobotString(self, msg):

        self.oculusSocket.sendall(msg + "\r\n")
        print("> " + msg)

    def enableRobotMove(self):

        self.sendRobotString("motionenabletoggle")
        self.waitForRobotReplySearch("motion enabled")

    def disableRobotMove(self):
        self.sendRobotString("motionenabletoggle")
        self.waitForRobotReplySearch("motion disabled")

    def turnRobotLeft(self, moveTime):
        self.sendRobotString("move left")
        time.sleep(moveTime)

    def turnRobotRight(self, moveTime):
        self.sendRobotString("move right")
        time.sleep(moveTime)

    def turnRobotForward(self, moveTime):
        self.sendRobotString("move forward")
        time.sleep(moveTime)

    def turnRobotBackward(self, moveTime):
        self.sendRobotString("move backward")
        time.sleep(moveTime)

    def stopRobot(self):
        self.sendRobotString("move stop")

    def update(self, currentAngle):

        if not self.isChanging:
            self.isChanging = True
            self.changeRobotDirection(currentAngle)

    def changeRobotDirection(self, currentServoAngle):

        if currentServoAngle < 90:
            self.turnRobotLeft(1)

        elif currentServoAngle > 90:
            self.turnRobotRight(1)

        else:
            self.turnRobotForward(2)
            leftOrRight = random.randint(0, 1)
            if leftOrRight == 0:
                self.turnRobotLeft(2)
            else:
                self.turnRobotRight(2)

        self.stopRobot()
        self.moveForwardTime = 0
        self.isChanging = False


def main():

    serialInputUltrasonicData = UltrasonicData()
    oculusRobot = robot(serialInputUltrasonicData)
    serialInputUltrasonicData.start()
    oculusRobot.connectRobot()
    oculusRobot.loginRobot()
    oculusRobot.enableRobotMove()
    while not oculusRobot.stop:

        try:
            if not oculusRobot.isChanging:
                oculusRobot.moveForwardTime = (oculusRobot.moveForwardTime + 1) % 5
                oculusRobot.turnRobotForward(2)
                oculusRobot.stopRobot()
                time.sleep(1)
                if oculusRobot.moveForwardTime == 0:
                    oculusRobot.changeRobotDirection(90)
        except KeyboardInterrupt:
            oculusRobot = True
            serialInputUltrasonicData.stop = True

    oculusRobot.stopRobot()
    oculusRobot.disableRobotMove()


if __name__ == '__main__':
    main()

