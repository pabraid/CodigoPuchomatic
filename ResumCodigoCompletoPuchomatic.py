import RPi.GPIO as GPIO
from time import sleep
import threading as th
GPIO.setmode(GPIO.BOARD)

#SETEO DE MOTORES TOTALES

global TOTAL_MOTORS
TOTAL_MOTORS=6

# CODIGO PARA CONTROL DE MOTOR CON 1 SENSOR HALL
STOP = 0 
MOVING = 1
START_MOVING = 2

##################### GPIOS CONFIG #########################

#POS 0 - MOTOR1+SENS1 | POS 1 - MOTOR2+SENS ....
MOTORS = [3,5,7,11,13,15]
SENSORS_TOP = [8,16,24,36,33,23]
SENSORS_BOT = [10,18,26,38,35,29]
HALL_SENSORS = [12,22,32,40,37,31]

#Seteo de GPIOS
for i in range(TOTAL_MOTORS):
    GPIO.setup(MOTORS[i],GPIO.OUT)
    GPIO.setup(SENSORS_TOP[i],GPIO.IN)
    GPIO.setup(SENSORS_BOT[i],GPIO.IN)
    GPIO.setup(HALL_SENSORS[i],GPIO.IN,pull_up_down=GPIO.PUD_UP)


##################### CANT MAX DE DESPACHO  #########################

global MAX_DISPATCH
MAX_DISPATCH = 5

#################### GLOBALES DE MANEJO NDE MOTOR ###################
global motor_position
global dispatch_count
global Timer
global FinVuelta
global ErrorMotor
global ContarTiempo
global timer_flag

timer_flag = False
ContarTiempo = [False,False,False,False,False,False]
ErrorMotor = [False,False,False,False,False,False] 
FinVuelta = [False,False,False,False,False,False]
motor_position = STOP
dispatch_count= [0,0,0,0,0,0]
###### INFORMO SENSOR TOP OBS (0) -> HAY 5 ATADOS
###### INFORMO SENSOR TOP NO OBS (1) -> HAY MENOS DE 5 ATADOS

############ FUNCION PARA OBTENCION DE ESTADOS DE SENSOR SUPERIOR ( 5 ATADOS)
def is_top_obs(num):
    return GPIO.input(SENSORS_TOP[num-1])
        
    
###### INFORMO SENSOR BOT OBS (0)-> HAY AL MENOS 1 ATADO
###### INFORMO SENSOR BOT NO OBS (1)-> NO HAY ATADOS
    ############ FUNCION PARA OBTENCION DE ESTADOS DE SENSOR SUPERIOR ( 1 ATADO)
def is_bot_obs(num):
    return GPIO.input(SENSORS_BOT[num-1])
    
############ FUNCION PARA FRENO DE MOTOR
def StopMotor(num):
    GPIO.output(MOTORS[num-1],GPIO.HIGH)

############ FUNCION PARA MOVER EL MOTOR DE CADA COLUMNA
def MoveMotor(num,cant):
    global dispatch_count
    global motor_position
    global Timer
    global FinVuelta
    global ContarTiempo
    global timer_flag
    
    ############ EL MOVIMIENTO SE BASA EN LOS ESTADOS DE STOP, START MOVING Y MOVING
    
        ############ LEO EL SENSOR PARA SABER EN QUE ESTADO ESTOY O SI TENGO QUE PASAR A OTRO ESTADO
    hall_1_state = GPIO.input(HALL_SENSORS[num-1])
        #print("Hall state =" + str(hall_1_state) )
    if(motor_position == START_MOVING):
        ############ SI ME DIERON LA ORDEN DE ARRANCAR EL MOVIENTO PRENDO EL MOTOR
        GPIO.output(MOTORS[num-1],GPIO.LOW)                
            
    if hall_1_state and motor_position == START_MOVING:
        ############ SI ME DIERON LA ORDEN DE EMPEZAR A MOVERME Y ESTOY VIENDO EL IMAN CONFIRMO QUE EMPECE A MOVERME
        ############ PASO A ESTADO MOVING Y ANULO EL TIMER DE TIMEOUT
        motor_position = MOVING
        FinVuelta[num-1] = False
        ContarTiempo[num-1] = False    
        timer_flag = False
            
    elif not hall_1_state and motor_position == START_MOVING:
        ############ SI EN CAMBIO ME DIERON LA ORDEN DE MOVERME PERO NO VEO EL IMAN ES PORQUE ESTOY ATASCADO, INICIO EL CONTEO DEL TIMEOUT
        ContarTiempo[num-1] = True
        if timer_flag == False:
            timer_flag = True
            Timer = th.Timer(5,checkMotorStatus(num))
            Timer.start()
            
    elif not hall_1_state and motor_position == MOVING:
        ############ SI YA ESTABA EN ESTADO MOVING Y VULEVO A VER EL IMAN ES PORQUE DI UNA VUELTA COMPLETA
        motor_position = STOP
        #Timer.cancel() # paro el timer  cuando llego al proximo iman
        GPIO.output(MOTORS[num-1],GPIO.HIGH)
        FinVuelta[num-1] = True
            
            # arranco timer de chequeo de estado del motor para ver si se clavo
            
            ############ SI NO TERMINE DE CONTAR EL TOTAL DE ATADOS A DESPACHAR VUELVO A MOVERME    
        if(dispatch_count[num-1] < cant):
            dispatch_count[num-1] = dispatch_count[num-1]+ 1
            motor_position = START_MOVING

############ FUNCION DE DESPACHO DE ATADOS, RECIBE COMO ARGUMENTO LA COLUMNA PARA DESPACHAR Y LA CANTIDAD A DESPACHAR
def Dispatch(cant,num_column):
    global dispatch_count # aca llevo la cuenta de cuantos despache
    global motor_position,MAX_DISPATCH
    global ErrorMotor
    dispatch_count[num_column-1] = 0
    ErrorMotor[num_column-1] = False
    #### motor 1
    if is_bot_obs(num_column) == 0:
        if( is_top_obs(1) == 0 and cant > MAX_DISPATCH ):
            cant = MAX_DISPATCH 
        elif( is_top_obs(1) == 1 and cant > 1 ):
            cant = 1 
        motor_position = START_MOVING
        while dispatch_count[num_column-1] < cant and ErrorMotor[num_column-1] == False:
            MoveMotor(MOTORS[num_column-1],cant)
    
############ FUNCION PARA TIMEOUT
def checkMotorStatus(motor_number):
    global FinVuelta
    global ErrorMotor
    global Timer
    global ContarTiempo
    print("cuento tiempo")
    global timer_flag
    timer_flag = False

    if(ContarTiempo[motor_number-1] == True):
        ContarTiempo[motor_number-1] = False
        ErrorMotor[motor_number-1] = True
        StopMotor(motor_number)
    
def checkMotorError(motor_number):
    global ErrorMotor
    return ErrorMotor[motor_number-1]

Timer = th.Timer(5,checkMotorStatus(1))
            
while  True:
    
    for i in range (TOTAL_MOTORS):
        GPIO.output(MOTORS[i],GPIO.HIGH)
        sens_bot = GPIO.input(SENSORS_BOT[TOTAL_MOTORS])
        print("SENSOR BOT"+ str(TOTAL_MOTORS) + " =" + str(sens_bot))
        sens_top = GPIO.input(SENSORS_TOP[TOTAL_MOTORS])
        print("SENSOR TOP" + str(TOTAL_MOTORS) + "=" + str(sens_top))
    
    print("INGRESAR CANTIDAD DE PAQUETES")
    command = raw_input()    
    print(int(command))
    Dispatch(int(command),1)