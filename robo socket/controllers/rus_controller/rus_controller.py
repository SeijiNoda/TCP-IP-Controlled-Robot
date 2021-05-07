"""rus_controller controller."""

#by slmm for TI502

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import time

print("Iniciando")
# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = 64 #int(robot.getBasicTimeStep())

nome = robot.getName()
print("Nome do robo : ", nome)

motor_esq = robot.getDevice("motor roda esquerda")
motor_dir = robot.getDevice("motor roda direita")

motor_esq.setPosition(float('+inf'))
motor_dir.setPosition(float('+inf'))

motor_esq.setVelocity(0.0)
motor_dir.setVelocity(0.0)

# obtem o sensor de distancia
ir0 = robot.getDevice("ir0")
ir0.enable(timestep)

ir1 = robot.getDevice("ir1")
ir1.enable(timestep)

ir2 = robot.getDevice("ir2")
ir2.enable(timestep)

ir3 = robot.getDevice("ir3")
ir3.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
virando = None
while robot.step(timestep) != -1: 
    distTras = ir0.getValue()
    distFrente = ir1.getValue()
    distEsq = ir2.getValue()
    distDir = ir3.getValue()
    
    #print("tras: " + str(distTras) + " frente: " + str(distFrente))    
    #print("esq: " + str(distEsq) + " dir: " + str(distDir))    
    
    # Process sensor data here.
    temParedeFrente = distFrente >= 300    #temParedeAtras  = distTras   >= 215
    temParedeDir    = distDir    >= 200
    temParedeEsq    = distEsq    >= 200 
    temParedeEsqDir = temParedeDir and temParedeEsq


    if virando != None:
        if not temParedeFrente:
            virando = None
        elif virando == "meia_volta":
            motor_dir.setVelocity(2.0)
            motor_esq.setVelocity(-2.0)
        elif virando == "dir":
            motor_dir.setVelocity(2.0)
            motor_esq.setVelocity(-2.0)
        elif virando == "esq":
            motor_dir.setVelocity(-2.0)
            motor_esq.setVelocity(2.0)
    elif temParedeFrente: # se tiver uma parede a frente
        if temParedeEsqDir: # se tiver uma parede em ambas
            motor_dir.setVelocity(0.0)
            motor_esq.setVelocity(0.0)
            print("frn: " + str(distFrente))
            print("esq: " + str(distEsq))
            print("dir: " + str(distDir))
            print("dando meia volta...")
            virando = "meia_volta"
        elif temParedeDir:  # se tiver uma parede na direita
            motor_dir.setVelocity(0.0)
            motor_esq.setVelocity(0.0)
            print("frn: " + str(distFrente))
            print("esq: " + str(distEsq))
            print("dir: " + str(distDir))
            print("virando a esquerda...")
            virando = "esq"
        elif temParedeEsq: # se tiver parede na esquerda
            motor_dir.setVelocity(0.0)
            motor_esq.setVelocity(0.0)
            print("frn: " + str(distFrente))
            print("esq: " + str(distEsq))
            print("dir: " + str(distDir)) 
            print("virando a direita...")
            virando = "dir"
        else: # nao tem parede nem na esquerda nem na direita
            motor_dir.setVelocity(0.0)
            motor_esq.setVelocity(0.0)
            print("frn: " + str(distFrente))
            print("esq: " + str(distEsq))
            print("dir: " + str(distDir))
            print("escolhi virar a direita...")
            virando = "dir"
    #elif not temParedeDir:
        #motor_dir.setVelocity(0.0)
        #motor_esq.setVelocity(0.0)
        #print("frn: " + str(distFrente))
        #print("esq: " + str(distEsq))
        #print("dir: " + str(distDir))
        #print("escolhi virar a direita...")
        #virando = "dir"
    else:
        motor_dir.setVelocity(-2.0)
        motor_esq.setVelocity(-2.0) 


# Enter here exit cleanup code.
