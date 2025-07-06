import pandas as pd
import re
import time

def clean_text(df):
    diff_mask = df[3] != df[6]

    replacements = {
        'ă': 'ă',
        'Ă': 'Ă',
        'ţ': 'ţ',
        'Ţ': 'Ţ',
        'Î': 'Î'
    }
    space_pattern = r'\s*-\s*'
    space_replacement = ' - '

    for idx in df[diff_mask].index:
        col4 = str(df.at[idx, 3])
        col7 = str(df.at[idx, 6])

        # Replace characters
        if len(col4) == len(col7):
            new_col7 = list(col7)
            changed = False
            for i, (c4, c7) in enumerate(zip(col4, col7)):
                if c4 != c7 and c4 in replacements:
                    new_col7[i] = replacements[c4]
                    changed = True
            if changed:
                col7 = ''.join(new_col7)

        # Replace space patterns
        col4 = re.sub(space_pattern, space_replacement, col4)
        col7 = re.sub(space_pattern, space_replacement, col7)

        # Update the DataFrame
        df.at[idx, 3] = col4
        df.at[idx, 6] = col7

    return df

def clean_data(df):

    pattern = r'\b(\w+)\s*-\s*(\w+)\b'
    replacement = r'\1-\2'

    df[3] = df[3].astype(str).str.replace(pattern, replacement, regex=True)
    df[6] = df[6].astype(str).str.replace(pattern, replacement, regex=True)

    df = clean_text(df)

    df.to_csv('table_extracted.csv', sep='|', index=False, header=False)

df = pd.read_csv('table_extracted.csv', sep='|', header=None)
clean_data(df)