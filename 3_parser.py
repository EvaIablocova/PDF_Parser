import pandas as pd
from collections import defaultdict
import pdfplumber
import re

def parse_pdf(pdf_url, column_sizes_file):

    line_tolerance = 2
    md_pattern = re.compile(r'MD-\d{4}')

    if re.search(r'Denumirea', pdf_url):
        df_xlsx = pd.read_excel(column_sizes_file, header=None)
        row = df_xlsx[df_xlsx[0] == 'Denumirea']
        if not row.empty:
            x = row.iloc[0, 1:].tolist()
        else:
            raise ValueError("No column sizes for 'Denumirea' found in column_sizes.xlsx")

    all_data = []

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
                    if text:
                        text = re.sub(r'-(\n)', '-', text)
                        text = text.replace('\n', ' ')
                    else:
                        text = ''
                    row_data.append(text)
                all_data.append(row_data)

    # Set the 3320th row (index 3319)
    all_data[3319] = [
        '3320',
        '07.08.2014',
        '1005603002522',
        'Întreprinderea Mixtă ""VINAGROFOROS"" S.R.L.',
        'MD-7320, s. Cîşla, r-l Cantemir, Republica Moldova',
        'INTREPRINDEREA MIXTA ""VINAGROFOROS"" SRL',
        'Întreprinderea Mixtă ""VINAGROFOROS"" S.R.L.'
    ]

    df = pd.DataFrame(all_data)
    return df

pdf_url = "Denumirea_2008_2024.pdf"
column_sizes_file = "column_sizes.xlsx"
df = parse_pdf(pdf_url, column_sizes_file)
df.to_csv('table_extracted.csv', sep='|', index=False, header=False)