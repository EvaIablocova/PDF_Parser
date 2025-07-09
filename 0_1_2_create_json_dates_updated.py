import os
import re
import json
from datetime import datetime
from PyPDF2 import PdfReader
import sys

download_dir = sys.argv[1]
today_file = sys.argv[2]

# Initialize a list to store the data
data = []

# Process each PDF file in the folder
for file_name in os.listdir(download_dir):
    if file_name.lower().endswith(".pdf"):
        file_path = os.path.join(download_dir, file_name)
        try:
            # Read the PDF file
            reader = PdfReader(file_path)
            text = ""
            if len(reader.pages) > 0:
                text = reader.pages[0].extract_text()

            date_pattern = r'(\d{2}\.\d{2}\.\d{4})\s*-\s*(\d{2}\.\d{2}\.\d{4})'
            date_match = re.search(date_pattern, text)

            if date_match:
                start_date = date_match.group(1)
                end_date = date_match.group(2)
                start_date = datetime.strptime(start_date, "%d.%m.%Y").strftime("%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%d.%m.%Y").strftime("%Y-%m-%d")
            else:
                start_date = end_date = "Not Found"

            # Append data to the list
            data.append({"FileName": file_name, "start_date": start_date, "end_date": end_date})
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
            data.append({"FileName": file_name, "start_date": "Error", "end_date": "Error"})

# Save the data to a JSON file
with open(today_file, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print(f"Data written to {today_file}")