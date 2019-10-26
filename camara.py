import cv2
import requests
from time import sleep,time
from io import BytesIO
import threading

# Computer Vision Keys
subscription_key = "dc46f2c494e74b67b8c82ec83d443b7d"
endpoint = "https://prueba-bravitos.cognitiveservices.azure.com/"
# path to Object detection service
analyze_url = endpoint + "vision/v2.1/analyze"
# Path to Text Recognition service
recognize_text_url = endpoint + "vision/v2.0/recognizeText"

def main():
    # Start video capture

    capture = cv2.VideoCapture(2)
    # Stores the time for make an interval on the reading of image
    last_time = 0
    while True:
        # Capturar un frame
        val, frame = capture.read()
        # Encoding image to jpg format 
        img_str = cv2.imencode('.jpg', frame)[1].tostring()
        cv2.imshow('Imagen', frame)
        
        # Obtain the actual time
        millis = int(round(time() * 1000))
        if (last_time + 2000) < millis:
            #result = detectObjectsFromImage(img_str)
            threading.Thread(target=detectTextFromImage, args=(img_str,)).start()
            threading.Thread(target=detectObjectsFromImage, args=(img_str,)).start()
            # Obtain new time for last_time
            last_time = int(round(time() * 1000))
            print(last_time)
        #Salir con 'ESC'
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            capture.release()
            break

def detectObjectsFromImage(image):
    # Features obteined from image
    params = {'visualFeatures': 'Objects'}
    print( requestToAzureComputerVision(analyze_url, params, image).json())

def detectTextFromImage(image):
    # Kind of text, can be Printed and Handwrited
    params = {'mode': 'Printed'}
    response = requestToAzureComputerVision(recognize_text_url, params, image)
    # Get Header response
    search_url = response.headers.get("Operation-Location")
    sleep(0.5)
    response = requests.get(search_url , headers={
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/json'
    })
    analysis = response.json()
    print(analysis)
    #return requestToAzureComputerVision(recognize_text_url, params, image)

def requestToAzureComputerVision(url, params, image):
    # Headers for azure request
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    # Make POST request to service with an image
    response = requests.post(
        url, headers=headers, params=params, data=image)
    response.raise_for_status()
    return response

if __name__ == '__main__':
    main()
