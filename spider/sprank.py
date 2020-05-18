import sqlite3


conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('SELECT COUNT(*) FROM Pages')
elem_count = cur.fetchone()[0]

cur.execute('SELECT id, rank FROM Pages')
rating = dict()
new_rating = dict()
for id, rank in cur:
    rating[id] = rank or (1/elem_count)
    new_rating[id] = 0.0

cur.execute('SELECT from_id, to_id FROM Links')
links = dict()
for from_id, to_id in cur:
    val = links.get(int(from_id), list())
    val.append(to_id)
    links[int(from_id)] = val

cycle_count = int(input('Enter the number of cycles to calculate ranks: '))
for i in range(cycle_count):
    for node in rating:
        incoming_edges = []
        for link in links:
            if node in links[link]: incoming_edges.append(link)

        r = (1-0.85)/elem_count + 0.85*sum(rating[edge]/len(links[edge]) for edge in incoming_edges)
        new_rating[node] = r
    rating = new_rating.copy()

for node, r in new_rating.items():
    cur.execute('UPDATE Pages SET rank = ? WHERE id = ?', (r, node))

print('Done. Run spjson.py')
conn.commit()
cur.close()