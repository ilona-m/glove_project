### This file reads data from the glove and writes it to a new .csv file.
### Used for collecting gesture data.

import socket
import time

# Function for reading the data from glove and writing it to a new .csv file:

def socketReadLine(connection):
    line = ""
    character = ""
    while (character != "\n"):
        line = line + character
        character = connection.recv(1).decode()
    #change name of csv file for different gestures (REMEMBER: .csv)
    with open('testsets2/t10rock4.csv', 'a') as csvfile:
        csvfile.write(line);
    return line

# Connecting the board:

ip = "IP ADDRESS HERE" # Remember to change the ip address
port = 80

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((ip, port))

connection.send(b'1')

# Printing the sensor values to the terminal to check what kind of values are saved to the .csv file:

for i in range(50000):
    line = socketReadLine(connection)
    print(line)

connection.send(b'0')

connection.close()
