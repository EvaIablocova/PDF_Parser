import pyodbc
import csv
import json
import os
from datetime import datetime
import shutil
import importlib
write_to_log_module = importlib.import_module('0_3_write_to_log')

try:
    file_config = json.loads(os.environ['FILE_CONFIG'])

    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)

    archive_dir = config['archive_dir']
    os.makedirs(archive_dir, exist_ok=True)

    path_to_file = json.loads(os.environ['path_to_file'])

    archive_pdf_file_name = os.path.splitext(os.path.basename(path_to_file))[0] + "_" + datetime.now().strftime('%Y%m%d%H%M') + ".pdf"

    shutil.copy(path_to_file, os.path.join(archive_dir, archive_pdf_file_name))

    print(f"PDF file {path_to_file} has been exported to {archive_dir}/ {archive_pdf_file_name}.")
except Exception as e:
    write_to_log_module.write_step_message("Py.Staging", f"Loading into archive file [failed] {os.path.splitext(os.path.basename(path_to_file))[0]} ")
    raise
