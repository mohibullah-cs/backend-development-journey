import sqlite3

# Connect to SQLite database
connection = sqlite3.connect("cookies.db")

# Create cursor
cursor = connection.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS cookies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL
)
""")

# Insert cookie records
cursor.execute("""
INSERT INTO cookies (name, price, quantity)
VALUES (?, ?, ?)
""", ("Chocolate Cookie", 250, 20))

# Save changes
connection.commit()

# Fetch all records
cursor.execute("SELECT * FROM cookies")

cookies = cursor.fetchall()

# Display records
for cookie in cookies:
    print(cookie)

# Close connection
connection.close()
