import sqlite3

connection = sqlite3.connect("students.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER
)
""")

cursor.execute(
    "INSERT INTO students (name, age) VALUES (?, ?)",
    ("Ali", 22)
)

cursor.execute(
    "INSERT INTO students (name, age) VALUES (?, ?)",
    ("Ahmed", 23)
)

connection.commit()

cursor.execute("SELECT * FROM students")

for student in cursor.fetchall():
    print(student)

connection.close()
