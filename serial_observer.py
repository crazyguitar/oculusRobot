__author__ = 'chang-ning'

import serial


class UltrasonicData:

    def __init__(self):

        self.serial = serial.Serial('/dev/ttyACM0', 9600, timeout=8)
        self.observerList = []
        self.stop = False
        self.obstacleDistance = 0
        self.servoCurrentAngle = 0

    def getUltrasonicDataFromSerialPort(self):

        self.serial.write('1')
        line = self.serial.readline()
        tmpList = line.split()
        print tmpList
        return tmpList

if __name__ == '__main__':
    measureDistObj = UltrasonicData()
    while True:
        dataList = measureDistObj.getUltrasonicDataFromSerialPort()
        print dataList