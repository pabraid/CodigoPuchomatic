import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)

# CODIGO PARA CONTROL DE MOTOR CON 1 SENSOR HALL
STOP = 0
MOVING = 1
START_MOVING = 2 
GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(5,GPIO.OUT)
motor_position = STOP
command = 'S'
while  True:
    hall_1_state = GPIO.input(12)
    print(hall_1_state)

    if(motor_position == START_MOVING):
        GPIO.output(5,GPIO.LOW)
        print('empezando a mover')
        command = 'S'
    if hall_1_state and motor_position == START_MOVING:
        motor_position = MOVING
        print('moviendose')
    elif not hall_1_state and motor_position == MOVING:
        motor_position = STOP
        GPIO.output(5,GPIO.HIGH)
        print('stopped')

    if motor_position == STOP:
        print('Ingresar comando')
        command = raw_input()
    
#       
    if command == 'M':
        motor_position = START_MOVING
#     else:
#         motor_position = MOVING
#         
#     if (motor_position == STOP and (not hall_1_state)):
#         # ARRANCO EL MOTOR
#         GPIO.output(5,GPIO.HIGH)
#         print('MOTOR INIT')
#     elif(hall_1_state and motor_position == STOP):
#         #         DETECTO QUE EL MOTOR ESTA EN MOVIMIENTO POR EL SENSOR
#         motor_position = MOVING
#         print('MOTOR MOVING')
#     elif ((not hall_1_state) and motor_position == MOVING) :
#         # EL MOTOR ESTABA EN MOVIMIENTO Y VUELVO A DETECTAR EL SENSOR, LO PARO
#         GPIO.output(5,GPIO.LOW)
#         motor_position = STOP
#         print('MOTOR COMPLETE')
#          
#    sleep(0.05)
    
    
