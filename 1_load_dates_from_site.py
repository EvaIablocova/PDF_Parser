import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
from datetime import datetime
import sys

url = "https://www.asp.gov.md/ro/date-deschise/avizele-agentilor-economici"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

rows = soup.select("table.table tbody tr")

result = []

for row in rows:
    cells = row.find_all("td")

    if len(cells) < 3:
        continue

    date_column = row.find_all("td")[1].get_text(strip=True)
    try:
        start_date, end_date = date_column.split(" - ")
    except ValueError:
        continue

    start_date = datetime.strptime(start_date, "%d.%m.%Y").strftime("%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%d.%m.%Y").strftime("%Y-%m-%d")

    # Extract the third column (link)
    link_tag = row.find_all("td")[2].find("a", href=True)
    if not link_tag:
        continue


    last_part = urlparse(link_tag["href"]).path.split("/")[-1]


    record = {
        "FileName": last_part,
        "start_date": start_date.strip(),
        "end_date": end_date.strip()
    }
    result.append(record)


today_file = sys.argv[1]

with open(today_file, "w", encoding="utf-8") as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)