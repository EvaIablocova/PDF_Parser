import pyodbc
import csv


connection_string = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=your_server;DATABASE=your_database;UID=your_username;PWD=your_password"


sql_table_name = "your_table_name"
output_csv_file = "output.csv"

# Connect to the database
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Open the CSV file for writing
with open(output_csv_file, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)

    # Fetch column names
    cursor.execute(f"SELECT * FROM {sql_table_name} WHERE 1=0")
    column_names = [desc[0] for desc in cursor.description]
    writer.writerow(column_names)  # Write header row

    # Stream data row by row
    cursor.execute(f"SELECT * FROM {sql_table_name}")
    while True:
        row = cursor.fetchone()
        if not row:
            break
        writer.writerow(row)

# Close the database connection
cursor.close()
conn.close()

print(f"Table {sql_table_name} has been exported to {output_csv_file}.")