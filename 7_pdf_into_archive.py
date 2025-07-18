import pyodbc
import csv
import json
import os
from datetime import datetime
import shutil

file_config = json.loads(os.environ['FILE_CONFIG'])

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

archive_dir = config['archive_dir']
os.makedirs(archive_dir, exist_ok=True)

path_to_file = json.loads(os.environ['path_to_file'])

archive_pdf_file_name = datetime.now().strftime('%Y%m%d_%H%M') + "_" + os.path.splitext(os.path.basename(path_to_file))[0] + ".pdf"

shutil.move(path_to_file, os.path.join(archive_dir, archive_pdf_file_name))

print(f"PDF file {path_to_file} has been exported to {archive_dir}/ {archive_pdf_file_name}.")
