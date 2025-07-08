import pandas as pd
from collections import defaultdict
import pdfplumber
import re
import time
import os
import json

def process_pdf(pdf_url, x, search_pattern):
    step2_start = time.time()
    all_data = []

    line_tolerance = 2
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
    step2_duration = time.time() - step2_start
    print(f"Step 2 (Process PDF): {step2_duration:.2f} seconds")
    return all_data

def parse_pdf(pdf_url, x, search_pattern):

    all_data = []
    all_data= process_pdf(pdf_url, x, search_pattern)


    # Step 4: Create DataFrame
    step4_start = time.time()
    df = pd.DataFrame(all_data)
    step4_duration = time.time() - step4_start
    print(f"Step 4 (Create DataFrame): {step4_duration:.2f} seconds")

    return df


file_config = json.loads(os.environ['FILE_CONFIG'])

pdf_url = file_config['pdf_file_name']
parsed_data_file_name = file_config['parsed_data_file_name']
x = file_config['sizes']
search_pattern = file_config['search_pattern']

df = parse_pdf(pdf_url, x, search_pattern)

df.to_csv(parsed_data_file_name, sep='|', index=False, header=False)