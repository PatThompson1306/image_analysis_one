import os
from azure.ai.vision.imageanalysis.aio import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

#load API key from external file and assign to variable API_KEY
try:
    with open("key.txt", "r") as key_file:
        API_KEY = key_file.read().strip()
    print("API key loaded successfully.")
except FileNotFoundError:
    print("Error: 'key.txt' file not found. Please ensure the file exists and contains your API key.")
    exit(1)

#load endpoint from external file and assign to variable ENDPOINT
try:
    with open("endpoint.txt", "r") as endpoint_file:
        ENDPOINT = endpoint_file.read().strip()
    print("Endpoint loaded successfully.")
except FileNotFoundError:
    print("Error: 'endpoint.txt' file not found. Please ensure the file exists and contains your endpoint URL.")
    exit(1)

#creating the ImageAnalysisClient
client = ImageAnalysisClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(API_KEY)
)