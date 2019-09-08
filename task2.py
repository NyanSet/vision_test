import logging
import os
import requests

from argparse import ArgumentParser


server_url = 'http://0.0.0.0/images'
success_statuses = (200, 201, 202)
img_ext = ('.jpg', '.png')
log_file = 'upload.log'

parser = ArgumentParser()
parser.add_argument('--path', default=os.getcwd(), type=str)
img_dir = parser.parse_args().path
if not os.path.isdir(img_dir):
    exit(f"'{img_dir}' is not a valid directory.")

logging.basicConfig(filename=os.path.join(img_dir, log_file), filemode='a', level=logging.INFO,
                    format='%(asctime)s,%(msecs)d;%(levelname)s;%(message)s')

images = [f for f in os.listdir(img_dir) if f.endswith(img_ext)]
for image in images:
    img_bytes = open(os.path.join(img_dir, image), 'rb').read()
    try:
        resp = requests.post(server_url, data=img_bytes, headers={'Content-Type': 'application/octet-stream'})
    except requests.exceptions.RequestException as e:
        logging.error(f'{image};{e.__class__.__name__} exception uploading the file.')
        continue
    if resp.status_code in success_statuses:
        logging.info(f'{image};Successfully uploaded the file.')
    else:
        logging.warning(f'{image};Failed to upload the file, the server returned code {resp.status_code}.')
