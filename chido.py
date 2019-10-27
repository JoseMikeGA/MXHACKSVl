# coding: utf-8

# Archivo: ultrasonico.py


import RPi.GPIO as GPIO
import time
from pygame import mixer

TRIG = 18
ECHO = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

print "Medición de distancias en progreso"
mixer.init()
mixer.music.load("beep.mp3")

		
try:
    while True:
	time.sleep(0.5)
        GPIO.output(TRIG, GPIO.LOW)
        print "Esperando a que el sensor se estabilice"
        time.sleep(0.01)
        GPIO.output(TRIG, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(TRIG, GPIO.LOW)
        print "Iniciando eco"
        while True:
            pulso_inicio = time.time()
            if GPIO.input(ECHO) == GPIO.HIGH:
                break
        while True:
            pulso_fin = time.time()
            if GPIO.input(ECHO) == GPIO.LOW:
                break
        duracion = pulso_fin - pulso_inicio
        distancia = (34300 * duracion) / 2
        print "Distancia: %.2f cm" % distancia

#Para los rangos y repruduccion de sonidos

	if distancia <= 150 and distancia >= 100:
		print "Objeto Detectado"
		print "Distancia: %.2f cm" % distancia
		
		mixer.music.play()		
	elif distancia <= 99 and distancia >= 50:
		for i in range(2):
			mixer.music.play()
			time.sleep(0.1)	 
            mixer.music.stop()
	elif distancia < 50:
		for i in range(3):
			mixer.music.play()
			time.sleep(0.1)	 
            mixer.music.stop()
finally:
    GPIO.cleanup()