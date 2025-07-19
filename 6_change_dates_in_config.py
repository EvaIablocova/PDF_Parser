import os
import json
import importlib
date_module = importlib.import_module('0_2_date')
write_to_log_module = importlib.import_module('0_3_write_to_log')

try:
    path_to_file = json.loads(os.environ['path_to_file'])
    file_base = os.path.splitext(os.path.basename(path_to_file))[0]
    file_name = '_'.join(file_base.split('_')[2:]) + ".pdf"


    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)

    config_last_dates_in_db = config['config_last_dates_in_db']
    today_file = config['today_file']

    date_module.update_stored_date_in_config_json(file_name, config_last_dates_in_db, today_file)
except Exception as e:
    write_to_log_module.write_step_message("Py.Staging", f"Changing dates in config file [failed] {os.path.splitext(os.path.basename(path_to_file))[0]} ")
    raise