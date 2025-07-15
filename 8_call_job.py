import pyodbc
import json

def run_sql_job():
    try:
        with open('config.json', 'r', encoding='utf-8') as file:
            config = json.load(file)

        database_config = config['database_config']

        database_name = database_config['database_name']
        server_name = database_config['server_name']
        username = database_config['username']
        password = database_config['password']
        job_name = database_config['job_name']

        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 18 for SQL Server}};'
            f'SERVER={server_name};'
            f'DATABASE={database_name};'
            f'UID={username};'
            f'PWD={password};'
            'TrustServerCertificate=yes;'
        )
        cursor = conn.cursor()

        cursor.execute("EXEC msdb.dbo.sp_start_job ?", job_name)
        conn.commit()

        print(f"Job '{job_name}' started successfully.")
    except pyodbc.Error as e:
        print(f"Error starting job '{job_name}': {e}")
    finally:
        if 'connection' in locals():
            conn.close()


run_sql_job()