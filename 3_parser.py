import pandas as pd
from collections import defaultdict
import pdfplumber
import re

def replace_a(df):
    diff_mask = df[3] != df[6]

    for idx in df[diff_mask].index:
        col4 = df.at[idx, 3]
        col7 = df.at[idx, 6]
        # Find positions where characters differ
        if len(col4) == len(col7):
            new_col7 = list(col7)
            changed = False
            for i, (c4, c7) in enumerate(zip(col4, col7)):
                if c4 != c7 and c4 == 'ă':
                    new_col7[i] = 'ă'
                    changed = True
                if c4 != c7 and c4 == 'Ă':
                    new_col7[i] = 'Ă'
                    changed = True
            if changed:
                df.at[idx, 6] = ''.join(new_col7)
    return df

def replace_t(df):
    diff_mask = df[3] != df[6]

    for idx in df[diff_mask].index:
        col4 = df.at[idx, 3]
        col7 = df.at[idx, 6]
        # Find positions where characters differ
        if len(col4) == len(col7):
            new_col7 = list(col7)
            changed = False
            for i, (c4, c7) in enumerate(zip(col4, col7)):
                if c4 != c7 and c4 == 'ţ':
                    new_col7[i] = 'ţ'
                    changed = True
                if c4 != c7 and c4 == 'Ţ':
                    new_col7[i] = 'Ţ'
                    changed = True
            if changed:
                df.at[idx, 6] = ''.join(new_col7)
    return df

def replace_i(df):
    diff_mask = df[3] != df[6]

    for idx in df[diff_mask].index:
        col4 = df.at[idx, 3]
        col7 = df.at[idx, 6]
        # Find positions where characters differ
        if len(col4) == len(col7):
            new_col7 = list(col7)
            changed = False
            for i, (c4, c7) in enumerate(zip(col4, col7)):
                if c4 != c7 and c4 == 'Î':
                    new_col7[i] = 'Î'
                    changed = True
            if changed:
                df.at[idx, 6] = ''.join(new_col7)
    return df

def replace_space_pattern(df):
    pattern = r'\s*-\s*'
    replacement = ' - '
    diff_mask = df[3] != df[6]

    for idx in df[diff_mask].index:
        col4 = str(df.at[idx, 3])
        col7 = str(df.at[idx, 6])
        if re.search(pattern, col4) or re.search(pattern, col7):
            df.at[idx, 3] = re.sub(pattern, replacement, col4)
            df.at[idx, 6] = re.sub(pattern, replacement, col7)
    return df

pdf_url = "Denumirea_2008_2024.pdf"
line_tolerance = 2
md_pattern = re.compile(r'MD-\d{4}')


if re.search(r'Denumirea', pdf_url):
    df_xlsx = pd.read_excel('column_sizes.xlsx', header=None)
    row = df_xlsx[df_xlsx[0] == 'Denumirea']
    if not row.empty:
        x = row.iloc[0, 1:].tolist()
    else:
        raise ValueError("No column sizes for 'Denumirea' found in column_sizes.xlsx")

# x = [0, 55, 100, 170, 313, 470, 640, 820]

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
            y.append(page.height-40)

        for i in range(len(y) - 1):
            row_data = []
            for j in range(len(x) - 1):
                bbox = (x[j], y[i], x[j + 1], y[i+1])
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

# headers = ['No', 'Data anuntului', 'IDNO', 'Denumirea', 'Adresa', 'Din', 'In']
# df = pd.DataFrame(all_data, columns=headers)
# df.to_csv('table_extracted.csv', sep='|', index=False, header=True)

df = pd.DataFrame(all_data)

pattern = r'\b(\w+)\s*-\s*(\w+)\b'
replacement = r'\1-\2'

df[3] = df[3].astype(str).str.replace(pattern, replacement, regex=True)
df[6] = df[6].astype(str).str.replace(pattern, replacement, regex=True)

df = replace_a(df)
df = replace_t(df)
df = replace_i(df)
df = replace_space_pattern(df)

df.to_csv('table_extracted.csv', sep='|', index=False, header=False)
