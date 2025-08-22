import sqlite3
conn = sqlite3.connect('violations.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM violations")
rows = cursor.fetchall()
print(f"Total violations recorded: {len(rows)}")
for row in rows:
    print(row)
conn.close()
