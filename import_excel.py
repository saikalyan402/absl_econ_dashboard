import pandas as pd
import sqlite3
import os

# Define file paths
excel_file = "BOOK TO TABLE.xlsx"
db_file = "dashboard.db"

# Connect to the SQLite database
conn = sqlite3.connect(db_file)

try:
    # Read the excel file
    print(f"Reading {excel_file}...")
    df = pd.read_excel(excel_file)
    print("Columns found:")
    print(df.columns.tolist())
    
    # Save it to the database table "economic_indicators"
    # User said "make it as table 2 named economic indicators in db"
    # I will replace if exists to be safe, or just insert
    df.to_sql("economic_indicators", conn, if_exists="replace", index=False)
    
    print("Successfully imported data into the 'economic_indicators' table in dashboard.db!")
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
