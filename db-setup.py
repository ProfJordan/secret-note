import sqlite3

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('secret.db')

# Create a cursor object using the cursor method of the connection
cursor = conn.cursor()

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS notes
             (id TEXT PRIMARY KEY, message TEXT, password TEXT, salt TEXT)''')

# Commit the changes and close the connection
conn.commit()
conn.close()
