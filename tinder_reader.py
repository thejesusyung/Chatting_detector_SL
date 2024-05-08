import os
import base64
import json
from google.cloud import vision
from google.oauth2 import service_account
import pandas as pd

def get_vision_client():
    # Decode the credentials from base64
    creds_json_str = base64.b64decode(os.getenv('GOOGLE_CREDENTIALS')).decode('utf-8')
    creds_dict = json.loads(creds_json_str)
    # Use the credentials to set up the client
    credentials = service_account.Credentials.from_service_account_info(creds_dict)
    client = vision.ImageAnnotatorClient(credentials=credentials)
    return client

def detect_text(image_bytes):
    """Use Google Vision API to extract text from an image."""
    client = get_vision_client()
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image)
    return response.text_annotations[0].description if response.text_annotations else ""

def process_images(folder_path):
    """Process all images in the specified folder and save the results to a CSV."""
    df = pd.DataFrame(columns=['File Name', 'Extracted Text'])

    # Iterate over all images in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Supports PNG, JPG, JPEG
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'rb') as image_file:
                image_bytes = image_file.read()
                extracted_text = detect_text(image_bytes)
                # Create a new DataFrame for the current image and concatenate it with the main DataFrame
                new_row = pd.DataFrame({'File Name': [filename], 'Extracted Text': [extracted_text]})
                df = pd.concat([df, new_row], ignore_index=True)

    # Save the DataFrame to a CSV file
    df.to_csv('tinder_output.csv', index=False)


# Usage example
if __name__ == "__main__":
    folder_path = '/Users/maxim/Desktop/Codes/OCRProject/vibe_files/photos'
    process_images(folder_path)
    #else:
     #   print("Usage: python script_name.py <folder_path>")
