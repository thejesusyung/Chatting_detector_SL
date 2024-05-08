import os
import pandas as pd
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv

def translate_text(text, target='en'):
    """Translate text into the target language."""
    translate_client = translate.Client()
    translated_texts = []
    # Check the size of the text; if large, split into smaller chunks
    text_chunks = [text[i:i+5000] for i in range(0, len(text), 5000)]  # Each chunk has a maximum size of 5000 characters
    for chunk in text_chunks:
        result = translate_client.translate(chunk, target_language=target)
        translated_texts.append(result['translatedText'])
    return ' '.join(translated_texts)

def process_file(file_path, target_lang='en'):
    # Initialize a DataFrame to store original and translated texts
    df = pd.DataFrame(columns=['Original Text', 'Translated Text'])

    # Read and process the file in chunks
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = []
        for line in file:
            if line.strip():  # Ensure we don't read empty lines
                lines.append(line.strip())
            if len(lines) == 30:  # Process in chunks of 30 lines
                original_text = ' '.join(lines)
                translated_text = translate_text(original_text, target=target_lang)
                # Using concat instead of append
                new_row = pd.DataFrame({'Original Text': [original_text], 'Translated Text': [translated_text]})
                df = pd.concat([df, new_row], ignore_index=True)
                lines = []  # Reset lines for the next chunk

        # Process any remaining lines if not exactly divisible by 30
        if lines:
            original_text = ' '.join(lines)
            translated_text = translate_text(original_text, target=target_lang)
            new_row = pd.DataFrame({'Original Text': [original_text], 'Translated Text': [translated_text]})
            df = pd.concat([df, new_row], ignore_index=True)

    # Output the DataFrame to a CSV file
    df.to_csv('translated_output.csv', index=False)

# Usage example
load_dotenv()
process_file('romance.txt', 'ru')  # Adjust path and target language as needed
