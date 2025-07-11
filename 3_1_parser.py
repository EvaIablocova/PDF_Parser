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

# def find_y_coordinates_from_page(page, black_line_threshold=0.9):
#     y_coordinates = []  # Array to store y-coordinates of horizontal lines
#
#     # Get the page's horizontal lines
#     horizontal_lines = [
#         obj for obj in page.objects.get("rect", [])
#         if obj["width"] > page.width * black_line_threshold and obj["height"] < 2
#     ]
#
#     # Sort lines by their y-coordinates
#     sorted_lines = sorted(horizontal_lines, key=lambda line: line["y1"], reverse=True)
#
#     # Extract y-coordinates
#     # y_coordinates.extend([line["y1"] for line in sorted_lines])
#     y_coordinates.extend(sorted([line["y1"] for line in sorted_lines]))
#
#     return y_coordinates

def extract_y_coordinates_from_page(page):
    y_values = []
    edges = page.edges

    horizontal_lines = [edge for edge in edges if abs(edge['y1'] - edge['y0']) < 1 and edge['x1'] > edge['x0']]
    horizontal_lines = horizontal_lines[::2]

    for line in horizontal_lines:
        y = line['y0']
        y_values.append(round(y))

    return sorted(set(y_values))

def find_start_y (page):
    pattern = r'\d{13}'

    first_row_pattern = re.compile(pattern)
    words = page.extract_words()
    for word in words:
        if first_row_pattern.search(word['text']):
            return word['top']
    return None

def find_last_y (page):
    pattern = r'\d{13}'
    last_y = None

    first_row_pattern = re.compile(pattern)
    words = page.extract_words()
    for word in words:
        if first_row_pattern.search(word['text']):
            last_y = word['top']

    return last_y

def cut_y(y, y0, y_last):
    y = [val - 40 for val in y]

    y_filtered = [val for val in y if y0 < val <= y_last]
    y_not_fit = [val for val in y if y0 > val]
    max_not_fit = max(y_not_fit) if y_not_fit else None
    y_filtered.append(max_not_fit)

    y_not_fit = [val for val in y if val > y_last]
    min_not_fit = min(y_not_fit) if y_not_fit else None

    if not min_not_fit:
        min_not_fit = y_last + 10

    y_filtered.append(round(min_not_fit))


    y_filtered = sorted(y_filtered)

    print(y_filtered)
    return y_filtered

def extract_table_with_black_lines (pdf_url, x, all_data, black_line_threshold=0.9):
    with pdfplumber.open(pdf_url) as pdf:
        for page in pdf.pages:
            # y = find_y_coordinates_from_page(page)

            # y1 = page.height
            # y = [199, 201, 224, 248, 272, 297, 321, 345, 369, 393, 417, 439, 440, 442, 481, 482, 484, 499, 521]

            y = extract_y_coordinates_from_page(page)

            y0 = find_start_y(page)
            y_last = find_last_y(page)
            y = cut_y(y, y0, y_last)

            page_data = read_page(y, x, page)
            all_data.append(page_data)
    return all_data


def parse_pdf(pdf_url, x, search_pattern, parsed_data_file_name):
    all_data = []

    line_tolerance = 2


    if search_pattern == 'no_pattern':

        no_pattern_module.parse_no_pattern(pdf_url, parsed_data_file_name)

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

os.makedirs("parsed_files", exist_ok=True)
parsed_data_file_name = "parsed_files/" + os.path.splitext(os.path.basename(path_to_file))[0] + ".csv"

x = file_config['sizes']
search_pattern = file_config['search_pattern']

parse_pdf(path_to_file, x, search_pattern, parsed_data_file_name)

