import pandas as pd
import os
import json

def check_address_format(df, address_column_numbers):
    report = []
    pattern = r'^MD-\d{4}'

    for column_number in address_column_numbers:
        mask = ~df[column_number].astype(str).str.match(pattern)
        invalid_rows = df[mask]

        if invalid_rows.empty:
            report.append(f"All rows in column {column_number + 1} start with 'MD-' and 4 digits")
        else:
            report.append(f"Rows where column {column_number + 1} does NOT start with 'MD-' and 4 digits:")
            report.append(invalid_rows[[0, column_number]])
    return report

def check_column_equality(df, equal_columns_numbers):
    report = []
    col1 = df.iloc[:, 0].astype(str)

    for i in range(len(equal_columns_numbers) - 1):
        col_a = df.iloc[:, equal_columns_numbers[i]].astype(str)
        col_b = df.iloc[:, equal_columns_numbers[i + 1]].astype(str)
        mismatches = df.index[col_a != col_b]

        if mismatches.empty:
            report.append(f"All values in columns {equal_columns_numbers[i] + 1} and {equal_columns_numbers[i + 1] + 1} are identical")
        else:
            report.append(f"Rows where columns {equal_columns_numbers[i] + 1} and {equal_columns_numbers[i + 1] + 1} are NOT identical:")
            for idx in mismatches:
                val1 = col1.loc[idx]
                val_a = col_a.loc[idx]
                val_b = col_b.loc[idx]
                report.append(f"Row {idx}: 1st col='{val1}' | col {equal_columns_numbers[i] + 1}='{val_a}' | col {equal_columns_numbers[i + 1] + 1}='{val_b}'")
    return report

def check_third_column_13_digits(df, idno_column_number):
    report = []
    third_col = df.iloc[:, idno_column_number].astype(str)
    invalid_rows = third_col[~third_col.str.match(r'^\d{13}$')]

    if invalid_rows.empty:
        report.append("All values in the idno column have exactly 13 digits")
    else:
        report.append(f"Rows with invalid values in the idno column (not 13 digits): {invalid_rows.index.tolist()}")
    return report

def check_dates_in_range(df, date_column_number, start_date, end_date):
    report = []

    try:
        dates = pd.to_datetime(df.iloc[:, date_column_number], dayfirst=True, errors='coerce')
    except Exception as e:
        report.append(f"Error parsing dates: {e}")
        return report

    if dates.isna().any():
        report.append(f"Found {dates.isna().sum()} unparsable date values")

    out_of_range = df.loc[(dates < start_date) | (dates > end_date)]
    if not out_of_range.empty:
        report.append(f"Found {len(out_of_range)} dates out of set range")
        report.append(out_of_range.iloc[:, date_column_number].tolist())
    else:
        report.append("All dates in the date column are within the specified range")
    return report

def find_sequence_breaks(df):
    first_col = df.iloc[:, 0]
    if not pd.api.types.is_numeric_dtype(first_col):
        return "First column is not numeric, cannot check for sequence breaks"
    sorted_col = first_col.sort_values().reset_index(drop=True)
    diffs = sorted_col.diff().fillna(1)
    breaks = diffs[diffs != 1].index.tolist()
    if not breaks:
        return "No sequence breaks found"
    else:
        # Show the value before and after the break
        breaks_info = []
        for idx in breaks:
            if idx > 0:
                prev_val = sorted_col.iloc[idx - 1]
                curr_val = sorted_col.iloc[idx]
                breaks_info.append(f"Break between {prev_val} and {curr_val} at index {idx}")
        return breaks_info


def validate_parsed_data(df, estimated_rows_count):
    report = []

    if df.shape[0] < estimated_rows_count:
        report.append(f"Error: Too few rows in the table, expected at least {estimated_rows_count} rows")
    else:
        report.append(f"Table has {df.shape[0] + 1} rows, which is sufficient")

    if df.duplicated().sum() > 0:
        report.append(f"Found {df.duplicated().sum()} duplicate rows")
    else:
        report.append("No duplicate rows found")

    if df.isna().sum().sum() > 0:
        report.append(f"Found {df.isna().sum().sum()} empty cells in the table")
    else:
        report.append("No empty cells found in the table")

    first_col = df.iloc[:, 0]
    if pd.api.types.is_numeric_dtype(first_col):
        sorted_col = first_col.sort_values().reset_index(drop=True)
        expected = pd.Series(range(2, estimated_rows_count+1))
        missing = set(expected) - set(sorted_col)
        if not missing:
            report.append("First column contains all consecutive numeric values from min to max")
        else:
            report.append(f"First column is missing values: {sorted(missing)}")
            breaks_report = find_sequence_breaks(df)
            print("Sequence breaks:", breaks_report)
    else:
        report.append("First column is not numeric, cannot check for consecutive values")

    return report

file_config = json.loads(os.environ['FILE_CONFIG'])

parsed_data_file_name = file_config['parsed_data_file_name']
address_column_number = file_config['address_column_number']
equal_columns_numbers = file_config['equal_columns_numbers']
idno_column_number = file_config['idno_column_number']
date_column_number = file_config['date_column_number']
start_date = file_config['start_date']
end_date = file_config['end_date']
estimated_rows_count = file_config['estimated_rows_count']

df = pd.read_csv(parsed_data_file_name, sep='|', header=None)

df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
validation_report = validate_parsed_data(df, estimated_rows_count)
print("Validation report:")
for line in validation_report:
    print(line)


date_report = check_dates_in_range(df, date_column_number, start_date, end_date)
print("Date check report:", date_report)

third_col_report = check_third_column_13_digits(df, idno_column_number)
for line in third_col_report:
    print(line)

address_report = check_address_format(df, address_column_number)
for line in address_report:
    print(line)

col_equality_report = check_column_equality(df, equal_columns_numbers)
for line in col_equality_report:
    print(line)

