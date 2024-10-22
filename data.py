import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('gemini_items.db')
cursor = conn.cursor()

# Query and print all records from the responses table
print("Responses:")
cursor.execute('SELECT * FROM responses')
rows = cursor.fetchall()
for row in rows:
    print(row)
    print("\n\n")

# Query and print all records from the items table
print("\nItems:")
cursor.execute('SELECT * FROM items')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
