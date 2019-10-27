import cv2
import os
import requests
from xml.etree import ElementTree
from time import sleep, time
from io import BytesIO
import threading
import RPi.GPIO as GPIO
from pygame import mixer

# Computer Vision Keys
subscription_key = "dc46f2c494e74b67b8c82ec83d443b7d"
endpoint = "https://prueba-bravitos.cognitiveservices.azure.com/"
# path to Object detection service
analyze_url = endpoint + "vision/v2.1/analyze"
# Path to Text Recognition service
recognize_text_url = endpoint + "vision/v2.0/recognizeText"
# Token
access_token = ""

TRIG = 18
ECHO = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

mixer.init()
mixer.music.load("beep.mp3")


def main():
    # Start video capture
    capture = cv2.VideoCapture(2)
    # Stores the time for make an interval on the reading of image
    last_time = 0
    # Get token
    get_token()
    while True:
        # Capturar un frame
        val, frame = capture.read()
        # Encoding image to jpg format
        img_str = cv2.imencode('.jpg', frame)[1].tostring()
        cv2.imshow('Imagen', frame)

        # Obtain the actual time
        millis = int(round(time() * 1000))
        if (last_time + 2000) < millis:
            # result = detectObjectsFromImage(img_str)
            threading.Thread(target=detectTextFromImage,
                             args=(img_str,)).start()
            threading.Thread(target=detectObjectsFromImage,
                             args=(img_str,)).start()
            # Obtain new time for last_time
            last_time = int(round(time() * 1000))
        # Salir con 'ESC'
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            capture.release()
            break


def detectObjectsFromImage(image):
    # Features obteined from image
    params = {'visualFeatures': 'Objects'}
    res = requestToAzureComputerVision(analyze_url, params, image).json()
    # print(res)
    if res['objects'][0]:
        text = res['objects'][0]['object']
        speechReader(text)
    


def detectTextFromImage(image):
    # Kind of text, can be Printed and Handwrited
    params = {'mode': 'Printed'}
    response = requestToAzureComputerVision(recognize_text_url, params, image)
    # Get Header response
    search_url = response.headers.get("Operation-Location")
    sleep(0.5)
    response = requests.get(search_url, headers={
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/json'
    })
    analysis = response.json()
    print(analysis)
    # return requestToAzureComputerVision(recognize_text_url, params, image


def requestToAzureComputerVision(url, params, image):
    # Headers for azure request
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    # Make POST request to service with an image
    response = requests.post(
        url, headers=headers, params=params, data=image)
    response.raise_for_status()
    return response


def measureDistance():
    GPIO.output(TRIG, GPIO.LOW)
    print("Esperando a que el sensor se estabilice")
    sleep(0.01)
    GPIO.output(TRIG, GPIO.HIGH)
    sleep(0.01)
    GPIO.output(TRIG, GPIO.LOW)
    print("Iniciando eco")
    while True:
        pulso_inicio = time()
        if GPIO.input(ECHO) == GPIO.HIGH:
            break
    while True:
        pulso_fin = time()
        if GPIO.input(ECHO) == GPIO.LOW:
            break
    duracion = pulso_fin - pulso_inicio
    distancia = (34300 * duracion) / 2
    print("Distancia: %.2f cm" % distancia)
    validateDistance(distancia)


def validateDistance(distancia):
    if distancia <= 150 and distancia >= 100:
        print("Objeto Detectado")
        print("Distancia: %.2f cm" % distancia)
        mixer.music.play()
    elif distancia <= 99 and distancia >= 50:
        for i in range(2):
            mixer.music.play()
            sleep(0.1)
            mixer.music.stop()
    elif distancia < 50:
        for i in range(3):
            mixer.music.play()
            sleep(0.1)
            mixer.music.stop()


def get_token():
        fetch_token_url = "https://southcentralus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        access_token = str(response.text)


def speechReader(text):
    base_url = 'https://southcentralus.tts.speech.microsoft.com/'
    path = 'cognitiveservices/v1'
    constructed_url = base_url + path
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
        'User-Agent': 'MXxHacks'
    }
    xml_body = ElementTree.Element('speak', version='1.0')
    xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'es-MX')
    voice = ElementTree.SubElement(xml_body, 'voice')
    voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'es-MX')
    # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
    voice.set('name', 'es-MX-HildaRUS')
    voice.text = text
    body = ElementTree.tostring(xml_body)
    response = requests.post(constructed_url, headers=headers, data=body)
    writeWAVFile(response)

def writeWAVFile(response):
    if response.status_code == 200:
        with open('sample' + '.wav', 'wb') as audio:
            audio.write(response.content)
            playWAVFile('sample.wav')
            print("\nStatus code: " + str(response.status_code) +
                    "\nYour TTS is ready for playback.\n")
    else:
        print("\nStatus code: " + str(response.status_code) +
                "\nSomething went wrong. Check your subscription key and headers.\n")
        print("Reason: " + str(response.reason) + "\n")

def playWAVFile(file):
    voice_sound = mixer.Sound(file)
    mixer.Sound.play(voice_sound)
    sleep(2)

if __name__ == '__main__':
    main()
