import fitz  # PyMuPDF

def validate_headers(file_config, path_to_file):
    x = file_config['sizes']
    validate_headers = file_config['validate_headers']

    with fitz.open(path_to_file) as doc:
        page = doc[0]
        header_row = []
        for i in range(len(x) - 1):
            bbox = (x[i], 0, x[i + 1], page.rect.height)
            cell = page.get_textbox(bbox)
            header_row.append(cell.strip() if cell else '')

    for idx, expected in enumerate(validate_headers):
        cell_text = header_row[idx].replace('\n', '').strip() if idx < len(header_row) else ''
        if expected.replace('\n', '').strip() not in cell_text:
            return False

    return True