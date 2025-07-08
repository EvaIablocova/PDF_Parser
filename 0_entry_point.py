import subprocess
import sys
import time
import json
import os
import requests
from bs4 import BeautifulSoup

def check_data_change(file_config):
    url = "https://www.asp.gov.md/ro/date-deschise/avizele-agentilor-economici"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    heading_string = file_config['heading_string']

    heading = soup.find('h4', string=heading_string)
    if not heading:
        print(f"Heading {heading_string} not found on the page.")
        return False

    table = heading.find_next('table', class_='table')
    if not table:
        print(f"Table not found under the heading {heading_string}.")
        return False

    row_in_table = file_config['row_in_table']
    rows = table.find_all('tr')
    for index, row in enumerate(rows):
        if index == row_in_table:
            cells = row.find_all('td')
            if len(cells) >= 2:
                date_range = cells[1].text.strip()
                stored_date_range = file_config['stored_date_range']
                if date_range != stored_date_range:
                    print(f"Date range has changed: {date_range}")
                    return True

    print("Date range has not changed.")
    return False




keyword = "Denumirea_2008_2024"

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

file_config = next((fc for fc in config['file_configs'] if fc['keyword'] == keyword), None)
os.environ['FILE_CONFIG'] = json.dumps(file_config)

subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirments"])

is_data_changed = check_data_change(file_config)

if not is_data_changed:
    print("Data has not changed, skipping the pipeline.")
    sys.exit(0)
else:
    print("Data has changed, proceeding with the pipeline.")


scripts = [
    "1_download_pdf.py",
    "2_parser.py",
    "3_clean.py",
    "4_validation.py",
    "5_load_sql.py"
]

for script in scripts:
    print(f"Running {script}...")
    start_time = time.time()
    result = subprocess.run([sys.executable, script, keyword], env=os.environ)
    elapsed = time.time() - start_time
    if result.returncode != 0:
        print(f"Script {script} failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    print(f"{script} finished successfully in {elapsed:.2f} seconds.\n")


