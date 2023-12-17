### This is the file where the final product is run from. It loads the ML model, makes predictions,
### and creates an UI window to control the data reading and display the gestures.

import socket
import time
import pickle
import numpy as np
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import threading
import os

# Resetting the objects:

model = None
current_gesture_label = None
connection = None

# Dictionary with the class names (gestures):

name_of_class = {0: 'Open hand', 1: 'Rock sign', 2: 'Two fingers up', 3: 'Tiger paw', 4: 'Four fingers up', 5: 'Fist', 6: 'Three fingers up', 7: 'Stop sign', 8: 'Index finger up', 9: 'Call sign'}

# Loading the ML model:

def loadModel():
    global model
    with open('model', 'rb') as file:
        model = pickle.load(file)[0]

# Creating an input numpy array:

def createInputData(arr):
    ans = [float(k) for k in arr.split(',')]
    new_data = np.array([ans])
    return new_data

# Predicting a gesture from an array:

def predictFromOneArray(norm_arr):
    prediction = model.predict(norm_arr)
    return prediction

# Reading data from the glove:

def socketReadLine(connection):
    line = ""
    character = ""
    while (character != "\n"):
        line = line + character
        character = connection.recv(1).decode()
    print(line)
    return name_of_class[predictFromOneArray(createInputData(line))[0]]

# Defining when the data reading starts by connecting the socket and creating a thread to read the socket:

def start_reading(instance):
    global connection
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(('IP ADDRESS HERE', 80)) # Remember to change the ip address
    connection.send(b'1')
    threading.Thread(target=socket_reading_thread).start()

# Reading data from the socket and updating the prediction/gesture:

def socket_reading_thread():
    global current_gesture_label
    while True:
        if connection:
            current_gesture = socketReadLine(connection)
            Clock.schedule_once(lambda dt: update_gesture(current_gesture))

# Changing the gesture label:

def update_gesture(current_gesture):
    global current_gesture_label
    current_gesture_label.text = current_gesture

# Defining when the data reading stops:

def stop_reading(instance):
    if connection:
        connection.send(b'0')
        connection.close()

# Building the UI window and assigning the starting, stopping and gesture printing to the buttons:

class GestureApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        start_button = Button(text="Start")
        start_button.bind(on_press=start_reading)
        layout.add_widget(start_button)

        stop_button = Button(text="Stop")
        stop_button.bind(on_press=stop_reading)
        layout.add_widget(stop_button)

        global current_gesture_label
        current_gesture_label = Label(text="No gesture", font_size='20sp')
        layout.add_widget(current_gesture_label)

        return layout

if __name__ == '__main__':
    app = GestureApp()
    loadModel()
    app.run()

if connection:
    connection.send(b'0')
    connection.close()