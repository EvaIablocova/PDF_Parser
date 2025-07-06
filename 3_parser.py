import pandas as pd
from collections import defaultdict
import pdfplumber
import re
import time


def read_excel_column_sizes(column_sizes_file):
    step1_start = time.time()

    if re.search(r'Denumirea', pdf_url):
        df_xlsx = pd.read_excel(column_sizes_file, header=None)
        row = df_xlsx[df_xlsx[0] == 'Denumirea']
        if not row.empty:
            x = row.iloc[0, 1:].tolist()
            step1_duration = time.time() - step1_start
            print(f"Step 1 (Read Excel file): {step1_duration:.2f} seconds")
            return x
        else:
            raise ValueError("No column sizes for 'Denumirea' found in column_sizes.xlsx")


def process_pdf(pdf_url, x):
    step2_start = time.time()
    all_data = []

    line_tolerance = 2
    md_pattern = re.compile(r'MD-\d{4}')

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

            md_tops = [entry['top'] - 2 for entry in other if md_pattern.search(entry['text'])]
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

def parse_pdf(pdf_url, column_sizes_file):

    # Step 1: Read Excel file for column sizes
    x = read_excel_column_sizes (column_sizes_file)

    # Step 2: Process PDF
    all_data = []
    all_data= process_pdf(pdf_url, x)

    # Step 3: Set the 3320th row
    step3_start = time.time()

    if len(all_data) >3320:
        all_data[3319] = [
            '3320',
            '07.08.2014',
            '1005603002522',
            'Întreprinderea Mixtă ""VINAGROFOROS"" S.R.L.',
            'MD-7320, s. Cîşla, r-l Cantemir, Republica Moldova',
            'INTREPRINDEREA MIXTA ""VINAGROFOROS"" SRL',
            'Întreprinderea Mixtă ""VINAGROFOROS"" S.R.L.'
        ]

    step3_duration = time.time() - step3_start
    print(f"Step 3 (Set 3320th row): {step3_duration:.2f} seconds")

    # Step 4: Create DataFrame
    step4_start = time.time()
    df = pd.DataFrame(all_data)
    step4_duration = time.time() - step4_start
    print(f"Step 4 (Create DataFrame): {step4_duration:.2f} seconds")

    return df

start_time = time.time()
pdf_url = "Denumirea_2008_2024.pdf"
column_sizes_file = "column_sizes.xlsx"
df = parse_pdf(pdf_url, column_sizes_file)
df.to_csv('table_extracted.csv', sep='|', index=False, header=False)

total_duration = time.time() - start_time
print(f"Total execution time: {total_duration:.2f} seconds")