import pandas as pd
import re
import os
import json

def clean_text(df, need_cleaning_columns):
    if not need_cleaning_columns:
        return df

    replacements = {
        'ă': 'ă',
        'Ă': 'Ă',
        'ţ': 'ţ',
        'Ţ': 'Ţ',
        'Î': 'Î'
    }
    space_pattern = r'\s*-\s*'
    space_replacement = ' - '

    for col_a, col_b in zip(need_cleaning_columns[:-1], need_cleaning_columns[1:]):
        diff_mask = df[col_a] != df[col_b]

        for idx in df[diff_mask].index:
            col_a_value = str(df.at[idx, col_a])
            col_b_value = str(df.at[idx, col_b])

            # Replace characters
            if len(col_a_value) == len(col_b_value):
                new_col_b_value = list(col_b_value)
                changed = False
                for i, (ca, cb) in enumerate(zip(col_a_value, col_b_value)):
                    if ca != cb and ca in replacements:
                        new_col_b_value[i] = replacements[ca]
                        changed = True
                if changed:
                    col_b_value = ''.join(new_col_b_value)

            # Replace space patterns
            col_a_value = re.sub(space_pattern, space_replacement, col_a_value)
            col_b_value = re.sub(space_pattern, space_replacement, col_b_value)

            # Update the DataFrame
            df.at[idx, col_a] = col_a_value
            df.at[idx, col_b] = col_b_value

    return df

def clean_data(parsed_data_file_name, need_cleaning_columns):
    df = pd.read_csv(parsed_data_file_name, sep='|', header=None)

    pattern = r'\b(\w+)\s*-\s*(\w+)\b'
    replacement = r'\1-\2'

    if need_cleaning_columns:
        for i in need_cleaning_columns:
            df[i] = df[i].astype(str).str.replace(pattern, replacement, regex=True)

    df = clean_text(df, need_cleaning_columns)
    return df


def clean_data_by_type (df, document_type_name):

    if document_type_name == 'Denumirea':
        if len(df) > 3320:
            df.loc[3319] = [
                int('3320'),
                '07.08.2014',
                '1005603002522',
                'Întreprinderea Mixtă ""VINAGROFOROS"" S.R.L.',
                'MD-7320, s. Cîşla, r-l Cantemir, Republica Moldova',
                'INTREPRINDEREA MIXTA ""VINAGROFOROS"" SRL',
                'Întreprinderea Mixtă ""VINAGROFOROS"" S.R.L.'
            ]

    elif document_type_name == 'Sediul':
        df[4] = df[4].astype(str).str.replace(r'\br l\b', 'r-l', regex=True)

    elif document_type_name == 'Reducere':
        if len(df) > 716:
            df.loc[716] = [
                int('717'),
                '6.05.2014',
                '1003600020651',
                'Societatea Comercială ""BUGE-PETRICANCA"" S.R.L.',
                'MD-2069, str. Petricani 19/2, mun. Chisinau, Republica Moldova',
                '888436,00',
                '822630,00'
            ]

            new_row = pd.DataFrame(
                {
                    0: [int('718')],
                    1: ['6.05.2014'],
                    2: ['1002604000030'],
                    3: ['SOCIETATEA CU RĂSPUNDERE LIMITATĂ ""REFORMA C.M."""'],
                    4: ['s. Terebna, rl. Edinet, Republica Moldova'],
                    5: ['4951176,00'],
                    6: ['1651176,00']
                }
            )

            df = pd.concat([df.iloc[:717], new_row, df.iloc[717:]]).reset_index(drop=True)

    return df

file_config = json.loads(os.environ['FILE_CONFIG'])
parsed_data_file_name = file_config['parsed_data_file_name']
need_cleaning_columns = file_config['need_cleaning_columns']
document_type_name = file_config['document_type_name']

df = clean_data(parsed_data_file_name, need_cleaning_columns)

df = clean_data_by_type(df, document_type_name)

df.to_csv(parsed_data_file_name, sep='|', index=False, header=False)