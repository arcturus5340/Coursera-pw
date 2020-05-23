import sqlite3


conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()
cur.execute('SELECT dns, sent_at, subject FROM Messages JOIN Servers ON Messages.sender_id = Servers.id')

for row in cur:
    print(row)

conn.close()
