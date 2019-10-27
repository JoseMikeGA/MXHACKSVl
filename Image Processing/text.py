########### Python 3.2 #############
import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
from time import sleep

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'dc46f2c494e74b67b8c82ec83d443b7d',
}

params = urllib.parse.urlencode({
    # Request parameters
    'mode': 'Printed',
})

image_path = "C:\\Users\\Miguel Gomez\\Pictures\\logo.jpg"

# Read the image into a byte array
image_data = open(image_path, "rb").read()

try:
    conn = http.client.HTTPSConnection(
        'prueba-bravitos.cognitiveservices.azure.com')
    conn.request("POST", "/vision/v2.0/recognizeText?%s" %
                 params, image_data, headers)
    response = conn.getresponse()
    link = response.headers.get("Operation-Location")
    conn.close()
    sleep(3)
    conn = http.client.HTTPSConnection(
        'prueba-bravitos.cognitiveservices.azure.com')
    conn.request("GET", "/vision/v2.0/textOperations/" + link.rpartition("/")[2], headers={
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'dc46f2c494e74b67b8c82ec83d443b7d',
    })
    print(conn.getresponse().read())
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
