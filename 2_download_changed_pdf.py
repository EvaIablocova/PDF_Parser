import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
import json
from datetime import datetime
import importlib
write_to_log_module = importlib.import_module('0_3_write_to_log')
slack_module = importlib.import_module('0_4_slack_module')


def download_changed_pdfs(download_dir, files_to_process_str):

        with open('config.json', 'r', encoding='utf-8') as file:
            config = json.load(file)

        source_url = config['source_url']

        os.makedirs(download_dir, exist_ok=True)

        files_to_process = files_to_process_str.split(',')
        files_to_process_downloaded = []

        response = requests.get(source_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.find_all("a")


        count = 0
        for link in links:
            href = link.get("href")
            if href and href.lower().endswith(".pdf"):
                file_url = urljoin(source_url, href)
                file_name = os.path.split(file_url)[-1]

                if file_name in files_to_process:
                    file_name = datetime.now().strftime('%Y%m%d_%H%M') + "_" + \
                                            os.path.splitext(os.path.basename(file_name))[0] + ".pdf"

                    file_path = os.path.join(download_dir, file_name)

                    try:
                        file_response = requests.get(file_url)
                        file_response.raise_for_status()
                        with open(file_path, "wb") as file:
                            file.write(file_response.content)
                        print(f"Downloaded: {file_name}")
                        files_to_process_downloaded.append(file_name)
                        count += 1
                    except Exception as e:
                        print(f"Failed to download {file_url}: {e}")
                        write_to_log_module.write_step_message("Py.Loader",
                                                               f"Downloading file from site [failed] {os.path.splitext(os.path.basename(file_url))[0]}")

                        slack_module.send_slack_message(
                            f"-------------[ERROR]--------------------\n Failed to download {file_url}: {e}")

        return count, files_to_process_downloaded


