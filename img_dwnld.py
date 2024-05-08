import requests
from bs4 import BeautifulSoup
import os

def download_images(url, folder):
    # Create a directory to save images
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Get HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all image tags
    images = soup.find_all('img')
    
    for img in images:
        # Get image source URL
        src = img.get('src')
        # Ensure src is not None and starts with http (to skip data URIs or JavaScript)
        if src and src.startswith('http'):
            # Get the image content
            img_response = requests.get(src, stream=True)
            if img_response.status_code == 200:
                # Write image content to file
                img_path = os.path.join(folder, src.split('/')[-1])
                with open(img_path, 'wb') as f:
                    for chunk in img_response.iter_content(chunk_size=8192):
                        f.write(chunk)

# Usage

download_images('https://seminar-beauty.ru/foto/kak-poznakomitsya-s-devushkoj-esli-ty-borodatyj-88-foto.html', 'downloaded_images')
