import RPi.GPIO as GPIO
from time import sleep
import threading as th
GPIO.setmode(GPIO.BOARD)

# CODIGO PARA CONTROL DE MOTOR CON 1 SENSOR HALL
STOP = 0 
MOVING = 1
START_MOVING = 2

##################### GPIOS CONFIG #########################
MOTOR_1 = 5
SENSOR_TOP_1 = 8
SENSOR_BOT_1 = 10
HALL_SENSOR_1 = 12

MOTOR_2 = 5
SENSOR_TOP_2 = 16
SENSOR_BOT_2 = 18
HALL_SENSOR_2 = 22

MOTOR_3 = 7
SENSOR_TOP_3 = 24
SENSOR_BOT_3 = 26
HALL_SENSOR_3 = 32

MOTOR_4 = 11
SENSOR_TOP_4 = 36
SENSOR_BOT_4 = 38
HALL_SENSOR_4 = 40

MOTOR_5 = 13
SENSOR_TOP_5 = 33
SENSOR_BOT_5 = 35
HALL_SENSOR_5 = 37

MOTOR_6 = 15
SENSOR_TOP_6 = 23
SENSOR_BOT_6 = 29
HALL_SENSOR_6 = 31


GPIO.setup(HALL_SENSOR_1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(SENSOR_TOP_1,GPIO.IN)
GPIO.setup(SENSOR_BOT_1,GPIO.IN)
GPIO.setup(MOTOR_1,GPIO.OUT)

# GPIO.setup(HALL_SENSOR_2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# GPIO.setup(SENSOR_TOP_2,GPIO.IN)
# GPIO.setup(SENSOR_BOT_2,GPIO.IN)
# GPIO.setup(MOTOR_2,GPIO.OUT)

GPIO.setup(HALL_SENSOR_3,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(SENSOR_TOP_3,GPIO.IN)
GPIO.setup(SENSOR_BOT_3,GPIO.IN)
GPIO.setup(MOTOR_3,GPIO.OUT)

GPIO.setup(HALL_SENSOR_4,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(SENSOR_TOP_4,GPIO.IN)
GPIO.setup(SENSOR_BOT_4,GPIO.IN)
GPIO.setup(MOTOR_4,GPIO.OUT)

GPIO.setup(HALL_SENSOR_5,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(SENSOR_TOP_5,GPIO.IN)
GPIO.setup(SENSOR_BOT_5,GPIO.IN)
GPIO.setup(MOTOR_5,GPIO.OUT)

GPIO.setup(HALL_SENSOR_6,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(SENSOR_TOP_6,GPIO.IN)
GPIO.setup(SENSOR_BOT_6,GPIO.IN)
GPIO.setup(MOTOR_6,GPIO.OUT)

##################### CANT MAX DE DESPACHO  #########################

global MAX_DISPATCH
MAX_DISPATCH = 5

#################### GLOBALES DE MANEJO NDE MOTOR ###################
global motor_position
global dispatch_count_1,dispatch_count_2,dispatch_count_3,dispatch_count_4,dispatch_count_5,dispatch_count_6
global Timer,FinVuelta_1
global ErrorMotor1
global ContarTiempo1
global timer_flag
timer_flag = False
ContarTiempo1 = False
ErrorMotor1 = False
FinVuelta_1 = False
motor_position = STOP
dispatch_count_1 = 0
###### INFORMO SENSOR TOP OBS (0) -> HAY 5 ATADOS
###### INFORMO SENSOR TOP NO OBS (1) -> HAY MENOS DE 5 ATADOS
def is_top_obs(num):
    if(num == 1):
        return GPIO.input(SENSOR_TOP_1)
    
###### INFORMO SENSOR BOT OBS (0)-> HAY AL MENOS 1 ATADO
###### INFORMO SENSOR BOT NO OBS (1)-> NO HAY ATADOS
def is_bot_obs(num):
    if(num == 1):
        return GPIO.input(SENSOR_BOT_1)
def StopMotor(num):
    if(num == 1):
        GPIO.output(MOTOR_1,GPIO.HIGH)
        
def MoveMotor(num,cant):
    global dispatch_count_1
    global motor_position
    global Timer
    global FinVuelta_1
    global ContarTiempo1
    global timer_flag
    if num == MOTOR_1:
        
        hall_1_state = GPIO.input(HALL_SENSOR_1)
        if(motor_position == START_MOVING):
            GPIO.output(MOTOR_1,GPIO.LOW)                
        if hall_1_state and motor_position == START_MOVING:
            motor_position = MOVING
            FinVuelta_1 = False
            ContarTiempo1 = True
            # arranco timer de chequeo de estado del motor para ver si se clavo
            if timer_flag == False:
                timer_flag = True
                Timer = th.Timer(5,checkMotorStatus)
                Timer.start()
                
        elif not hall_1_state and motor_position == MOVING:
            motor_position = STOP
            #Timer.cancel() # paro el timer  cuando llego al proximo iman
            GPIO.output(MOTOR_1,GPIO.HIGH)
            FinVuelta_1 = True
            ContarTiempo1 = False
            timer_flag = False
                
            if(dispatch_count_1 < cant):
                dispatch_count_1 = dispatch_count_1 + 1
                motor_position = START_MOVING
                
def Dispatch(cant,num_column):
    global dispatch_count_1 #aca llevo la cuenta de cuantos despache
    global motor_position,MAX_DISPATCH
    global ErrorMotor1
    dispatch_count_1 = 0
    ErrorMotor1 = False
    
    if( num_column==1 and (is_bot_obs(1) == 0)):
        if( is_top_obs(1) == 0 and cant > MAX_DISPATCH ):
            cant = MAX_DISPATCH 
        elif( is_top_obs(1) == 1 and cant > 1 ):
            cant = 1 
        motor_position = START_MOVING
        while dispatch_count_1 < cant and ErrorMotor1 == False:
            MoveMotor(MOTOR_1,cant)

def checkMotorStatus():
    global FinVuelta_1
    global ErrorMotor1
    global Timer
    global ContarTiempo1
    print("cuento tiempo")
    global timer_flag
    timer_flag = False

    if(FinVuelta_1 == False and ContarTiempo1 == True):
        ContarTiempo1 = False
        ErrorMotor1 = True
        StopMotor(1)

def checkMotorError():
    global ErrorMotor1
    return ErrorMotor1

Timer = th.Timer(5,checkMotorStatus)
            
while  True:
    
    GPIO.output(MOTOR_1,GPIO.HIGH)
    sens_bot1 = GPIO.input(SENSOR_BOT_1)
    print("SENSOR BOT =" + str(sens_bot1))
    sens_top1 = GPIO.input(SENSOR_TOP_1)
    print("SENSOR TOP =" + str(sens_top1))
 
    print("INGRESAR CANTIDAD DE PAQUETES")
    command = raw_input()    
    print(int(command))
    Dispatch(int(command),1)
#sleep(1)