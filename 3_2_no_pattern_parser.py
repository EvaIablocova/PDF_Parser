import camelot
import re
import csv
import shutil

def delete_empty_rows(parsed_data_file_name):
    rows = []
    with open(parsed_data_file_name, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter='|')
        for row in reader:
            if any(field.strip() for field in row):
                rows.append(row)
    with open(parsed_data_file_name, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile, delimiter='|')
        writer.writerows(rows)


def process_csv(input_file, output_file):
    shutil.copy(input_file, 'debug_no_pattern.csv')

    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = list(csv.reader(infile, delimiter='|'))
        result = []

        i = 0
        while i < len(reader) - 2:
            # Skip rows that start with text
            if reader[i][0] and not re.match(r'^\d+$', reader[i][0]):
                i += 1
                continue

            if re.match(r'^\d+$', reader[i][0]) and re.match(r'^\d+$', reader[i][1]):
                i += 1
                continue

            # Check if the first element of the current row is "" and the next row starts with a number and the next row is ""
            if reader[i][0] == "" and re.match(r'^\d+$', reader[i + 1][0]) and reader[i+2][0] == "":
                # Save the current row and the next two rows
                row1 = reader[i]
                row2 = reader[i + 1]
                row3 = reader[i + 2]

                # Combine the elements of the three rows
                combined_row = [f"{a} {b} {c}".strip() for a, b, c in zip(row1, row2, row3)]
                result.append(combined_row)

                # Skip to the row after these three
                i += 3

            elif reader[i][0] == "" and reader[i+1][0] == "" and re.match(r'^\d+$', reader[i + 2][0]) and reader[i+3][0] == "" and reader[i+4][0] == "":
                # Save the current row and the next two rows
                row1 = reader[i]
                row2 = reader[i + 1]
                row3 = reader[i + 2]
                row4 = reader[i + 3]
                row5 = reader[i + 4]


                combined_row = [f"{a} {b} {c} {d} {e}".strip() for a, b, c, d, e in zip(row1, row2, row3, row4, row5)]
                result.append(combined_row)

                # Skip to the row after these three
                i += 5


            # Check if the first element of the current row starts with a number and the next row starts with a number
            elif reader[i-1][0] and re.match(r'^\d+$', reader[i][0]) and not reader[i+1][0]:
                result.append(reader[i])

                # Move to the next row
                i += 1

            elif not reader[i-1][0] and re.match(r'^\d+$', reader[i][0]) and reader[i+1][0]:
                result.append(reader[i])

                # Move to the next row
                i += 1

            elif not reader[i-1][0] and re.match(r'^\d+$', reader[i][0]) and not reader[i+1][0]:
                result.append(reader[i])

                # Move to the next row
                i += 1

            elif re.match(r'^\d+$', reader[i][0]) and re.match(r'^\d+$', reader[i][0]) and re.match(r'^\d+$', reader[i][0]):
                result.append(reader[i])

                # Move to the next row
                i += 1

            else:
                i += 1

        if re.match(r'^\d+$', reader[len(reader) - 2][0]) and re.match(r'^\d+$', reader[len(reader) - 1][0]):
            result.append(reader[len(reader) - 2])
            result.append(reader[len(reader) - 1])
    # Write the processed rows to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter='|')
        writer.writerows(result)

def transformare_check(cleaned_file):
    result = []
    with open(cleaned_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            elements = line.strip().split('|')
            if len(elements) >= 5 and 'Transformare' in elements[3]:
                elements[4] = (elements[4] + ' Transformare').strip()
                elements[3] = elements[3].replace('Transformare', '').strip()
            result.append('|'.join(elements))
    with open(cleaned_file, 'w', encoding='utf-8') as outfile:
        outfile.write('\n'.join(result))



def clean(processed_file, cleaned_file, count_columns):
    with open(processed_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()  # Read all lines from the file

    result = []
    for line in lines:
        line = line.strip()  # Remove any leading/trailing whitespace
        if line.count('|') == count_columns-1:
            result.append(line)
        else:
            if "||" in line:
                # Replace "||" with "|"
                result.append(line.replace("||", "|"))
            else:
                            # Split the line into elements
                            elements = line.split('|')
                            if len(elements) > 5:
                                # Move the 5th element to the end of the 6th element and remove the 5th element
                                try:
                                    elements[5] = elements[5] + " " + elements[4]  # Append the 5th element to the 6th element
                                    result.append('|'.join(elements[:4] + elements[5:]))  # Remove the 5th element
                                except ValueError:
                                     result.append(line)
                            else:
                                result.append(line)

    with open(cleaned_file, 'w', encoding='utf-8') as outfile:
        outfile.write('\n'.join(result))  # Write the processed lines back to the file

def parse_no_pattern(file_path, parsed_data_file_name, count_columns):

    try:
                tables = camelot.read_pdf(file_path, flavor='stream', pages='all')

                if tables:
                    with open(parsed_data_file_name, 'w', encoding='utf-8') as outfile:
                        for i, table in enumerate(tables):
                            table.to_csv(outfile, sep='|', index=False, header=(i == 0))
                    print(f"All tables saved into: {parsed_data_file_name}")
                else:
                    print("No tables found in pdf.")
    except Exception as e:
        print(f"Error ocured: {e}")

    try:
        delete_empty_rows(parsed_data_file_name)
        processed_file = 'processed_combined_tables.csv'
        process_csv(parsed_data_file_name, processed_file)
        cleaned_file = 'cleaned_combined_tables.csv'
        clean(processed_file, cleaned_file, count_columns)
        transformare_check(cleaned_file)
    except Exception as e:
        print(f"Error ocured: {e}")

    with open(cleaned_file, 'r', encoding='utf-8') as infile, open(parsed_data_file_name, 'w', encoding='utf-8') as outfile:
        outfile.write(infile.read())

    # with open(processed_file, 'r', encoding='utf-8') as infile, open(parsed_data_file_name, 'w', encoding='utf-8') as outfile:
    #      outfile.write(infile.read())


