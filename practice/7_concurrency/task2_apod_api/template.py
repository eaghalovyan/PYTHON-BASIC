from concurrent.futures import ThreadPoolExecutor
import requests
import os
from pprint import pprint


API_KEY = "dFCjoKdiP1PpTFB7jg7vHeVS2msW9Fuv6vt2Qwg7"
APOD_ENDPOINT = 'https://api.nasa.gov/planetary/apod'
OUTPUT_IMAGES = './output'


def get_apod_metadata(start_date: str, end_date: str, api_key: str) -> list:
    params = {
        'api_key': api_key,
        'start_date': start_date,
        'end_date': end_date
    }   
    print(f"Requesting metadata from {start_date} to {end_date}...")
    response = requests.get(APOD_ENDPOINT, params = params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get metadata: {response.status_code}")
        return []  

def download_single_image(item: dict):
    if item.get("media_type") != "image":
        return
    
    date = item.get("date")
    image_url = item.get("url")
    if not image_url:
        return
    
    ext = os.path.splitext(image_url)[1]
    filename = f"{date}{ext}"
    file_path = os.path.join(OUTPUT_IMAGES, filename)

    try:
        img_response = requests.get(image_url, stream = True, timeout=15)
        img_response.raise_for_status()

        with open(file_path, "wb") as f:
            for chunk in img_response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Failed to download {date}: {e}")


def download_apod_images(metadata: list):
    if not metadata:
        print("No images found in the specified range.")
        return
    
    os.makedirs(OUTPUT_IMAGES, exist_ok=True)
    print(f"Starting parallel download of {len(metadata)} items...")

    with ThreadPoolExecutor(max_workers=15) as executor:
        executor.map(download_single_image, metadata)

def main():
    metadata = get_apod_metadata(
        start_date='2021-08-01',
        end_date='2021-09-30',
        api_key=API_KEY,
    )
    download_apod_images(metadata)

if __name__ == '__main__':
    main()
