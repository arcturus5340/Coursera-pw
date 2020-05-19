import sqlite3


conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('SELECT COUNT(rank) FROM Pages WHERE rank ISNULL')
if cur.fetchone()[0] != 0:
    print('Start sprank.py first')
    quit()

cur.execute('SELECT COUNT(from_id) AS weight, rank, id, url FROM Pages JOIN Links ON id = from_id GROUP BY id')

fhandle = open('spider.js', 'w')
print('spiderJson = {"nodes":[', file=fhandle)
for row in cur:
    print('{{"weight": {}, "rank": {}, "id": {}, "url": "{}"}},'.format(*row), file=fhandle)
print('],', file=fhandle)

cur.execute('SELECT from_id, to_id FROM Links')

print('"links":[', file=fhandle)
for row in cur:
    print('{{"source": {}, "target": {}, "value": 1 }},'.format(*row), file=fhandle)
print(']};', file=fhandle)

conn.close()
