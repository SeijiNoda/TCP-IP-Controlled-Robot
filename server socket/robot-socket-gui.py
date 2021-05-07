# Robot Controller Client with socket-connection - made in May 2021 for TI502
# Matheus Seiji Luna Noda - 19190

# All imports 
from PySimpleGUI import PySimpleGUI as gui
import struct, socket, sys, _thread

# Function that returns the port used for the socket
def get_port():
    return 9001
    
# Function that returns the IP address looked for
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255',1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    return IP

# Sets the GUI's theme
gui.theme('Reddit')

# Sets the GUI's layout (a TextField and two Buttons)
layout = [
    [gui.Text(size=(40,1), key='-OUTPUT-')],
    [gui.Button('Start'), gui.Button('Stop')]
]

# Creates the GUI's window
window = gui.Window('Webots Controller', layout)

# Event loop
while True:
    # Gets the events and the values that accours on the window
    event, values = window.read()
    # If the button 'Start' is pressed
    if event == 'Start':
        try:
            # Sets the message to 'start'
            msg = 'start'
            
            # Sets the socket and connects with the server
            socket.setdefaulttimeout(0.5)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            sock.connect((get_ip(), get_port()))

            # Sends the encoded message
            sock.sendall(msg.encode())
        finally:
            # Closes the socket
            sock.close()

        # Updates the TextField
        window['-OUTPUT-'].update('Enviou mensagem \'start\'')
    # If the button 'Stop' is pressed
    elif event == 'Stop':
        try:
            # Sets the message to 'stop'
            msg = 'stop'

            # Sets the socket and connects with ther server
            socket.setdefaulttimeout(0.5)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            sock.connect((get_ip(), get_port()))
            
            # Sends the encoded message
            sock.sendall(msg.encode())
        finally:
            # Closes the socket
            sock.close()

        # Updates the TextField
        window['-OUTPUT-'].update('Saindo do socket')
    # If the window-close button is pressed, ends the Event Loop
    elif event == gui.WINDOW_CLOSED:
        break

# Closes the window
window.close()