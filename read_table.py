import pdfplumber
import pandas as pd

def extract_table_with_black_lines(pdf_path, column_coords, black_line_threshold=0.9):
    rows = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Get the page's horizontal lines
            horizontal_lines = [
                obj for obj in page.objects.get("rect", [])
                if obj["width"] > page.width * black_line_threshold and obj["height"] < 2
            ]

            # Sort lines by their y-coordinates
            horizontal_lines = sorted(horizontal_lines, key=lambda x: x["y1"], reverse=True)

            # Extract text between black lines
            for i in range(len(horizontal_lines) - 1):
                top = horizontal_lines[i]["y1"]
                bottom = horizontal_lines[i + 1]["y0"]

                # Extract text row by row based on column coordinates
                row = []
                for j in range(len(column_coords) - 1):
                    left = column_coords[j]
                    right = column_coords[j + 1]
                    cell = page.within_bbox((left, bottom, right, top)).extract_text()
                    row.append(cell.strip() if cell else "")
                rows.append(row)

    return rows


pdf_path = "downloaded_pdf_files/Finaliz_proced_reorg.pdf"
column_coords = [0, 55, 170, 250, 300, 500, 800]
rows = extract_table_with_black_lines(pdf_path, column_coords)

# Convert rows to a DataFrame
df = pd.DataFrame(rows)

# Save the DataFrame to a CSV file
output_csv_path = 'Finaliz_proced_reorg.csv'
df.to_csv(output_csv_path, sep='|', index=False)