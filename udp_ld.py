__author__ = '7634'

import socket
import sys
from math import sin,cos,sqrt
from time import clock,sleep

# Create a socket (SOCK_STREAM means a TCP socket)
class ModelLd:
    """ Ktn model
    """
    def __init__(self):
        self.n = 100.0
        self.y_min = -3000.0
        self.y_max = 3000.0
        self.r = 0.0
        self.y = 0.0
        self.v = 400.0
        self.z = 1000.0
        self.t = 0.0

    def data(self):
        self.t += 1/self.n
        self.y = self.y_max - self.v*self.t
        if (self.y <= self.y_min):
            self.y = self.y_max
        self.r = sqrt(self.z*self.z + self.y*self.y)
        return 'ld;'+str(clock())+';' + \
                str(self.t) + ';' + \
                str(self.r)

class ControllerLd:
    def __init__(self):
        self.HOST = "0.0.0.0"
        self.PORT = 9991
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print ("Ld connected with CVS")
        self.ld = ModelLd()

    def send(self):
            data = self.ld.data()
            print "Sent:     {}".format(data)
            self.sock.sendto(data + "\n",(self.HOST,self.PORT))
            sleep(0.01)

    def run(self):
        for i in range(0,1000):
            self.send()

ctrl = ControllerLd()
ctrl.run()