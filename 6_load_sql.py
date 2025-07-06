import pandas as pd
import pyodbc

headers = ['No', 'Date_of_announcement', 'IDNO', 'Name', 'Address', 'From_name', 'Into_name']

create_table_query = """
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'table_extracted') 
    DROP TABLE table_extracted;

CREATE TABLE [table_extracted] (
    [No] NVARCHAR(255),
    [Date_of_announcement] NVARCHAR(255),
    [IDNO] NVARCHAR(255),
    [Name] NVARCHAR(255),
    [Address] NVARCHAR(255),
    [From_name] NVARCHAR(255),
    [Into_name] NVARCHAR(255)
);
"""

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=DenumireaDB;'
    'UID=SA;'
    'PWD=MyStr0ngPass123;'
    'TrustServerCertificate=yes;'
)
cursor = conn.cursor()

cursor.execute(create_table_query)
conn.commit()

df = pd.read_csv('table_extracted.csv', sep='|', header=None, names=headers)

insert_query = f"INSERT INTO table_extracted ({', '.join(headers)}) VALUES (?, ?, ?, ?, ?, ?, ?)"
for _, row in df.iterrows():
    cursor.execute(insert_query, tuple(row))

conn.commit()
cursor.close()
conn.close()