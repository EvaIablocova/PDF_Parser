import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys

url = "https://www.asp.gov.md/ro/date-deschise/avizele-agentilor-economici"

download_dir = sys.argv[1]
os.makedirs(download_dir, exist_ok=True)

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a")

for link in links:
    href = link.get("href")
    if href and href.lower().endswith(".pdf"):
        file_url = urljoin(url, href)
        file_name = os.path.split(file_url)[-1]
        file_path = os.path.join(download_dir, file_name)

        try:
            file_response = requests.get(file_url)
            file_response.raise_for_status()
            with open(file_path, "wb") as file:
                file.write(file_response.content)
            print(f"Downloaded: {file_name}")
        except Exception as e:
            print(f"Failed to download {file_url}: {e}")