import pandas as pd
import pyodbc
import os
import json
from sqlalchemy import create_engine
from datetime import datetime

file_config = json.loads(os.environ['FILE_CONFIG'])
path_to_file = json.loads(os.environ['path_to_file'])
count_columns = file_config['count_columns']


sql_table_name = os.path.splitext(os.path.basename(path_to_file))[0]

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

parsed_data_dir = config['parsed_data_dir']
parsed_data_file_name = parsed_data_dir + "/" + os.path.splitext(os.path.basename(path_to_file))[0] + ".csv"

validated_data_dir = config['validated_data_dir']
validated_data_file_name = validated_data_dir + "/" + os.path.splitext(os.path.basename(path_to_file))[0] + ".csv"

technical_fields = config['technical_fields']
field_names = list(technical_fields.keys())

headers = file_config['headers']
headers.extend(field_names)

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


# engine = create_engine(
#     f"mssql+pyodbc://{username}:{password}@{server_name}/{database_name}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
# )

if not table_exists:
    create_table_query = f"""
    CREATE TABLE [{sql_table_name}] (
         id INT IDENTITY(1,1) PRIMARY KEY,
        {', '.join([f"[{header}] NVARCHAR(255)" for header in headers[:count_columns]])},
        {', '.join([f"[{field}] {definition}" for field, definition in technical_fields.items()])}
    );
    """
    cursor.execute(create_table_query)
    conn.commit()

new_data = pd.read_csv(validated_data_file_name, sep='|', header=None, names=headers)
new_data.iloc[:, 1:count_columns] = new_data.iloc[:, 1:count_columns].astype(str)

staging_table_name = f"staging_{sql_table_name}"


staging_table_exists_query = f"SELECT COUNT(*) FROM sys.tables WHERE name = '{staging_table_name}'"
cursor.execute(staging_table_exists_query)
staging_table_exists = cursor.fetchone()[0] > 0

if  staging_table_exists:
    drop_staging_table_query = f"DROP TABLE [{staging_table_name}];"
    cursor.execute(drop_staging_table_query)
    conn.commit()

create_staging_table_query = f"""
    CREATE TABLE [{staging_table_name}] (
        id INT IDENTITY(1,1) PRIMARY KEY,
        {', '.join([f"[{header}] NVARCHAR(255)" for header in headers[:count_columns]])},
        {', '.join([f"[{field}] {definition}" for field, definition in technical_fields.items()])}
    );
    """
cursor.execute(create_staging_table_query)
conn.commit()

# new_data['No'] = new_data['No'].astype(str)  # NVARCHAR
# new_data['Date_of_announcement'] = new_data['Date_of_announcement'].astype(str)  # NVARCHAR
# new_data['IDNO'] = new_data['IDNO'].astype(str)  # NVARCHAR
# new_data['is_valid'] = new_data['is_valid'].fillna(1).astype(int)  # BIT
# new_data['is_deleted'] = new_data['is_deleted'].fillna(0).astype(int)  # BIT


# Replace both float('nan') and string 'nan' with None
new_data = new_data.replace({float('nan'): None, 'nan': None})

for _, row in new_data.iterrows():
    # Filter out columns with None values
    non_null_columns = [col for col, val in zip(new_data.columns, row) if val is not None]
    non_null_values = [val for val in row if val is not None]

    # Construct the query dynamically
    insert_staging_query = f"INSERT INTO {staging_table_name} ({', '.join(non_null_columns)}) VALUES ({', '.join(['?' for _ in non_null_columns])})"
    cursor.execute(insert_staging_query, non_null_values)

conn.commit()

insert_delta_query = f"""
IF OBJECT_ID('tempdb..#tmp_table') IS NOT NULL DROP TABLE #tmp_table;
IF OBJECT_ID('tempdb..#new_row_ids') IS NOT NULL DROP TABLE #new_row_ids;

CREATE TABLE #tmp_table (
    {', '.join([f"[{col}] NVARCHAR(255)" for col in headers[:count_columns]])}
);

INSERT INTO #tmp_table
SELECT {', '.join(headers[:count_columns])}
FROM {staging_table_name}
EXCEPT
SELECT {', '.join(headers[:count_columns])}
FROM {sql_table_name};


-- Select IDs of new rows from the staging table based on the temporary table
SELECT stg.id
INTO #new_row_ids
FROM {staging_table_name} stg
JOIN #tmp_table tmp
ON { ' AND '.join([f'stg.[{col}] = tmp.[{col}]' for col in headers[:count_columns]]) };

-- Insert new rows into the main table
INSERT INTO {sql_table_name} ({', '.join(headers)})
SELECT {', '.join(headers)}
FROM {staging_table_name}
WHERE id IN (SELECT id FROM #new_row_ids);


SELECT * INTO #tmp_staging_table
FROM {staging_table_name}
WHERE id IN (SELECT id FROM #new_row_ids);

-- Delete all rows from the staging table
DELETE FROM {staging_table_name};

-- Insert only new rows into the staging table
INSERT INTO {staging_table_name} ({', '.join(headers)})
SELECT {', '.join(headers)}
FROM #tmp_staging_table;



-- Clean up temporary tables
DROP TABLE #tmp_table;
DROP TABLE #new_row_ids;
DROP TABLE #tmp_staging_table;

"""


cursor.execute(insert_delta_query)
conn.commit()


cursor.close()
conn.close()


