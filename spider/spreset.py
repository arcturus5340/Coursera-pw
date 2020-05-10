import sqlite3


conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Pages')
cur.execute('DROP TABLE IF EXISTS Links')
cur.execute('DROP TABLE IF EXISTS Webs')

conn.commit()
conn.close()
