import sqlite3
import pandas as pd
import os

# Create output folder
output_folder = 'output_csv'
os.makedirs(output_folder, exist_ok=True)

# Connect to the database
conn = sqlite3.connect('employee_management.db')

# List of tables
tables = ['Department', 'Position', 'Employee', 'Attendance', 'LeaveRequest', 'Payroll']

# Export each table to CSV
for table in tables:
    df = pd.read_sql_query(f"SELECT * FROM {table};", conn)
    file_path = os.path.join(output_folder, f"{table}.csv")
    df.to_csv(file_path, index=False)
    print(f"✅ {table}.csv created successfully at {file_path}")

conn.close()

print("\nAll tables exported to CSV in 'output_csv' folder.")
