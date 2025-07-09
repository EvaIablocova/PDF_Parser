import json
from PyPDF2 import PdfReader
import re
from datetime import datetime

def update_stored_date_in_config_json(differences, config_dates):

    with open(config_dates, "r", encoding="utf-8") as f:
        config_data = json.load(f)

    config_dict = {item["FileName"]: item for item in config_data}

    for diff in differences:
        file_name = diff["FileName"]
        if file_name in config_dict:
            config_dict[file_name]["start_date"] = diff["today_start_date"]
            config_dict[file_name]["end_date"] = diff["today_end_date"]

    with open(config_dates, "w", encoding="utf-8") as f:
        json.dump(list(config_dict.values()), f, ensure_ascii=False, indent=4)

    print("Dates updated in config_last_dates_in_db.json")



def compare_dates(config_dates, today_file):

    with open(config_dates, "r", encoding="utf-8") as f:
        config_data = json.load(f)
    with open(today_file, "r", encoding="utf-8") as f:
        today_data = json.load(f)


    config_dict = {item["FileName"]: item for item in config_data}
    today_dict = {item["FileName"]: item for item in today_data}


    differences = []
    for file_name, today_item in today_dict.items():
        config_item = config_dict.get(file_name)
        if config_item:
            if (today_item["start_date"] != config_item["start_date"] or
                today_item["end_date"] != config_item["end_date"]):
                differences.append({
                    "FileName": file_name,
                    "config_start_date": config_item["start_date"],
                    "config_end_date": config_item["end_date"],
                    "today_start_date": today_item["start_date"],
                    "today_end_date": today_item["end_date"]
                })
        else:
            differences.append({
                "FileName": file_name,
                "config_start_date": "Not Found",
                "config_end_date": "Not Found",
                "today_start_date": today_item["start_date"],
                "today_end_date": today_item["end_date"]
            })

    files_to_process = []

    if differences:
        files_to_process = [diff["FileName"] for diff in differences]
        update_stored_date_in_config_json (differences, config_dates)

    return files_to_process



