import openai
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

def detect_text(image_bytes):
    """Use Google Vision API to extract text from an image."""
    client = get_vision_client()
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image)
    return response.text_annotations[0].description if response.text_annotations else ""

def analyze_with_chatgpt(text):
    """Send text to ChatGPT for analysis to determine if it's a conversation."""
    openai.api_key = os.getenv('OPENAI_API_KEY')  # Ensure your API key is set in environment variables
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # Use the appropriate model name
        messages=[{"role": "system", "content": "What follows is a text extracted from a screenshot of a user. The user sent this screenshot to a dating copilot bot and it is either a dialogue screenshot or not. It could be a screenshot of a person's dating profile page or a photo in which case no text would be exctracted. Only in case that it looks like the following text is a dialogue answer 'That is a dialogue!' In all the other cases answer 'Other!' Here follows the extracted text:"},
                  {"role": "user", "content": text}]
    )
    return response['choices'][0]['message']['content']


def main():
    st.title("Image Conversation Detector")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        with st.spinner('Extracting text and analyzing...'):
            text_content = detect_text(uploaded_file.getvalue())
            if text_content:
                st.text_area("Extracted Text", text_content, height=150)
                analysis_result = analyze_with_chatgpt(text_content)
                st.write("Analysis Result:")
                st.write(analysis_result)
            else:
                st.write("No detectable text found in the image.")

if __name__ == "__main__":
    main()
