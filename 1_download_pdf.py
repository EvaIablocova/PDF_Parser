import requests
import json
import os

file_config = json.loads(os.environ['FILE_CONFIG'])

url = "https://www.asp.gov.md/sites/default/files/date-deschise/avizele-agentilor-economici/total/Sediul_2008_2024.pdf"
goal_file = "Sediul_2008_2024.pdf"

response = requests.get(url)

with open(goal_file, 'wb') as f:
    f.write(response.content)