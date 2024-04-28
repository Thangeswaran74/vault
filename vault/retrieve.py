import sqlite3
import os
from vault.encdec import decrypt

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

DB_FILE_PATH = os.path.join(APP_ROOT, '../instance', 'vault.db')

def show(username,passw):
    conn=sqlite3.connect(DB_FILE_PATH)
# Create a cursor object
    cursor = conn.cursor()

# Execute a SELECT query
    cursor.execute(f"SELECT * FROM {username} WHERE username IS NOT NULL")  # Replace 'your_table' with the name of your table

# Fetch all rows from the result set
    rows = cursor.fetchall()
    rows_lists = [list(row) for row in rows]
# Print the retrieved data 
    for i in rows_lists:
        b=decrypt(i[4],password=passw)
        i[4]=b

# Close the cursor and connection  
    cursor.close()
    conn.close()
    return rows_lists
