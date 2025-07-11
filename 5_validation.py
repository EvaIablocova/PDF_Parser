import pandas as pd
import os
import json
import re

def check_address_format(df, address_column_numbers):

    if not address_column_numbers:
        return ["No address columns specified for format check"]

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
    if not equal_columns_numbers:
        return ["No columns specified for equality check"]

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


def check_dates_in_range(df, date_column_numbers, start_date, end_date):
    report = []

    for column_number in date_column_numbers:
        try:
            dates = pd.to_datetime(df.iloc[:, column_number], dayfirst=True, errors='coerce')
        except Exception as e:
            report.append(f"Error parsing dates in column {column_number + 1}: {e}")
            continue

        if dates.isna().any():
            report.append(f"Column {column_number + 1}: Found {dates.isna().sum()} unparsable date values")

        out_of_range = df.loc[(dates < start_date) | (dates > end_date)]
        if not out_of_range.empty:
            report.append(f"Column {column_number + 1}: Found {len(out_of_range)} dates out of set range")
            report.append(out_of_range.iloc[:, column_number].tolist())
        else:
            report.append(f"Column {column_number + 1}: All dates are within the specified range")

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
        report.append(f"Table has {df.shape[0]} rows, which is sufficient")

    duplicates_mask = df.duplicated(keep=False)
    if duplicates_mask.sum() > 0:
        df.loc[duplicates_mask, 'is_valid'] = 0
        df.loc[duplicates_mask, 'error_message'] += "Duplicate row; "
        report.append(f"Found {duplicates_mask.sum()} duplicate rows")
    else:
        report.append("No duplicate rows found")

    if df.isna().sum().sum() > 0:
        empty_rows_mask = df.isna().any(axis=1)
        df.loc[empty_rows_mask, 'is_valid'] = 0
        df.loc[empty_rows_mask, 'error_message'] += "Row contains empty cells; "
        report.append(f"Found {df.isna().sum().sum()} empty cells in the table")
    else:
        report.append("No empty cells found in the table")

    first_col = df.iloc[:, 0]
    if pd.api.types.is_numeric_dtype(first_col):
        sorted_col = first_col.sort_values().reset_index(drop=True)
        expected = pd.Series(range(2, estimated_rows_count + 1))
        missing = set(expected) - set(sorted_col)
        if not missing:
            report.append("First column contains all consecutive numeric values from min to max")
        else:
            report.append(f"First column is missing values: {sorted(missing)}")
            breaks_report = find_sequence_breaks(df)
            print("Sequence breaks:", breaks_report)
            non_consecutive_mask = ~df.iloc[:, 0].isin(sorted_col)
            df.loc[non_consecutive_mask, 'is_valid'] = 0
            df.loc[non_consecutive_mask, 'error_message'] += "Non-consecutive values in the first column; "
    else:
        report.append("First column is not numeric, cannot check for consecutive values")
        df['is_valid'] = 0
        df['error_message'] += "Non-numeric values in the first column; "

    return report, df









file_config = json.loads(os.environ['FILE_CONFIG'])
path_to_file = json.loads(os.environ['path_to_file'])

parsed_data_file_name = "parsed_files/" + os.path.splitext(os.path.basename(path_to_file))[0] + ".csv"

address_column_number = file_config['address_column_number']
equal_columns_numbers = file_config['equal_columns_numbers']
idno_column_number = file_config['idno_column_number']
estimated_rows_count = file_config['estimated_rows_count']

date_column_number = file_config['date_column_number']

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

validated_data_dir = config['validated_data_dir']
os.makedirs(validated_data_dir, exist_ok=True)

config_last_dates_in_db_path = config.get("config_last_dates_in_db")

with open(config_last_dates_in_db_path, 'r', encoding='utf-8') as f:
    config_last_dates_in_db = json.load(f)

file_name_to_find = os.path.splitext(os.path.basename(path_to_file))[0] + ".pdf"

matching_record = next(
    (record for record in config_last_dates_in_db if record.get("FileName") == file_name_to_find),
    None
)

start_date = matching_record['start_date']
end_date = matching_record['end_date']


df = pd.read_csv(parsed_data_file_name, sep='|', header=None)

technical_fields = config['technical_fields']
field_names = list(technical_fields.keys())

for field in field_names:
    if field not in df.columns:
        df[field] = pd.NA

validated_data_file_name = validated_data_dir + "/" + os.path.splitext(os.path.basename(path_to_file))[0] + ".csv"




df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
validation_report, df = validate_parsed_data(df, estimated_rows_count)
print("Validation report:")
for line in validation_report:
    print(line)



#  ----------------------------

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

#  ----------------------------

df.to_csv(validated_data_file_name, sep='|', index=False, header=False)

