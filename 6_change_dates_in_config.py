import os
import json
import re
import importlib
import time
import sys
date_module = importlib.import_module('0_2_date')
write_to_log_module = importlib.import_module('0_3_write_to_log')

try:
    path_to_file = json.loads(os.environ['path_to_file'])

    file_base = os.path.splitext(os.path.basename(path_to_file))[0]
    timestamp_pattern = r'\d{8}_\d{4}'

    if not re.search(timestamp_pattern, file_base):
        file_name = file_base  + ".pdf"
    else:
        file_name = '_'.join(file_base.split('_')[2:]) + ".pdf"



    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)

    config_last_dates_in_db = config['config_last_dates_in_db']
    today_file = config['today_file']

    date_module.update_stored_date_in_config_json(file_name, config_last_dates_in_db, today_file)
except Exception as e:
    print (f"Error updating dates in config file: {e}")
    write_to_log_module.write_step_message("Py.Staging", f"Changing dates in config file [failed] {os.path.splitext(os.path.basename(path_to_file))[0]} ")
    write_to_log_module.write_step_message("Py.Parser",
                                           f"[ERROR] Finished time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

    sys.exit(1)