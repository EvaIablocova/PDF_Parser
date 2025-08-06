import json
import os
from datetime import datetime
import shutil
import re
import importlib
import sys
import time
write_to_log_module = importlib.import_module('0_3_write_to_log')
slack_module = importlib.import_module('0_4_slack_module')

try:
    file_config = json.loads(os.environ['FILE_CONFIG'])

    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)

    archive_dir = config['archive_dir']
    os.makedirs(archive_dir, exist_ok=True)

    path_to_file = json.loads(os.environ['path_to_file'])

    file_base = os.path.splitext(os.path.basename(path_to_file))[0]
    timestamp_pattern = r'\d{8}_\d{4}'

    if not re.search(timestamp_pattern, file_base):
            archive_pdf_file_name = datetime.now().strftime('%Y%m%d_%H%M') + "_" + file_base + ".pdf"
    else:
            archive_pdf_file_name = file_base + ".pdf"

    shutil.move(path_to_file, os.path.join(archive_dir, archive_pdf_file_name))

    print(f"PDF file {path_to_file} has been exported to {archive_dir}/ {archive_pdf_file_name}.")
except Exception as e:
    print(f"Error archiving data: {e}")
    write_to_log_module.write_step_message("Py.Staging", f"Staging file [failed] {os.path.splitext(os.path.basename(path_to_file))[0]} ")
    write_to_log_module.write_step_message("Py.Staging",
                                           f"[ERROR] Finished time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    slack_module.send_slack_message(
        f"-------------[ERROR]--------------------\n Error archiving data: {e}")

    sys.exit(1)
