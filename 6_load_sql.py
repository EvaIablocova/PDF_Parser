import pandas as pd
import pyodbc
import os
import json
from sqlalchemy import create_engine
from datetime import datetime

file_config = json.loads(os.environ['FILE_CONFIG'])
path_to_file = json.loads(os.environ['path_to_file'])
count_columns = file_config['count_columns']

headers = file_config['headers']
if "last_updated_date" not in headers:
    headers.append("last_updated_date")
    headers.append("isValid")

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


engine = create_engine(
    f"mssql+pyodbc://{username}:{password}@{server_name}/{database_name}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
)

if not table_exists:
    create_table_query = f"""
    CREATE TABLE [{sql_table_name}] (
        [id] INT IDENTITY(1,1) PRIMARY KEY,
        {', '.join([f"[{header}] NVARCHAR(255)" for header in headers[:count_columns]])},
       [last_updated_date] DATETIME
        ,[isValid] BIT DEFAULT 1
    );
    """
    cursor.execute(create_table_query)
    conn.commit()

new_data = pd.read_csv(parsed_data_file_name, sep='|', header=None, names=headers)
new_data = new_data.astype(str)

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
    [id] INT IDENTITY(1,1) PRIMARY KEY,
     {', '.join([f"[{header}] NVARCHAR(255)" for header in headers[:count_columns]])},
    [last_updated_date] DATETIME,
     [isValid] BIT DEFAULT 1
);
"""
cursor.execute(create_staging_table_query)
conn.commit()


insert_staging_query = f"INSERT INTO {staging_table_name} ({', '.join(headers)}) VALUES ({', '.join(['?' for _ in headers])})"
for _, row in new_data.iterrows():
    row_data = tuple(row[:count_columns]) + (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1,)
    cursor.execute(insert_staging_query, row_data)
conn.commit()

# insert_delta_query = f"""
# INSERT INTO {sql_table_name} ({', '.join(headers)})
# SELECT {', '.join(headers[:-1])}, [last_updated_date]
# FROM {staging_table_name}
# EXCEPT
# SELECT {', '.join(headers[:-1])}, [last_updated_date]
# FROM {sql_table_name};
# """

# insert_delta_query = f"""
#
# IF OBJECT_ID('tempdb..#sql_table_name_tmp') IS NOT NULL DROP TABLE #sql_table_name_tmp;
# IF OBJECT_ID('tempdb..#staging_table_name_tmp') IS NOT NULL DROP TABLE #staging_table_name_tmp;
# IF OBJECT_ID('tempdb..#missing_row_indices') IS NOT NULL DROP TABLE #missing_row_indices;
#
# -- Create temporary tables
# SELECT id, {', '.join(headers[:-1])}
# INTO #sql_table_name_tmp
# FROM {sql_table_name};
#
# SELECT id, {', '.join(headers[:-1])}
# INTO #staging_table_name_tmp
# FROM {staging_table_name};
#
# -- Find missing rows
# SELECT stg.id
# INTO #missing_row_indices
# FROM #staging_table_name_tmp stg
# EXCEPT
# SELECT sql.id
# FROM #sql_table_name_tmp sql;
#
# -- Insert missing rows
# INSERT INTO {sql_table_name} ({', '.join(headers)})
# SELECT {', '.join(headers)}
# FROM {staging_table_name}
# WHERE id IN (SELECT id FROM #missing_row_indices);
#
# -- Clean up temporary tables
# DROP TABLE #sql_table_name_tmp;
# DROP TABLE #staging_table_name_tmp;
# """

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


