import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False) #omitir as mensagens do rasp
GPIO.setmode(GPIO.BOARD) #modo de trabalhar com a placa
GPIO.setup(12, GPIO.OUT) #último
GPIO.setup(16, GPIO.OUT) #meio
GPIO.setup(18, GPIO.OUT) #primeiro

GPIO.output(12,1)
GPIO.output(16,1)
GPIO.output(18,1)

time_ret_cil = 0.1

def disparar_cilindro_1():
    GPIO.output(18, 0)
    time.sleep(time_ret_cil)
    GPIO.output(18, 1)
    
def disparar_cilindro_2():
    GPIO.output(16, 0)
    time.sleep(time_ret_cil)
    GPIO.output(16, 1)
   
def disparar_cilindro_3():
    GPIO.output(12, 0)
    time.sleep(time_ret_cil)
    GPIO.output(12, 1)