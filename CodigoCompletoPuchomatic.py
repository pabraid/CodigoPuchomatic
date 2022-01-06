import RPi.GPIO as GPIO
from time import sleep
import threading as th
GPIO.setmode(GPIO.BOARD)

# CODIGO PARA CONTROL DE MOTOR CON 1 SENSOR HALL
STOP = 0 
MOVING = 1
START_MOVING = 2

##################### GPIOS CONFIG #########################
MOTOR_1 = 3
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

GPIO.setup(HALL_SENSOR_2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(SENSOR_TOP_2,GPIO.IN)
GPIO.setup(SENSOR_BOT_2,GPIO.IN)
GPIO.setup(MOTOR_2,GPIO.OUT)

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
global Timer
global FinVuelta_1,FinVuelta_2,FinVuelta_3,FinVuelta_4,FinVuelta_5,FinVuelta_6
global ErrorMotor1,ErrorMotor2,ErrorMotor3,ErrorMotor4,ErrorMotor5,ErrorMotor6
global ContarTiempo1,ContarTiempo2,ContarTiempo3,ContarTiempo4,ContarTiempo5,ContarTiempo6
global timer_flag
timer_flag = False
ContarTiempo1 = False
ContarTiempo2 = False
ContarTiempo3 = False
ContarTiempo4 = False
ContarTiempo5 = False
ContarTiempo6 = False
ErrorMotor1 = False
ErrorMotor2 = False
ErrorMotor3 = False
ErrorMotor4 = False
ErrorMotor5 = False
ErrorMotor6 = False 
FinVuelta_1 = False
FinVuelta_2 = False
FinVuelta_3 = False
FinVuelta_4 = False
FinVuelta_5 = False
FinVuelta_6 = False
motor_position = STOP
dispatch_count_1 = 0
###### INFORMO SENSOR TOP OBS (0) -> HAY 5 ATADOS
###### INFORMO SENSOR TOP NO OBS (1) -> HAY MENOS DE 5 ATADOS

############ FUNCION PARA OBTENCION DE ESTADOS DE SENSOR SUPERIOR ( 5 ATADOS)
def is_top_obs(num):
    if(num == 1):
        return GPIO.input(SENSOR_TOP_1)
    if(num == 2):
        return GPIO.input(SENSOR_TOP_2)
    if(num == 3):
        return GPIO.input(SENSOR_TOP_3)
    if(num == 4):
        return GPIO.input(SENSOR_TOP_4)
    if(num == 5):
        return GPIO.input(SENSOR_TOP_5)
    if(num == 6):
        return GPIO.input(SENSOR_TOP_6)
        
    
###### INFORMO SENSOR BOT OBS (0)-> HAY AL MENOS 1 ATADO
###### INFORMO SENSOR BOT NO OBS (1)-> NO HAY ATADOS
    ############ FUNCION PARA OBTENCION DE ESTADOS DE SENSOR SUPERIOR ( 1 ATADO)
def is_bot_obs(num):
    if(num == 1):
        return GPIO.input(SENSOR_BOT_1)
    if(num == 2):
        return GPIO.input(SENSOR_BOT_2)
    if(num == 3):
        return GPIO.input(SENSOR_BOT_3)
    if(num == 4):
        return GPIO.input(SENSOR_BOT_4)
    if(num == 5):
        return GPIO.input(SENSOR_BOT_5)
    if(num == 6):
        return GPIO.input(SENSOR_BOT_6)

############ FUNCION PARA FRENO DE MOTOR
def StopMotor(num):
    if(num == 1):
        GPIO.output(MOTOR_1,GPIO.HIGH)
    if(num == 2):
        GPIO.output(MOTOR_2,GPIO.HIGH)
    if(num == 3):
        GPIO.output(MOTOR_3,GPIO.HIGH)
    if(num == 4):
        GPIO.output(MOTOR_4,GPIO.HIGH)
    if(num == 5):
        GPIO.output(MOTOR_5,GPIO.HIGH)
    if(num == 6):
        GPIO.output(MOTOR_6,GPIO.HIGH)

############ FUNCION PARA MOVER EL MOTOR DE CADA COLUMNA
def MoveMotor(num,cant):
    global dispatch_count_1
    global motor_position
    global Timer
    global FinVuelta_1,FinVuelta_2,FinVuelta_3,FinVuelta_4,FinVuelta_5,FinVuelta_6
    global ContarTiempo1,ContarTiempo2,ContarTiempo3,ContarTiempo4,ContarTiempo5,ContarTiempo6
    global timer_flag
    
    ############ EL MOVIMIENTO SE BASA EN LOS ESTADOS DE STOP, START MOVING Y MOVING
    if num == MOTOR_1:
        ############ LEO EL SENSOR PARA SABER EN QUE ESTADO ESTOY O SI TENGO QUE PASAR A OTRO ESTADO
        hall_1_state = GPIO.input(HALL_SENSOR_1)
        #print("Hall state =" + str(hall_1_state) )
        if(motor_position == START_MOVING):
            ############ SI ME DIERON LA ORDEN DE ARRANCAR EL MOVIENTO PRENDO EL MOTOR
            GPIO.output(MOTOR_1,GPIO.LOW)                
            
        if hall_1_state and motor_position == START_MOVING:
            ############ SI ME DIERON LA ORDEN DE EMPEZAR A MOVERME Y ESTOY VIENDO EL IMAN CONFIRMO QUE EMPECE A MOVERME
            ############ PASO A ESTADO MOVING Y ANULO EL TIMER DE TIMEOUT
            motor_position = MOVING
            FinVuelta_1 = False
            ContarTiempo1 = False    
            timer_flag = False
            
        elif not hall_1_state and motor_position == START_MOVING:
            ############ SI EN CAMBIO ME DIERON LA ORDEN DE MOVERME PERO NO VEO EL IMAN ES PORQUE ESTOY ATASCADO, INICIO EL CONTEO DEL TIMEOUT
           ContarTiempo1 = True
           if timer_flag == False:
                timer_flag = True
                Timer = th.Timer(5,checkMotorStatus)
                Timer.start()
            
        elif not hall_1_state and motor_position == MOVING:
            ############ SI YA ESTABA EN ESTADO MOVING Y VULEVO A VER EL IMAN ES PORQUE DI UNA VUELTA COMPLETA
            motor_position = STOP
            #Timer.cancel() # paro el timer  cuando llego al proximo iman
            GPIO.output(MOTOR_1,GPIO.HIGH)
            FinVuelta_1 = True
            
            # arranco timer de chequeo de estado del motor para ver si se clavo
            
            ############ SI NO TERMINE DE CONTAR EL TOTAL DE ATADOS A DESPACHAR VUELVO A MOVERME    
            if(dispatch_count_1 < cant):
                dispatch_count_1 = dispatch_count_1 + 1
                motor_position = START_MOVING
    
    if num == MOTOR_2:
        
        hall_1_state = GPIO.input(HALL_SENSOR_2)
        #print("Hall state =" + str(hall_1_state) )
        if(motor_position == START_MOVING):
            GPIO.output(MOTOR_2,GPIO.LOW)                
            
        if hall_1_state and motor_position == START_MOVING:
            
            motor_position = MOVING
            FinVuelta_2 = False
            ContarTiempo2= False    
            timer_flag = False
            
        elif not hall_1_state and motor_position == START_MOVING:
           ContarTiempo2 = True
           if timer_flag == False:
                timer_flag = True
                Timer = th.Timer(5,checkMotorStatus)
                Timer.start()
            
        elif not hall_1_state and motor_position == MOVING:
            motor_position = STOP
            #Timer.cancel() # paro el timer  cuando llego al proximo iman
            GPIO.output(MOTOR_2,GPIO.HIGH)
            FinVuelta_2 = True
            
            # arranco timer de chequeo de estado del motor para ver si se clavo 
            if(dispatch_count_1 < cant):
                dispatch_count_1 = dispatch_count_1 + 1
                motor_position = START_MOVING
    
    if num == MOTOR_3:
        
        hall_1_state = GPIO.input(HALL_SENSOR_3)
        #print("Hall state =" + str(hall_1_state) )
        if(motor_position == START_MOVING):
            GPIO.output(MOTOR_3,GPIO.LOW)                
            
        if hall_1_state and motor_position == START_MOVING:
            
            motor_position = MOVING
            FinVuelta_3 = False
            ContarTiempo3= False    
            timer_flag = False
            
        elif not hall_1_state and motor_position == START_MOVING:
           ContarTiempo3 = True
           if timer_flag == False:
                timer_flag = True
                Timer = th.Timer(5,checkMotorStatus)
                Timer.start()
            
        elif not hall_1_state and motor_position == MOVING:
            motor_position = STOP
            #Timer.cancel() # paro el timer  cuando llego al proximo iman
            GPIO.output(MOTOR_3,GPIO.HIGH)
            FinVuelta_3 = True
            
            # arranco timer de chequeo de estado del motor para ver si se clavo 
            if(dispatch_count_1 < cant):
                dispatch_count_1 = dispatch_count_1 + 1
                motor_position = START_MOVING

    if num == MOTOR_4:
        
        hall_1_state = GPIO.input(HALL_SENSOR_4)
        #print("Hall state =" + str(hall_1_state) )
        if(motor_position == START_MOVING):
            GPIO.output(MOTOR_4,GPIO.LOW)                
            
        if hall_1_state and motor_position == START_MOVING:
            
            motor_position = MOVING
            FinVuelta_4= False
            ContarTiempo4 = False    
            timer_flag = False
            
        elif not hall_1_state and motor_position == START_MOVING:
           ContarTiempo4= True
           if timer_flag == False:
                timer_flag = True
                Timer = th.Timer(5,checkMotorStatus)
                Timer.start()
            
        elif not hall_1_state and motor_position == MOVING:
            motor_position = STOP
            #Timer.cancel() # paro el timer  cuando llego al proximo iman
            GPIO.output(MOTOR_4,GPIO.HIGH)
            FinVuelta_4= True
            
            # arranco timer de chequeo de estado del motor para ver si se clavo
            if(dispatch_count_1 < cant):
                dispatch_count_1 = dispatch_count_1 + 1
                motor_position = START_MOVING           

    if num == MOTOR_5:
        
        hall_1_state = GPIO.input(HALL_SENSOR_5)
        #print("Hall state =" + str(hall_1_state) )
        if(motor_position == START_MOVING):
            GPIO.output(MOTOR_5,GPIO.LOW)                
            
        if hall_1_state and motor_position == START_MOVING:
            
            motor_position = MOVING
            FinVuelta_5 = False
            ContarTiempo5 = False    
            timer_flag = False
            
        elif not hall_1_state and motor_position == START_MOVING:
           ContarTiempo5 = True
           if timer_flag == False:
                timer_flag = True
                Timer = th.Timer(5,checkMotorStatus)
                Timer.start()
            
        elif not hall_1_state and motor_position == MOVING:
            motor_position = STOP
            #Timer.cancel() # paro el timer  cuando llego al proximo iman
            GPIO.output(MOTOR_5,GPIO.HIGH)
            FinVuelta_5= True
            
            # arranco timer de chequeo de estado del motor para ver si se clavo
            if(dispatch_count_1 < cant):
                dispatch_count_1 = dispatch_count_1 + 1
                motor_position = START_MOVING

    if num == MOTOR_6:
        
        hall_1_state = GPIO.input(HALL_SENSOR_6)
        #print("Hall state =" + str(hall_1_state) )
        if(motor_position == START_MOVING):
            GPIO.output(MOTOR_6,GPIO.LOW)                
            
        if hall_1_state and motor_position == START_MOVING:
            
            motor_position = MOVING
            FinVuelta_6 = False
            ContarTiempo6 = False    
            timer_flag = False
            
        elif not hall_1_state and motor_position == START_MOVING:
           ContarTiempo1 = True
           if timer_flag == False:
                timer_flag = True
                Timer = th.Timer(5,checkMotorStatus)
                Timer.start()
            
        elif not hall_1_state and motor_position == MOVING:
            motor_position = STOP
            #Timer.cancel() # paro el timer  cuando llego al proximo iman
            GPIO.output(MOTOR_6,GPIO.HIGH)
            FinVuelta_6 = True
            
            # arranco timer de chequeo de estado del motor para ver si se clavo   
            if(dispatch_count_1 < cant):
                dispatch_count_1 = dispatch_count_1 + 1
                motor_position = START_MOVING

############ FUNCION DE DESPACHO DE ATADOS, RECIBE COMO ARGUMENTO LA COLUMNA PARA DESPACHAR Y LA CANTIDAD A DESPACHAR
def Dispatch(cant,num_column):
    global dispatch_count_1 #aca llevo la cuenta de cuantos despache
    global motor_position,MAX_DISPATCH
    global ErrorMotor1,ErrorMotor2,ErrorMotor3,ErrorMotor4,ErrorMotor5,ErrorMotor6
    dispatch_count_1 = 0
    ErrorMotor1 = False
    #### motor 1
    if( num_column==1 and (is_bot_obs(1) == 0)):
        if( is_top_obs(1) == 0 and cant > MAX_DISPATCH ):
            cant = MAX_DISPATCH 
        elif( is_top_obs(1) == 1 and cant > 1 ):
            cant = 1 
        motor_position = START_MOVING
        while dispatch_count_1 < cant and ErrorMotor1 == False:
            MoveMotor(MOTOR_1,cant)
    #### motor 2
    if( num_column==2 and (is_bot_obs(2) == 0)):
        if( is_top_obs(2) == 0 and cant > MAX_DISPATCH ):
            cant = MAX_DISPATCH 
        elif( is_top_obs(2) == 1 and cant > 1 ):
            cant = 1 
        motor_position = START_MOVING
        while dispatch_count_1 < cant and ErrorMotor2 == False:
            MoveMotor(MOTOR_2,cant)
    #### motor 3
    if( num_column==3 and (is_bot_obs(3) == 0)):
        if( is_top_obs(3) == 0 and cant > MAX_DISPATCH ):
            cant = MAX_DISPATCH 
        elif( is_top_obs(3) == 1 and cant > 1 ):
            cant = 1 
        motor_position = START_MOVING
        while dispatch_count_1 < cant and ErrorMotor3 == False:
            MoveMotor(MOTOR_3,cant)
    #### motor 4
    if( num_column==4 and (is_bot_obs(4) == 0)):
        if( is_top_obs(4) == 0 and cant > MAX_DISPATCH ):
            cant = MAX_DISPATCH 
        elif( is_top_obs(4) == 1 and cant > 1 ):
            cant = 1 
        motor_position = START_MOVING
        while dispatch_count_1 < cant and ErrorMotor4 == False:
            MoveMotor(MOTOR_4,cant)
    #### motor 5
    if( num_column==5 and (is_bot_obs(5) == 0)):
        if( is_top_obs(5) == 0 and cant > MAX_DISPATCH ):
            cant = MAX_DISPATCH 
        elif( is_top_obs(5) == 1 and cant > 1 ):
            cant = 1 
        motor_position = START_MOVING
        while dispatch_count_1 < cant and ErrorMotor5 == False:
            MoveMotor(MOTOR_5,cant)
    #### motor 6
    if( num_column==6 and (is_bot_obs(6) == 0)):
        if( is_top_obs(6) == 0 and cant > MAX_DISPATCH ):
            cant = MAX_DISPATCH 
        elif( is_top_obs(6) == 1 and cant > 1 ):
            cant = 1 
        motor_position = START_MOVING
        while dispatch_count_1 < cant and ErrorMotor6 == False:
            MoveMotor(MOTOR_6,cant)

############ FUNCION PARA TIMEOUT
def checkMotorStatus():
    global FinVuelta_1,FinVuelta_2,FinVuelta_3,FinVuelta_4,FinVuelta_5,FinVuelta_6
    global ErrorMotor1,ErrorMotor2,ErrorMotor3,ErrorMotor4,ErrorMotor5,ErrorMotor6
    global Timer
    global ContarTiempo1,ContarTiempo2,ContarTiempo3,ContarTiempo4,ContarTiempo5,ContarTiempo6
    print("cuento tiempo")
    global timer_flag
    timer_flag = False

    if(ContarTiempo1 == True):
        ContarTiempo1 = False
        ErrorMotor1 = True
        StopMotor(1)
    if(ContarTiempo2 == True):
        ContarTiempo2 = False
        ErrorMotor2 = True
        StopMotor(2)
    if(ContarTiempo3 == True):
        ContarTiempo3 = False
        ErrorMotor3 = True
        StopMotor(3)
    if(ContarTiempo4 == True):
        ContarTiempo4 = False
        ErrorMotor4 = True
        StopMotor(4)
    if(ContarTiempo5 == True):
        ContarTiempo5 = False
        ErrorMotor5 = True
        StopMotor(5)
    if(ContarTiempo6 == True):
        ContarTiempo6 = False
        ErrorMotor6 = True
        StopMotor(6)

def checkMotorError():
    global ErrorMotor1
    return ErrorMotor1

Timer = th.Timer(5,checkMotorStatus)
            
while  True:
    
    GPIO.output(MOTOR_1,GPIO.HIGH)
    GPIO.output(MOTOR_2,GPIO.HIGH)
    GPIO.output(MOTOR_3,GPIO.HIGH)
    GPIO.output(MOTOR_4,GPIO.HIGH)
    GPIO.output(MOTOR_5,GPIO.HIGH)
    GPIO.output(MOTOR_6,GPIO.HIGH)
    sens_bot1 = GPIO.input(SENSOR_BOT_1)
    print("SENSOR BOT 1 =" + str(sens_bot1))
    sens_top1 = GPIO.input(SENSOR_TOP_1)
    print("SENSOR TOP 1 =" + str(sens_top1))
    
    sens_bot2 = GPIO.input(SENSOR_BOT_2)
    print("SENSOR BOT 2 =" + str(sens_bot2))
    sens_top2 = GPIO.input(SENSOR_TOP_2)
    print("SENSOR TOP 2 =" + str(sens_top2))
    
    sens_bot3 = GPIO.input(SENSOR_BOT_3)
    print("SENSOR BOT 3 =" + str(sens_bot3))
    sens_top3 = GPIO.input(SENSOR_TOP_3)
    print("SENSOR TOP 3 =" + str(sens_top3))
 
    sens_bot4 = GPIO.input(SENSOR_BOT_4)
    print("SENSOR BOT 4 =" + str(sens_bot4))
    sens_top4 = GPIO.input(SENSOR_TOP_4)
    print("SENSOR TOP 4 =" + str(sens_top4))
 
    sens_bot5 = GPIO.input(SENSOR_BOT_5)
    print("SENSOR BOT 5 =" + str(sens_bot5))
    sens_top5 = GPIO.input(SENSOR_TOP_5)
    print("SENSOR TOP 5 =" + str(sens_top5))
 
    sens_bot6 = GPIO.input(SENSOR_BOT_6)
    print("SENSOR BOT 6 =" + str(sens_bot6))
    sens_top6 = GPIO.input(SENSOR_TOP_6)
    print("SENSOR TOP 6 =" + str(sens_top6))
 
    print("INGRESAR CANTIDAD DE PAQUETES")
    command = raw_input()    
    print(int(command))
    Dispatch(int(command),1)
#sleep(1)