import sqlite3


conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('SELECT COUNT(from_id) AS inbound, rank, id, url FROM Pages JOIN Links ON id = from_id '
            'GROUP BY id ORDER BY inbound DESC')

for row in cur:
    print(row)

conn.close()