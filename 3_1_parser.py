import pandas as pd
from collections import defaultdict
import pdfplumber
import re
import time
import os
import json
import sys
import csv
import importlib
no_pattern_module = importlib.import_module('3_2_no_pattern_parser')
write_to_log_module = importlib.import_module('0_3_write_to_log')
import warnings
from cryptography.utils import CryptographyDeprecationWarning
import shutil


warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

def hyphenate_text(text, page, j, y, i, x, equal_columns_with_dash):

    switch_column = 0
    letterBeforeHyphen = []

    if re.search(r'-\n', text):
        letterBeforeHyphen = re.findall(r'(.)-\n', text)
        if j == equal_columns_with_dash[0]:
            switch_column = equal_columns_with_dash[1]
        elif j == equal_columns_with_dash[1]:
            switch_column = equal_columns_with_dash[0]

        bbox = (x[switch_column], y[i], x[switch_column + 1], y[i + 1])
        cell = page.within_bbox(bbox)
        switched_text = cell.extract_text(x_tolerance=1, y_tolerance=1) if cell else ''

        for symbol in letterBeforeHyphen:
            pattern_with_space = re.escape(symbol) + r'- '
            pattern_no_space = re.escape(symbol) + r'-'
            replace_pattern = re.escape(symbol) + r'-\n'
            if re.search(pattern_with_space, switched_text):
                text = re.sub(replace_pattern, symbol + '- ', text)
                # break
            else:
                if re.search(pattern_no_space, switched_text):
                    text = re.sub(replace_pattern, symbol + '-', text)

    if '\n' in text:
        text = text.replace('\n', ' ')

    return text


def hyphenate_texts(text, page, y, x, j, i, equal_columns_with_dash):
    if '\n' in text and j in equal_columns_with_dash:
        text = hyphenate_text(text, page, j, y, i, x, equal_columns_with_dash)
    else:
        if re.search(r'-\n', text):
            if re.search(r' -\n', text):
                text = re.sub(r'-\n', '- ', text)
            else:
                text = re.sub(r'-\n', '-', text)

        if '\n' in text:
            text = text.replace('\n', ' ')
    return text

def detect_the_diff_in_columns (row_data, page, y, x, i):
    isChanged = False

    for j in range(len(x) - 1):

        bbox = (x[j + 1] - 30, y[i], x[j + 1] + 10, y[i + 1])
        cell = page.within_bbox(bbox)
        textOverlap = cell.extract_text(x_tolerance=1, y_tolerance=1) if cell else ''

        match = re.search(r'-', textOverlap) or re.search(r'"', textOverlap)
        if match:
            substring_with_dash = textOverlap[:match.end()]

            bbox2 = (x[j], y[i], x[j + 1], y[i + 1])
            cell2 = page.within_bbox(bbox2)
            textReal = cell2.extract_text(x_tolerance=1, y_tolerance=1) if cell else ''

            pattern = re.escape(substring_with_dash)
            if not re.search(pattern, textReal):
                substring_no_dash = substring_with_dash[:-1]
                if re.search(substring_no_dash, textReal):
                    textReal = textReal.replace(substring_no_dash, substring_with_dash)
                    isChanged = True
                else:
                    substring_no_dash_newline = substring_no_dash.rstrip(' ') + '\n'
                    if re.search(substring_no_dash_newline, textReal):
                        substring_no_dash_no_sapce = substring_no_dash.rstrip(' ')
                        textReal = textReal.replace(substring_no_dash_no_sapce, substring_with_dash)
                        isChanged = True

            row_data[j] = textReal

    return row_data, isChanged




def row_compare(row_data, page, y, x, i):
    isChanged = False
    bbox = (x[0], y[i], x[len(x)-1], y[i + 1])
    cell = page.within_bbox(bbox)
    textRow = cell.extract_text(x_tolerance=1, y_tolerance=1) if cell else ''

    if sorted(''.join(row_data).replace(' ', '').replace('\n', '')) != sorted(textRow.replace(' ', '').replace('\n', '')):
        row_data, isChanged = detect_the_diff_in_columns (row_data, page, y, x, i)

    return row_data, isChanged

def overlap_row_read(page, y, x, i):
    new_row_data = []

    for j in range(len(x) - 1):
        bbox = (x[j], y[i]-1, x[j + 1], y[i + 1])
        cell = page.within_bbox(bbox)
        text = cell.extract_text(x_tolerance=1, y_tolerance=1) if cell else ''

        new_row_data.append(text)

    return new_row_data


def read_page(y, x, page, all_data, equal_columns_with_dash):

            isChanged = False
            for i in range(len(y) - 1):


                    row_data = []
                    for j in range(len(x) - 1):
                        bbox = (x[j], y[i], x[j + 1], y[i + 1])
                        cell = page.within_bbox(bbox)
                        text = cell.extract_text(x_tolerance=1, y_tolerance=1) if cell else ''

                        text = hyphenate_texts(text, page, y, x, j, i, equal_columns_with_dash)

                        row_data.append(text)

                    row_data, isChanged = row_compare(row_data, page, y, x, i)
                    if isChanged:
                        row_data = [
                            hyphenate_texts(text, page, y, x, j, i, equal_columns_with_dash)
                            for j, text in enumerate(row_data)
                        ]

                    if None in row_data or '' in row_data:
                        row_data = overlap_row_read(page, y, x, i)
                        row_data = [
                            hyphenate_texts(text, page, y, x, j, i, equal_columns_with_dash)
                            for j, text in enumerate(row_data)
                        ]


                    all_data.append(row_data)
            return all_data

def parse_pdf(pdf_url, x, search_pattern, parsed_data_file_name, count_columns, equal_columns_with_dash):
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
                # md_tops = [entry['top'] - 1 for entry in other if md_pattern.search(entry['text'])]
                y = sorted(set(md_tops))
                if y and y[-1] < page.height:
                    y.append(page.height - 40)

                all_data = read_page(y, x, page, all_data, equal_columns_with_dash)




        df = pd.DataFrame(all_data)

        df.to_csv(parsed_data_file_name, sep='|', index=False, header=False)

# MD-2069, str. Calea Iesilor 34, mun. Chisinau, R e p u b l ic a M o l d o v a



file_config = json.loads(os.environ['FILE_CONFIG'])

path_to_file = json.loads(os.environ['path_to_file'])

# file_base = os.path.splitext(os.path.basename(path_to_file))[0]
# file_name = '_'.join(file_base.split('_')[2:]) + ".pdf"

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

parsed_data_dir = config ['parsed_data_dir']

os.makedirs(parsed_data_dir, exist_ok=True)
parsed_data_file_name = parsed_data_dir + "/" + os.path.splitext(os.path.basename(path_to_file))[0] + ".csv"

x = file_config['sizes']
search_pattern = file_config['search_pattern']
count_columns = file_config['count_columns']
equal_columns_with_dash = file_config['equal_columns_with_dash']

write_to_log_module.write_step_message("Py.Parser", f"Parsing file [start] {os.path.splitext(os.path.basename(path_to_file))[0]} ")

try:
    parse_pdf(path_to_file, x, search_pattern, parsed_data_file_name, count_columns, equal_columns_with_dash)

    copy_path = parsed_data_file_name.replace('.csv', '_copy_debug.csv')
    shutil.copy(parsed_data_file_name, copy_path)

    write_to_log_module.write_step_message("Py.Parser", f"Parsing file [done] {os.path.splitext(os.path.basename(path_to_file))[0]} ")
except Exception as e:
    print(f"Error parsing PDF file: {e}")
    write_to_log_module.write_step_message("Py.Parser", f"Parsing file [failed] {os.path.splitext(os.path.basename(path_to_file))[0]} ")
    write_to_log_module.write_step_message("Py.Parser",
                                           f"[ERROR] Finished time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    sys.exit(1)
