#!/usr/bin/env python
import serial
import time
import socket

HOST = ''
PORT = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "puerto creado"
s.bind((HOST, PORT))
s.listen(1)
print "escucho"
conn, addr = s.accept()
print "inicio while"
while True:
    rcv = "+    18Kg"
    print(rcv)
    time.sleep(1)
    conn.sendall(rcv)
    print(rcv)
conn.close()
