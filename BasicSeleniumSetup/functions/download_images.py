import logging
import os


def download_images(url, folder_name, image_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            with open(os.path.join(folder_name, image_name), 'wb') as f:
                f.write(response.content)
    except Exception:
        logging.exception('Error downloading images')
