import openai
import os
import json
import base64
from google.oauth2 import service_account
from google.cloud import vision
import streamlit as st
from groq import Groq
import time  # Import the time module
import cohere
from cohere.responses.classify import Example
from semantic_router import Route
import os
from semantic_router.encoders import CohereEncoder
from semantic_router.layer import RouteLayer

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



# Initialize the Cohere client
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Define examples that represent different intents
examples = [
    Example("У вас есть рекомендации для романтического ужина?", "Рекомендации ресторанов"),
    Example("Можно ли привести собаку в кафе?", "Политика относительно животных"),
    Example("Будет ли сегодня вечером живая музыка?", "Мероприятия и развлечения"),
    Example("Во сколько закрывается кухня?", "Часы работы"),
    Example("У вас есть безглютеновые опции?", "Информация о меню")
]
option_1 = Route(
    name="Опция один",
    utterances=[
        "У вас есть рекомендации для романтического ужина?",
        "Можно ли привести собаку в кафе?",
        "Будет ли сегодня вечером живая музыка?",
        ],
)
option_2 = Route(
    name="Опция два",
    utterances=[
        "Во сколько закрывается кухня?",
        "У вас есть безглютеновые опции?",
        ],
)
routes = [option_1, option_2]
encoder = CohereEncoder()
rl = RouteLayer(encoder=encoder, routes=routes)

def analyze_with_chatgpt(text):
    rl(text).name

def analyze_with_chatgpt_2(text):
    """Send text to Cohere for classification to determine its intent based on predefined examples."""
    try:
        response = co.classify(
            model='medium',
            inputs=[text],
            examples=examples,
        )
        return response.classifications[0].prediction
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error in intent classification"

def main():
    st.title("Image Conversation Detector")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
   
    if uploaded_file is not None:
        with st.spinner('Extracting text and analyzing...'):
            start_time = time.time()  # Start the timer
            text_content = detect_text(uploaded_file.getvalue())
            text_extraction_time = time.time() - start_time  # Calculate text extraction time
            
            if text_content:
                st.text_area("Extracted Text", text_content, height=150)
                start_time = time.time()  # Reset the timer for analysis
                analysis_result = analyze_with_chatgpt(text_content)
                analysis_time = time.time() - start_time  # Calculate analysis time
                st.write("Analysis Result:")
                st.write(analysis_result)
                st.write(f"Text extraction time: {text_extraction_time:.2f} seconds")
                st.write(f"Analysis time: {analysis_time:.2f} seconds")
            else:
                st.write("No detectable text found in the image.")
                st.write(f"Text extraction time: {text_extraction_time:.2f} seconds")

if __name__ == "__main__":
    main()
