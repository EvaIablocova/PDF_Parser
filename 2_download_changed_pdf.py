import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
import json

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

source_url = config['source_url']

download_dir = sys.argv[1]
os.makedirs(download_dir, exist_ok=True)

files_to_process_str = sys.argv[2:]

response = requests.get(source_url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a")

for link in links:
    href = link.get("href")
    if href and href.lower().endswith(".pdf"):
        file_url = urljoin(source_url, href)
        file_name = os.path.split(file_url)[-1]

        if file_name in files_to_process_str:
            file_path = os.path.join(download_dir, file_name)

            try:
                file_response = requests.get(file_url)
                file_response.raise_for_status()
                with open(file_path, "wb") as file:
                    file.write(file_response.content)
                print(f"Downloaded: {file_name}")
            except Exception as e:
                print(f"Failed to download {file_url}: {e}")