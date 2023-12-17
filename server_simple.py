### This file prints the sensor values to the terminal in real time.
### Used for checking sensor values.

import socket
import time

# Function for reading the data from glove:

def socketReadLine(connection):
    line = ""
    character = ""
    while (character != "\n"):
        line = line + character
        character = connection.recv(1).decode()
    print(line)
    return line

# Connecting the board:

ip = "IP ADDRESS HERE" # Remember to change the ip address
port = 80

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((ip, port))

connection.send(b'1')

# Printing the sensor values to the terminal:

for i in range(10000):
    line = socketReadLine(connection)
    print(line)

connection.send(b'0')

connection.close()
