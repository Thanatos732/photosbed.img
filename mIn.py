import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_image(url, folder_path, headers):
    filename = url.split("/")[-1]
    filepath = os.path.join(folder_path, filename)
    with open(filepath, 'wb') as f:
        response = requests.get(url, headers=headers)
        f.write(response.content)
    print(f"Downloaded: {filename}")

def scrape_pixiv_daily_top_100(save_folder):
    # URL of Pixiv daily ranking
    url = 'https://www.pixiv.net/ranking.php?mode=daily&content=illust'
    
    # Send a GET request to the URL
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all image elements
    image_elements = soup.find_all('img', class_='_thumbnail ui-scroll-view')
    
    # Create the save folder if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    # Download and save each image
    for i, img in enumerate(image_elements, 1):
        img_url = img['data-src']
        img_url = img_url.replace('/c/240x480/img-master/', '/img-original/') # Modify image URL to get full resolution
        img_url = img_url.replace('_master1200', '') # Remove resolution suffix
        img_url = img_url.replace('img-original', 'img-master') # Modify URL to get the master quality
        img_url = img_url.replace('.jpg', '_p0_master1200.jpg') # Ensure highest resolution
        
        img_url = urljoin(url, img_url)
        
        download_image(img_url, save_folder, headers)

        # Stop after downloading the top 100 images
        if i == 100:
            break

if __name__ == "__main__":
    save_folder = "E:/pixiv_images"
    scrape_pixiv_daily_top_100(save_folder)
