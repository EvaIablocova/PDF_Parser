import fitz  # PyMuPDF
import re

def change_config_init_lichid(file_config, path_to_file):
    isChanged = False

    if file_config.get('keyword') == 'Init_lichid':
        if file_config.get('count_columns') == 6:
            file_config.update({
                'count_columns': 5,
                'sizes':  [0,
                55,
                100,
                165,
                430,
                820],
                'search_pattern': r'MD-\d{4}',
                'address_column_number': [4],
                'equal_columns_numbers': None,
                'idno_column_number': 2,
                'date_column_number': [1],
                'estimated_rows_count': 599,
                'need_cleaning_columns': None,
                'equal_columns_with_dash': [],
                'headers': [
                    'No',
                    'Date_of_announcement',
                    'IDNO',
                    'Name',
                    'Address'
                ],
                'validate_headers': [
                    'N/o',
                    'Data anunţului',
                    'IDNO',
                    'Denumirea',
                    'Adresa'
                ]
            })
        else:
            file_config.update({
                'count_columns': 6,
                'sizes': [
                    0,
                    60,
                    105,
                    170,
                    370,
                    619,
                    820
                ],
                'search_pattern': r'MD-\d{4}',
                'address_column_number': [4],
                'equal_columns_numbers': None,
                'idno_column_number': 2,
                'date_column_number': [1],
                'estimated_rows_count': 599,
                'need_cleaning_columns': None,
                'equal_columns_with_dash': [],
                'headers': [
                    'No',
                    'Date_of_announcement',
                    'IDNO',
                    'Name',
                    'Address',
                    'Date_from'
                ],
                'validate_headers': [
                    'N/o',
                    'Data anunţului',
                    'IDNO',
                    'Denumirea',
                    'Adresa',
                    'Persoana juridică se află în proces de dizolvare'
                ]
            })

        isChanged = True
    return file_config, isChanged

def validate_headers(file_config, path_to_file):
    isValid = True
    isChanged = False

    x = file_config['sizes']
    validate_headers = file_config['validate_headers']

    with fitz.open(path_to_file) as doc:
        page = doc[0]
        header_row = []
        for i in range(len(x) - 1):
            bbox = (x[i], 0, x[i + 1], page.rect.height-60)
            cell = page.get_textbox(bbox)
            header_row.append(cell.strip() if cell else '')

    for idx, expected in enumerate(validate_headers):
        cell_text = header_row[idx].replace('\n', '').strip() if idx < len(header_row) else ''
        if expected.replace('\n', '').strip() not in cell_text:
           isValid  = False
        if expected == 'Denumirea' and re.search(r'MD-\d{4}', cell_text):
            isValid = False

    if (not isValid) and file_config['keyword'] == 'Init_lichid':
        file_config, isChanged = change_config_init_lichid(file_config, path_to_file)


    return isValid, file_config, isChanged