import pandas as pd
from collections import defaultdict
import pdfplumber
import re
import time
import os
import json
import csv
import importlib
no_pattern_module = importlib.import_module('3_2_no_pattern_parser')
write_to_log_module = importlib.import_module('0_3_write_to_log')
import warnings
from cryptography.utils import CryptographyDeprecationWarning

warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)


# def read_page(y, x, page):
#     page_data = []
#     for i in range(len(y) - 1):
#         row_data = []  # Collect data for a single row
#         for j in range(len(x) - 1):
#             bbox = (x[j], y[i], x[j + 1], y[i + 1])
#             cell = page.within_bbox(bbox)
#             text = cell.extract_text(x_tolerance=1, y_tolerance=1) if cell else ''
#             if '\n' in text:
#                 text = re.sub(r'-(\n)', '-', text)
#                 text = text.replace('\n', ' ')
#             row_data.append(text)  # Append text without adding quotes
#         page_data.append('|'.join(row_data))  # Join row data with '|'
#     return '\n'.join(page_data)  # Join all rows with a newline

def read_page(y, x, page, all_data):
            for i in range(len(y) - 1):
                    row_data = []
                    for j in range(len(x) - 1):
                        bbox = (x[j], y[i], x[j + 1], y[i + 1])
                        cell = page.within_bbox(bbox)
                        text = cell.extract_text(x_tolerance=1, y_tolerance=1) if cell else ''
                        if '\n' in text:
                            text = re.sub(r'-(\n)', '-', text)
                            text = text.replace('\n', ' ')
                        row_data.append(text)
                    all_data.append(row_data)
            return all_data

def parse_pdf(pdf_url, x, search_pattern, parsed_data_file_name, count_columns):
    all_data = []

    line_tolerance = 2


    if search_pattern == 'no_pattern':

        no_pattern_module.parse_no_pattern(pdf_url, parsed_data_file_name, count_columns)

    else:
        md_pattern = re.compile(search_pattern)

        with pdfplumber.open(pdf_url) as pdf:
            for page in pdf.pages:
                words = page.extract_words()
                lines = defaultdict(list)
                for word in words:
                    top = round(word['top'] / line_tolerance) * line_tolerance
                    lines[top].append(word)

                other = []
                for top in sorted(lines.keys()):
                    line_words = sorted(lines[top], key=lambda w: w['x0'])
                    text_line = " ".join(word['text'] for word in line_words)
                    other.append({'top': top, 'text': text_line})

                md_tops = [entry['top'] - 1 for entry in other if md_pattern.search(entry['text'])]
                y = sorted(set(md_tops))
                if y and y[-1] < page.height:
                    y.append(page.height - 40)

                all_data = read_page(y, x, page, all_data)


        df = pd.DataFrame(all_data)

        df.to_csv(parsed_data_file_name, sep='|', index=False, header=False)





file_config = json.loads(os.environ['FILE_CONFIG'])

path_to_file = json.loads(os.environ['path_to_file'])

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

parsed_data_dir = config ['parsed_data_dir']

os.makedirs(parsed_data_dir, exist_ok=True)
parsed_data_file_name = parsed_data_dir + "/" + os.path.splitext(os.path.basename(path_to_file))[0] + ".csv"

x = file_config['sizes']
search_pattern = file_config['search_pattern']
count_columns = file_config['count_columns']

write_to_log_module.write_step_message("Py.Parser", f"Parsing file [start] {os.path.splitext(os.path.basename(path_to_file))[0]} ")

try:
    parse_pdf(path_to_file, x, search_pattern, parsed_data_file_name, count_columns)

    write_to_log_module.write_step_message("Py.Parser", f"Parsing file [done] {os.path.splitext(os.path.basename(path_to_file))[0]} ")
except Exception as e:
    write_to_log_module.write_step_message("Py.Parser", f"Parsing file [failed] {os.path.splitext(os.path.basename(path_to_file))[0]} ")
    raise