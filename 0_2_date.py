import json
import requests
from bs4 import BeautifulSoup

def update_stored_date_in_config_json(file_config, new_date_range):

    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)

    for fc in config['file_configs']:
        if fc['keyword'] == file_config['keyword']:
            fc['stored_date_range'] = new_date_range
            break

    with open('config.json', 'w', encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False, indent=4)

    print(f"Updated in config.json stored date range to: {new_date_range}")

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
                    update_stored_date_in_config_json(file_config, date_range)
                    return True

    print("Date range has not changed.")
    return False