__author__ = 'chang-ning'

import serial
import threading

Threshold = 45


class UltrasonicData(threading.Thread):

    def __init__(self):

        threading.Thread.__init__(self)
        self.serial = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.observerList = []
        self.stop = False
        self.obstacleDistance = 0
        self.servoCurrentAngle = 0

    def registerObserver(self, observer):
        self.observerList.append(observer)

    def removeObserver(self, observer):
        self.observerList.remove(observer)

    def notifyObserver(self):

        for observer in self.observerList:
            observer.update(self.servoCurrentAngle)

    def isSmallerThanThreshold(self):

        if self.obstacleDistance < Threshold:
            self.notifyObserver()

    def run(self):

        while not self.stop:

            msgLine = self.serial.readline()
            tmpList = msgLine.split()
            print tmpList
            if len(tmpList) == 4:
                self.obstacleDistance = float(tmpList[1])
                self.servoCurrentAngle = float(tmpList[3])
                self.isSmallerThanThreshold()


if __name__ == '__main__':
    measureDistObj = UltrasonicData()
    measureDistObj.run()