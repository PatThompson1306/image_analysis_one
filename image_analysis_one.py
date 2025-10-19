import asyncio
import json
from azure.ai.vision.imageanalysis.aio import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

#Load API key from external file and assign to variable API_KEY
try:
    with open("key.txt", "r") as key_file:
        API_KEY = key_file.read().strip()
    print("API key loaded successfully.")
except FileNotFoundError:
    print("Error: 'key.txt' file not found. Please ensure the file exists and contains your API key.")
    exit(1)

#Load endpoint from external file and assign to variable ENDPOINT
try:
    with open("endpoint.txt", "r") as endpoint_file:
        ENDPOINT = endpoint_file.read().strip()
    print("Endpoint loaded successfully.")
except FileNotFoundError:
    print("Error: 'endpoint.txt' file not found. Please ensure the file exists and contains your endpoint URL.")
    exit(1)


async def analyse_image():
    """
    Asynchronously analyses an image using Azure AI Vision service.
    This function:
    1. Creates an asynchronous Image Analysis Client with Azure credentials
    2. Reads an image file from the local 'images' directory
    3. Sends the image to Azure for analysis with three visual features:
       - TAGS: General content tags describing the image
       - OBJECTS: Specific objects detected with bounding boxes
       - READ: OCR (Optical Character Recognition) to extract text
    4. Processes and displays the results:
       - Objects detected with their confidence scores
       - Any text found in the image
       - General tags with confidence scores
    5. Returns the complete analysis result object
    """
    async with ImageAnalysisClient(
        endpoint=ENDPOINT,
        credential=AzureKeyCredential(API_KEY)
    ) as client:
        with open("images/image.jpg", "rb") as image_file:
            image_data = image_file.read()
        result = await client.analyze(
            image_data=image_data,
            visual_features=[VisualFeatures.TAGS, VisualFeatures.OBJECTS, VisualFeatures.READ],
        )
        print("\nImage Analysis Results:")
        if result.objects:
            print("\nObjects Detected:")
            for obj in result.objects.list:
                tag = obj.tags[0] if obj.tags else None
                if tag:
                    print(f"  - {tag.name} (confidence: {tag.confidence:.2f})")        
        if result.read:
            print("\nText Found in Image:")
            for block in result.read.blocks:
                for line in block.lines:
                    print(f"  - {line.text}")
        if result.tags:
            print("\nTags:")
            for tag in result.tags.list:
                print(f"  - {tag.name} (confidence: {tag.confidence:.2f})")
        
        # Save the result as JSON
        result_dict = result.as_dict()
        with open("analysis_result.json", "w") as json_file:
            json.dump(result_dict, json_file, indent=4)
        print("\nAnalysis results saved to 'analysis_result.json'")
        
        return result

# Starts the async function
if __name__ == "__main__":
    result = asyncio.run(analyse_image())