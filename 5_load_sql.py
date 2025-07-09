import pandas as pd
import pyodbc
import os
import json
from sqlalchemy import create_engine

file_config = json.loads(os.environ['FILE_CONFIG'])
path_to_file = json.loads(os.environ['path_to_file'])


headers = file_config['headers']

parsed_data_file_name = "parsed_files/" + os.path.splitext(os.path.basename(path_to_file))[0] + ".csv"
sql_table_name = os.path.splitext(os.path.basename(path_to_file))[0]

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

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

# Check if the table exists
table_exists_query = f"SELECT COUNT(*) FROM sys.tables WHERE name = '{sql_table_name}'"
cursor.execute(table_exists_query)
table_exists = cursor.fetchone()[0] > 0

if table_exists:
    # Read existing table data into a DataFrame
    existing_data_query = f"SELECT * FROM [{sql_table_name}]"

    engine = create_engine(
        f"mssql+pyodbc://{username}:{password}@{server_name}/{database_name}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    )

    existing_data = pd.read_sql(existing_data_query, engine)

    # Load new data
    df = pd.read_csv(parsed_data_file_name, sep='|', header=None, names=headers)
    df = df.astype(str)

    # Find the difference between the new data and the existing data
    new_rows = pd.concat([df, existing_data]).drop_duplicates(keep=False)

    if not new_rows.empty:
        insert_query = f"INSERT INTO {sql_table_name} ({', '.join(headers)}) VALUES ({', '.join(['?' for _ in headers])})"
        for _, row in new_rows.iterrows():
            cursor.execute(insert_query, tuple(row))
    else:
        print("No data to insert into the table.")
else:
    # Create the table and insert all rows
    create_table_query = f"""
    CREATE TABLE [{sql_table_name}] (
        {', '.join([f"[{header}] NVARCHAR(255)" for header in headers])}
    );
    """
    cursor.execute(create_table_query)
    conn.commit()

    df = pd.read_csv(parsed_data_file_name, sep='|', header=None, names=headers)
    df = df.astype(str)

    insert_query = f"INSERT INTO {sql_table_name} ({', '.join(headers)}) VALUES ({', '.join(['?' for _ in headers])})"
    for _, row in df.iterrows():
        cursor.execute(insert_query, tuple(row))


conn.commit()
cursor.close()
conn.close()