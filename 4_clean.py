import pandas as pd
import re
import os
import json
import importlib
write_to_log_module = importlib.import_module('0_3_write_to_log')
import shutil

import re

def join_specific_words(text):

    for word in ['Chisinau, ', 'Republica Moldova', 'mun. ']:
        # Match the word with any spaces between letters and optional comma
        pattern = r'\b' + r'\s*'.join(list(word)) + r'\s*,?\b'
        def repl(m):
                matched = m.group(0)
                return word
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    return text

def spased_words(df):
    return df.apply(lambda x: join_specific_words(x) if isinstance(x, str) else x)


def clean_text(df, need_cleaning_columns):

    replacements = {
        'ă': 'ă',
        'Ă': 'Ă',
        'ţ': 'ţ',
        'Ţ': 'Ţ',
        'Î': 'Î',
        'î': 'î',
        'ș': 'ș',
        'ş':'ş',
        'Ș': 'Ș'
    }
    # space_pattern = r'\s*-\s*'
    # space_replacement = ' - '

    for col_a, col_b in zip(need_cleaning_columns[:-1], need_cleaning_columns[1:]):
        diff_mask = df[col_a] != df[col_b]

        for idx in df[diff_mask].index:
            col_a_value = str(df.at[idx, col_a])
            col_b_value = str(df.at[idx, col_b])

            # Replace characters
            if len(col_a_value.replace(' ', '')) == len(col_b_value.replace(' ', '')):
                new_col_b_value = list(col_b_value)
                changed = False
                for i, (ca, cb) in enumerate(zip(col_a_value, col_b_value)):
                    if ca != cb and ca in replacements:
                        new_col_b_value[i] = replacements[ca]
                        changed = True
                if changed:
                    col_b_value = ''.join(new_col_b_value)

            # # Replace space patterns
            # col_a_value = re.sub(space_pattern, space_replacement, col_a_value)
            # col_b_value = re.sub(space_pattern, space_replacement, col_b_value)

            # Update the DataFrame
            df.at[idx, col_a] = col_a_value
            df.at[idx, col_b] = col_b_value

    return df

def clean_data(df, need_cleaning_columns):

    if not need_cleaning_columns:
        return df

    # pattern = r'\b(\w+)\s*-\s*(\w+)\b'
    # replacement = r'\1-\2'
    #
    # print(df.shape[0])
    #
    # for i in need_cleaning_columns:
    #     df[i] = df[i].astype(str).str.replace(pattern, replacement, regex=True)


    df = clean_text(df, need_cleaning_columns)
    return df

# def clean_data2(df, need_cleaning_columns):



def clean_data_by_type (df, keyword):

    if keyword == 'Denumirea':
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

    elif keyword == 'Sediul':
        df[4] = df[4].astype(str).str.replace(r'\br l\b', 'r-l', regex=True)
        df[6] = spased_words(df[6])

    elif keyword == 'Reducere':
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

def clean_address (df, address_columns):
    if not address_columns:
        return df
    for col in address_columns:
        if col in df.columns:
            df[col] = df[col].str.replace(r'.*MD-', r'MD-', regex=True)
    return df

file_config = json.loads(os.environ['FILE_CONFIG'])
path_to_file = json.loads(os.environ['path_to_file'])

parsed_data_file_name = "parsed_files/" + os.path.splitext(os.path.basename(path_to_file))[0] + ".csv"

need_cleaning_columns = file_config['need_cleaning_columns']
keyword = file_config['keyword']


try:

    df = pd.read_csv(parsed_data_file_name, sep='|', header=None)

    df = clean_data(df, need_cleaning_columns)

    df = clean_data_by_type(df, keyword)

    df = clean_address(df, file_config['address_column_number'])

    df.to_csv(parsed_data_file_name, sep='|', index=False, header=False)

    copy_path = parsed_data_file_name.replace('.csv', '_copy_debug_cleaned.csv')
    shutil.copy(parsed_data_file_name, copy_path)
except Exception as e:
    write_to_log_module.write_step_message("Py.Parser", f"Cleaning file [failed] {os.path.splitext(os.path.basename(path_to_file))[0]} ")
    raise