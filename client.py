#practice file for joystick TCP laptop -> raspi
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname("192.168.254.67")
s.connect((host, 12345))

while True:
    msg = s.recv(32)
    print(msg.decode("utf-8"))




