__author__ = '7634'

import socket
import sys
from math import sin,cos
from time import clock,sleep

# Create a socket (SOCK_STREAM means a TCP socket)
class ModelKtn:
    """ Ktn model
    """
    def __init__(self):
        self.n = 10.0
        self.v = 2.77
        self.w = 1.0
        self.omega = 1.0
        self.t = 0.0

    def data(self):
        self.t += 1/self.n
        self.x = 0.0
        self.y = self.v*self.t
        self.z = sin(self.w*self.t) + 1.0
        self.V_x = 0.0
        self.V_y = self.v
        self.V_z = self.w * cos(self.w * self.t)
        self.fi_z = self.omega * self.t
        self.fi_x = 0.0
        self.fi_y = 0.0
        self.w_x = 0.0
        self.w_y = 0.0
        self.w_z = 0.0
        return 'ktn;'+str(clock())+';' + \
                str(self.t) + ';' + \
                str(self.x) + ';' + \
                str(self.y) + ';' + \
                str(self.z) + ';' + \
                str(self.V_x) + ';' + \
                str(self.V_y) + ';' + \
                str(self.V_z) + ';' + \
                str(self.fi_z) + ';' + \
                str(self.fi_x) + ';' + \
                str(self.fi_y) + ';' + \
                str(self.w_x) + ';' + \
                str(self.w_y) + ';' + \
                str(self.w_z)

class ControllerKtn:
    def __init__(self):
        self.HOST = "0.0.0.0"
        self.PORT = 9991
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print ("KTN connected with CVS")
        self.ktn = ModelKtn()

    def send(self):
            data = self.ktn.data()
            print ("Sent:     {}".format(data))
            self.sock.sendto(data + "\n",(self.HOST,self.PORT))
            sleep(0.1)

    def run(self):
        for i in range(0,1000):
            self.send()

ctrl = ControllerKtn()
ctrl.run()