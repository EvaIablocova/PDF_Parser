import json
import pyodbc

def write_step_message(step_name, message):
        with open('config.json', 'r', encoding='utf-8') as file:
            config = json.load(file)

        log_table_name = config['log_table_name']

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

        # Use parameterized query to prevent SQL injection
        insert_log_query = f"INSERT INTO {log_table_name} (ExecutionStep, MessageDescription) VALUES (?, ?)"
        cursor.execute(insert_log_query, (step_name, message))
        conn.commit()

        cursor.close()
        conn.close()