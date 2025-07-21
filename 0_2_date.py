import json
import re
from datetime import datetime

def update_stored_date_in_config_json(file_name, config_dates, today_file):

    with open(today_file, "r", encoding="utf-8") as f:
        today_data = json.load(f)

    today_entry = next((item for item in today_data if item["FileName"] == file_name), None)
    if not today_entry:
        raise ValueError(f"FileName '{file_name}' not found in {today_file}")

    with open(config_dates, "r", encoding="utf-8") as f:
        config_data = json.load(f)

    all_config_names = {item["FileName"]: item for item in config_data}

    if file_name in all_config_names:
            all_config_names[file_name]["start_date"] = today_entry["start_date"]
            all_config_names[file_name]["end_date"] = today_entry["end_date"]
    else:
            all_config_names[file_name] = {
                "FileName": file_name,
                "start_date": today_entry["start_date"],
                "end_date": today_entry["end_date"]
            }

    with open(config_dates, "w", encoding="utf-8") as f:
        json.dump(list(all_config_names.values()), f, ensure_ascii=False, indent=4)

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
    date_from = ''
    date_into = ''

    if differences:
        files_to_process = [diff["FileName"] for diff in differences]
        date_from = differences[0]["config_start_date"] + ' - ' + differences[0]["config_end_date"]
        date_into = differences[0]["today_start_date"] + ' - ' + differences[0]["today_end_date"]

    return files_to_process, date_from, date_into



