import requests
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
from io import BytesIO

# Add your Computer Vision subscription key and endpoint to your environment variables.

subscription_key = "dc46f2c494e74b67b8c82ec83d443b7d"

endpoint = "https://prueba-bravitos.cognitiveservices.azure.com/"

analyze_url = endpoint + "vision/v2.1/analyze"
recognize_text_url = endpoint + "vision/v2.0/recognizeText"

# Set image_path to the local path of an image that you want to analyze.
image_path ="C:\\Users\\Miguel Gomez\\Pictures\\logo.jpg"

# Read the image into a byte array
image_data = open(image_path, "rb").read()
headers = {'Ocp-Apim-Subscription-Key': subscription_key,
           'Content-Type': 'application/octet-stream'}

#           'Content-Type': 'application/octet-stream'}
#           params = {'visualFeatures': 'Categories,Description,Color,Objects'}

# params = {'visualFeatures': 'Text'}
params = {'mode': 'Printed'}

response = requests.post(
    recognize_text_url, headers=headers, params=params, data=image_data)
response.raise_for_status()

# The 'analysis' object contains various fields that describe the image. The most
# relevant caption for the image is obtained from the 'description' property.
analysis = response.json()
print(analysis)
#image_caption = analysis["description"]["captions"][0]["text"].capitalize()
