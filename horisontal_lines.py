import pdfplumber
import re

def read_page(y, x, page):
    page_data = []
    for i in range(len(y) - 1):
        row_data = []  # Collect data for a single row
        for j in range(len(x) - 1):
            bbox = (x[j], y[i], x[j + 1], y[i + 1])
            cell = page.within_bbox(bbox)
            text = cell.extract_text(x_tolerance=1, y_tolerance=1) if cell else ''
            if '\n' in text:
                text = re.sub(r'-(\n)', '-', text)
                text = text.replace('\n', ' ')
            row_data.append(f'"{text}"' if ' ' in text or '"' in text else text)  # Add quotes if needed
        page_data.append('|'.join(row_data))  # Join row data with '|'
    return '\n'.join(page_data)


with pdfplumber.open("downloaded_pdf_files/Finaliz_proced_reorg.pdf") as pdf:
    # for page in pdf.pages:
        page = pdf.pages [0]
        # y = [199, 201, 224, 248, 272, 297, 321, 345, 369, 393, 417, 439, 440, 442, 481, 482, 484, 499, 521]
        # [161, 183, 203, 224, 245, 267, 298, 315, 336, 357, 377, 398, 419, 439, 479, 480, 482, 497, 519]
        y = [183, 203 ]
        x = [0, 55, 100, 170, 347, 530, 800]
        page_data = read_page(y, x, page)
        print(page_data)




# import pdfplumber
#
# y_values = []
#
# with pdfplumber.open("downloaded_pdf_files/Finaliz_proced_reorg_2021_2024.pdf") as pdf:
#     for page in pdf.pages:
#         edges = page.edges
#
#         horizontal_lines = [edge for edge in edges if abs(edge['y1'] - edge['y0']) < 1 and edge['x1'] > edge['x0']]
#         horizontal_lines = horizontal_lines[::2]
#
#         for line in horizontal_lines:
#             y0, y1 = line['y0'], line['y1']
#             avg_y = round((y0 + y1) / 2)
#             y_values.append(avg_y)
#
#         y_values = sorted(set(y_values))
#         print("y values:", y_values)
#
