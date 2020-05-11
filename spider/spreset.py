import sqlite3


conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('UPDATE Pages SET old_rank=0.0, new_rank=1.0')
print('All pages set to a rank of 1.0')

conn.commit()
conn.close()
