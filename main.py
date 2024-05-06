import os
import json
import base64
from google.oauth2 import service_account
from google.cloud import vision
import streamlit as st

def get_vision_client():
    # Decode the credentials from base64
    creds_json_str = base64.b64decode(os.getenv('GOOGLE_CREDENTIALS')).decode('utf-8')
    creds_dict = json.loads(creds_json_str)

    # Use the credentials to set up the client
    credentials = service_account.Credentials.from_service_account_info(creds_dict)
    client = vision.ImageAnnotatorClient(credentials=credentials)
    return client

def detect_text(client, image_bytes):
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description if texts else "No text found"

def main():
    st.title("OCR with Google Vision API")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image_bytes = uploaded_file.getvalue()
        client = get_vision_client()
        text = detect_text(client, image_bytes)
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
        st.write("Detected text:")
        st.write(text)

if __name__ == "__main__":
    main()
