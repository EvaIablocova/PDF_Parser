import requests
import json
import os

file_config = json.loads(os.environ['FILE_CONFIG'])

url = file_config['url_to_download_from']
goal_file = file_config['pdf_file_name']

response = requests.get(url)

with open(goal_file, 'wb') as f:
    f.write(response.content)