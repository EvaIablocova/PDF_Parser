import pandas as pd
import pyodbc
import os
import json

file_config = json.loads(os.environ['FILE_CONFIG'])

sql_table_name = file_config['sql_table_name']
headers = file_config['headers']
parsed_data_file_name = file_config['parsed_data_file_name']


with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

database_config = config['database_config']

database_name = database_config['database_name']
server_name = database_config['server_name']
username = database_config['username']
password = database_config['password']


create_table_query = f"""
IF EXISTS (SELECT * FROM sys.tables WHERE name = '{sql_table_name}')
    DROP TABLE {sql_table_name};

CREATE TABLE [{sql_table_name}] (
    {', '.join([f"[{header}] NVARCHAR(255)" for header in headers])}
);
"""

conn = pyodbc.connect(
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={server_name};'
    f'DATABASE={database_name};'
    f'UID={username};'
    f'PWD={password};'
    'TrustServerCertificate=yes;'
)
cursor = conn.cursor()


cursor.execute(create_table_query)
conn.commit()

df = pd.read_csv(parsed_data_file_name, sep='|', header=None, names=headers)

# Convert all columns to string type
df = df.astype(str)

insert_query = f"INSERT INTO {sql_table_name} ({', '.join(headers)}) VALUES ({', '.join(['?' for _ in headers])})"
for _, row in df.iterrows():
    cursor.execute(insert_query, tuple(row))


conn.commit()
cursor.close()
conn.close()