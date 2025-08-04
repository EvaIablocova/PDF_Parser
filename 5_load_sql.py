import pandas as pd
import pyodbc
import os
import json
import importlib
import sys
import time
import subprocess
write_to_log_module = importlib.import_module('0_3_write_to_log')

file_config = json.loads(os.environ['FILE_CONFIG'])
path_to_file = json.loads(os.environ['path_to_file'])
count_columns = file_config['count_columns']


sql_table_name = os.path.splitext(os.path.basename(path_to_file))[0]

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

parsed_data_dir = config['parsed_data_dir']
parsed_data_file_name = parsed_data_dir + "/" + os.path.splitext(os.path.basename(path_to_file))[0] + ".csv"


headers = file_config['headers']

database_config = config['database_config']

database_name = database_config['database_name']
server_name = database_config['server_name']
username = database_config['username']
password = database_config['password']

conn = pyodbc.connect(
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={server_name};'
    f'DATABASE={database_name};'
    f'UID={username};'
    f'PWD={password};'
    'TrustServerCertificate=yes;'
)
cursor = conn.cursor()

try:
    new_data = pd.read_csv(parsed_data_file_name, sep='|', header=None, names=headers, dtype=str)


    # Validate and clean data before insertion
    for col in new_data.columns:
        if new_data[col].dtype == 'object':  # Check for string columns
            new_data[col] = new_data[col].fillna('').astype(str)  # Replace NaN with empty string
        elif new_data[col].dtype in ['float64', 'int64']:  # Check for numeric columns
            new_data[col] = pd.to_numeric(new_data[col], errors='coerce')  # Convert invalid values to NaN
            new_data[col] = new_data[col].fillna(0)  # Replace NaN

    # new_data = new_data.astype(str)

    keyword = file_config["keyword"]
    staging_table_name = f"staging_{keyword}"

    # staging_table_name = f"staging_{sql_table_name}"

    # truncate_query = f"TRUNCATE TABLE {staging_table_name}"
    # cursor.execute(truncate_query)
    # conn.commit()


    write_to_log_module.write_step_message("Py.Staging", f"Staging file [start] {os.path.splitext(os.path.basename(path_to_file))[0]} ")

    try:
        for _, row in new_data.iterrows():
            insert_staging_query = f"INSERT INTO {staging_table_name} ({', '.join(headers)}) VALUES ({', '.join(['?' for _ in headers])})"
            cursor.execute(insert_staging_query, tuple(row))

        conn.commit()

        try:
            deduplicate_exec_query = f"EXEC PDFparser.dbo.Dedupe_Staging_Records '{staging_table_name}'"
            cursor.execute(deduplicate_exec_query)
            conn.commit()
            write_to_log_module.write_step_message("Py.Staging",
                                                   f"Deduplicated [done] {staging_table_name} ")
        except Exception as e:
            print(f"Error staging data: {e}")
            write_to_log_module.write_step_message("Py.Staging",
                                                   f"Deduplicated [failed] {staging_table_name} ")


        write_to_log_module.write_step_message("Py.Staging", f"Staging file [done] {os.path.splitext(os.path.basename(path_to_file))[0]} ")
    except Exception as e:
        print(f"Error staging data: {e}")
        write_to_log_module.write_step_message("Py.Staging", f"Staging file [failed] {os.path.splitext(os.path.basename(path_to_file))[0]} ")
        write_to_log_module.write_step_message("Py.Parser",
                                               f"[ERROR] Finished time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
except Exception as e:
    print(f"Error staging data: {e}")
    write_to_log_module.write_step_message("Py.Staging", f"Staging file [failed] {os.path.splitext(os.path.basename(path_to_file))[0]} ")
    write_to_log_module.write_step_message("Py.Parser",
                                           f"[ERROR] Finished time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

    sys.exit(1)

cursor.close()
conn.close()

if os.path.exists(parsed_data_file_name):
    os.remove(parsed_data_file_name)