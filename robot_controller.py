__author__ = 'chang-ning'

import socket
import re
import time
from serial_observer import UltrasonicData
import random
import subprocess
import shlex

Threshold = 45


class robot:

    def __init__(self, ultrasonicData):

        self.host = "127.0.0.1"
        self.userName = "crazyguitar"
        self.password = "96201006"
        self.port = 4444
        self.oculusSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.oculusFileIO = None
        self.isChanging = False
        self.moveForwardTime = 0
        self.stop = False
        self.ultrasonicData = ultrasonicData

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

    def waitForRobotCollectionData(self, dataIndex):

        shell_command = 'sudo ~/linux-80211n-csitool-supplementary/netlink/log_to_file ' \
                        'tmp/log%d.dat tmp/ap_log%d.dat' % (dataIndex, dataIndex)
        args = shlex.split(shell_command)
        subprocess.call(args)

    def changeRobotDirection(self, Angle):

        if Angle < 90:
            self.turnRobotBackward(0.5)
            self.turnRobotRight(1.5)

        elif Angle > 90:
            self.turnRobotBackward(0.5)
            self.turnRobotLeft(1.5)

        else:
            self.turnRobotBackward(1)
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
    oculusRobot.connectRobot()
    oculusRobot.loginRobot()
    oculusRobot.enableRobotMove()
    angleList = [30, 50, 70, 90, 110, 130, 150]
    dataIndex = 1

    while not oculusRobot.stop:

        try:
            ultrasonicDataList = oculusRobot.ultrasonicData.getUltrasonicDataFromSerialPort()
            if len(ultrasonicDataList) == 7:

                # whether angle 90's dist is larger than threshold
                if float(ultrasonicDataList[3]) > Threshold:
                    oculusRobot.turnRobotForward(3)
                    oculusRobot.stopRobot()

                    # collection data
                    oculusRobot.waitForRobotCollectionData(dataIndex)
                    dataIndex += 1

                    # whether robot move forward every 8 times
                    oculusRobot.moveForwardTime = (oculusRobot.moveForwardTime + 1) % 8
                    if oculusRobot.moveForwardTime == 0:
                        oculusRobot.changeRobotDirection(90)

                else:
                    # change ultrasonicDataList data type to float
                    ultrasonicDataList = [float(item) for item in ultrasonicDataList]

                    if all(item < Threshold for item in ultrasonicDataList):
                        oculusRobot.changeRobotDirection(90)
                    else:
                        val, idx = max((val, idx) for (idx, val) in enumerate(ultrasonicDataList))
                        angle = angleList[idx]
                        oculusRobot.changeRobotDirection(angle)

        except KeyboardInterrupt:
            oculusRobot.stop = True

    oculusRobot.stopRobot()
    oculusRobot.disableRobotMove()


if __name__ == '__main__':
    main()