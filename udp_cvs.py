__author__ = '7634'

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0",9991))
while True:
    data, address = s.recvfrom(1024)
    print("Got data from %s" % str(data))
    #s.sendto(b"Ok",("localhost",9991))