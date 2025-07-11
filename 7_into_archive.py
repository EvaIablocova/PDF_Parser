import pyodbc
import csv
import json
import os
from datetime import datetime

file_config = json.loads(os.environ['FILE_CONFIG'])

headers = file_config['headers']
if "last_updated_date" not in headers:
    headers.append("last_updated_date")
    headers.append("isValid")



with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

archive_dir = config['archive_dir']
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

path_to_file = json.loads(os.environ['path_to_file'])
sql_table_name = os.path.splitext(os.path.basename(path_to_file))[0]
staging_table_name = f"staging_{sql_table_name}"

os.makedirs(archive_dir, exist_ok=True)

archive_csv_file = archive_dir + f"/archive_{sql_table_name}_{datetime.now().strftime('%Y%m%d%H%M')}.csv"
archive_staging_csv_file = archive_dir + f"/archive_{staging_table_name}_{datetime.now().strftime('%Y%m%d%H%M')}.csv"



with open(archive_csv_file, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)


    cursor.execute(f"SELECT * FROM {sql_table_name} WHERE 1=0")
    writer.writerow(["id"] + headers)


    cursor.execute(f"SELECT * FROM {sql_table_name}")
    while True:
        row = cursor.fetchone()
        if not row:
            break
        writer.writerow(row)

with open(archive_staging_csv_file, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)


    cursor.execute(f"SELECT * FROM {staging_table_name} WHERE 1=0")
    writer.writerow(headers)


    cursor.execute(f"SELECT * FROM {staging_table_name}")
    while True:
        row = cursor.fetchone()
        if not row:
            break
        writer.writerow(row)



cursor.close()
conn.close()

print(f"Table {sql_table_name} has been exported to {archive_csv_file}.")
print(f"Table {staging_table_name} has been exported to {archive_staging_csv_file}.")