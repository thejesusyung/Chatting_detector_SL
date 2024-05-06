import streamlit as st
import openai
import os
from google.cloud import vision

def get_vision_client():
    """Function to authenticate and return the Google Vision API client."""
    # Initialize the Vision API client (assuming credentials are set up)
    return vision.ImageAnnotatorClient()

def detect_text(image_bytes):
    """Use Google Vision API to extract text from an image."""
    client = get_vision_client()
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image)
    return response.text_annotations[0].description if response.text_annotations else ""

def analyze_with_chatgpt(text):
    """Send text to ChatGPT for analysis to determine if it's a conversation."""
    openai.api_key = os.getenv('OPENAI_API_KEY')  # Ensure your API key is set in environment variables
    response = openai.Completion.create(
        engine="gpt-4-turbo-2024-04-09",  # or the latest model
        prompt=f"What follows is a text extracted from a screenshot of a user. The user sent this screenshot to a dating copilot bot and it is either a dialogue screenshot or not. It could be a screenshot of a person's dating profile page or a photo in which case no text would be exctracted. Only in case that it looks like the following text is a dialogue answer 'That is a dialogue!' In all the other cases answer 'Other!' Here follows the extracted text: {text}",
        max_tokens=100
    )
    return response.choices[0].text.strip()

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
