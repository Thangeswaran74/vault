import sqlite3
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# Specify the path to your SQLite database file inside the "instance" folder
DB_FILE_PATH = os.path.join(APP_ROOT, '../instance', 'vault.db')
path=DB_FILE_PATH
def create_table(username):
    conn = sqlite3.connect(path)
    c = conn.cursor()

    # Create table based on username
    c.execute(f'''CREATE TABLE IF NOT EXISTS {username} (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    email_address TEXT,
                    website TEXT,
                    password TEXT
                )''')
    conn.commit()
    conn.close()

def insert(user1,username,email,website,password):
    conn = sqlite3.connect(path)
    if username!=None:
        sql = f'''INSERT INTO {user1} (username, email_address,website,password)
         VALUES (?, ? , ? , ?)'''
        cursor = conn.cursor()
# Execute the SQL statement with the data
        cursor.execute(sql, (username, email,website,password))
    

# Commit the transaction
    conn.commit()

# Close the connection
    conn.close()
