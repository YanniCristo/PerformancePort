import sqlite3
conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute("SELECT * FROM Subscription")

# nomi delle colonne
columns = [desc[0] for desc in c.description]

# dati
rows = c.fetchall()

print(columns)
for row in rows:
    print(row)

conn.close()
