import pandas as pd

def check_address_format(df):
    report = []
    pattern = r'^MD-\d{4}'

    mask = ~df[4].astype(str).str.match(pattern)
    invalid_rows = df[mask]

    if invalid_rows.empty:
        report.append ("All rows in the 5th column start with 'MD-' and 4 digits")
    else:
        report.append ("Rows where the 5th column does NOT start with 'MD-' and 4 digits:")
        report.append (invalid_rows[[0, 4]])
    return report

def check_column_equality(df):
    report = []
    col1 = df.iloc[:, 0].astype(str)
    col4 = df.iloc[:, 3].astype(str)
    col7 = df.iloc[:, 6].astype(str)
    mismatches = df.index[col4 != col7]
    if mismatches.empty:
        report.append("All values in the 4th and 7th columns are identical")
    else:
        for idx in mismatches:
            val1 = col1.loc[idx]
            val4 = col4.loc[idx]
            val7 = col7.loc[idx]
            report.append(f"Row {idx}: 1st col='{val1}' | 4th col='{val4}' | 7th col='{val7}'")
    return report

def check_third_column_13_digits(df):
    report = []
    third_col = df.iloc[:, 2].astype(str)
    invalid_rows = third_col[~third_col.str.match(r'^\d{13}$')]

    if invalid_rows.empty:
        report.append("All values in the third column have exactly 13 digits")
    else:
        report.append(f"Rows with invalid values in the third column (not 13 digits): {invalid_rows.index.tolist()}")
    return report

def check_dates_in_range(df):
    report = []
    # Parse the second column as dates (assuming index 1)
    try:
        dates = pd.to_datetime(df.iloc[:, 1], dayfirst=True, errors='coerce')
    except Exception as e:
        report.append(f"Error parsing dates: {e}")
        return report

    start = pd.Timestamp('2008-06-01')
    end = pd.Timestamp('2024-12-31')

    if dates.isna().any():
        report.append(f"Found {dates.isna().sum()} unparsable date values")

    out_of_range = df.loc[(dates < start) | (dates > end)]
    if not out_of_range.empty:
        report.append(f"Found {len(out_of_range)} dates out of range 01.06.2008 - 31.12.2024")
        report.append(out_of_range.iloc[:, 1].tolist())
    else:
        report.append("All dates in the second column are within the specified range")
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


def validate_parsed_data(df):
    report = []

    if df.shape[0] < 9120:
        report.append("Error: Too few rows in the table, expected at least 9121 rows")
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
        expected = pd.Series(range(2, 9122))
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

df = pd.read_csv('table_extracted.csv', sep='|', header=None)
df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
validation_report = validate_parsed_data(df)
print("Validation report:")
for line in validation_report:
    print(line)


date_report = check_dates_in_range(df)
print("Date check report:", date_report)

third_col_report = check_third_column_13_digits(df)
for line in third_col_report:
    print(line)

address_report = check_address_format(df)
for line in address_report:
    print(line)

col_equality_report = check_column_equality(df)
for line in col_equality_report:
    print(line)

