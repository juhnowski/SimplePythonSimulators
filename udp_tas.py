__author__ = '7634'

import socket
import sys
from math import sin,cos,sqrt,pi
from time import clock,sleep

# Create a socket (SOCK_STREAM means a TCP socket)
class ModelTas:
    """ Tas model
    """
    def __init__(self):
        self.n = 50.0
        self.t = 0.0
        self.x_max = 1280.0
        self.y_max = 1024.0
# model type
        self.m = 0
# parameters for elliptic model
        self.a = 600.0
        self.b = 400.0
        self.x_e = 640.0
        self.y_e = 512.0
        self.x_c = -self.a
        self.y_c = 0.0
# parameters of the simulation model capture target
        self.x_1 = 10.0
        self.y_1 = 300.0
        self.y_2 = 1000.0
# imitation's vars
        self.x = 0.0
        self.y = 0.0
        self.fi_1 = 0.0
        self.fi_2 = 0.0

    def data(self):
        self.t += 1/self.n
        if (self.m == 0):
            self.m0()
        else:
            self.m1()

        return 'tas;'+str(clock())+';' + \
                str(self.t) + ';' + \
                str(self.x) + ';' + \
                str(self.y) + ';' + \
                str(self.fi_1) + ';' + \
                str(self.fi_2)
# Model elliptical motion targets
    def m0(self):
        if (self.x_c < self.a):
            self.y_c = (self.b/self.a)*sqrt(self.a*self.a - self.x_c*self.x_c)
        else:
            self.y_c = -(self.b/self.a)*sqrt(self.a*self.a - self.x_c*self.x_c)
        self.x = self.x_e + self.x_c
        self.y = self.y_e + self.y_c
        self.t += 1/self.n
        self.x_c += 1.0
        return

# Capture target's simulation model
    def m1(self):
        if(self.t < self.y_2/self.n):
            self.x = self.x_1
            self.y = self.n*self.t
            self.fi_1 = pi*self.t/(4*self.n)
            self.fi_2 = 0
            return
        if (self.t < (self.y_2 - self.y_1)/self.n ):
            self.x = self.x_1
            self.y = self.y_2 - self.n*self.t
            self.fi_1 = pi*self.t/4 - pi*self.t/(8*self.n)
            self.fi_2 = 0
            return
        if (self.t <(self.x_max - self.x_1)/self.n):
            self.x = self.x_1 + self.n*self.t
            self.y = self.y_1
            self.fi_1 = pi*self.t/8
            self.fi_2 = pi*self.t/(360*self.n)
            return
        if (self.t == (self.x_max - self.x_1)/self.n):
            self.t = 0
            return

class ControllerTas:
    def __init__(self):
        self.HOST = "0.0.0.0"
        self.PORT = 9991
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print ("Tas connected with CVS")
        self.tas = ModelTas()

    def send(self):
            data = self.tas.data()
            print "Sent:     {}".format(data)
            self.sock.sendto(data + "\n",(self.HOST,self.PORT))
            sleep(0.02)

    def run(self):
        for i in range(0,1000):
            self.send()

ctrl = ControllerTas()
ctrl.run()