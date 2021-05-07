# Robot Controller with socket-connection - made in May 2021 for TI502
# Matheus Seiji Luna Noda - 19190

# All imports
from controller import Robot, DifferentialWheels 
import struct, socket, sys, _thread

# Set robot timestep
timestep = 64

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

# On new socket connection (new client)
def on_new_client(socket, addr):
    # Gets this robot's controller
    global robot_controller
    # Message loop 
    while True:
        # Receives the message
        msg = socket.recv(1024)  
        # If the message is to start, calls pararRobo(False)
        if msg.decode() == 'start':
            robot_controller.pararRobo(False)
        # If the message is to stop, calls paraRobo(True)
        elif msg.decode() == 'stop': 
            robot_controller.pararRobo(True)
        # Else, exits the Message loop
        else:
            break
    # Close the socket connection
    socket.close()
    return

# Creates the socket server structure
def servidor(https, hport):
    # Gets the socket and sets it accordingly
    sockHttp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sockHttp.bind((https, hport))
    except:
        sockHttp.bind((''.hport))
    
    # After setting up the socket, listens
    sockHttp.listen(1)
    
    # Starts the server's thread
    while True:
        client, addr = sockHttp.accept()
        _thread.start_new_thread(on_new_client, (client, addr))

# Primary robot class
class sockRobot:
    def __init__(self, robot):
        # All of the robots settings and data
        self.robot = robot
        self.name = self.robot.getName()
        self.robot.setSpeed(0,0)
        self.parado = False
        self.sentido = 0
        
        # Setting touch sensors
        self.ts1 = self.robot.getDevice("ts1")
        self.ts2 = self.robot.getDevice("ts2")
        self.ts1.enable(timestep)           
        self.ts2.enable(timestep)           
         
    def run(self):
        raise NotImplementedError

# This robot's class
class rfa1(sockRobot):
    def run(self):
        # Direction control variable
        sentido = 0 
        
        # Instruction loop
        while robot.step(timestep) != -1:
            # (Negative) Verifies touch sensor no.1
            if self.ts1.getValue() == 1:
                sentido = 0
            # (Positive) Verifies touch sensor no.2
            elif self.ts2.getValue() == 1:
                sentido = 1
                              
            # Sets the speed according to the "sentido" variable 
            if sentido == 0:
               self.robot.setSpeed(-4,-4)
            else:
                self.robot.setSpeed(4,4)
            
            # If the socket determines that the robot must stop, this if will always set the speed to zero
            if self.parado:
                self.robot.setSpeed(0,0)
           
    # Function that stops/starts the robot based on the "estado" (boolean) paramater
    def pararRobo(self, estado):
        self.parado = estado
            
# Starts the robot and the server's thread
robot = DifferentialWheels()
robot_controller = rfa1(robot)
_thread.start_new_thread(servidor, (get_ip(),get_port()))
robot_controller.run()

