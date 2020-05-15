import sqlite3


conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('SELECT COUNT(*) FROM Pages')
elem_count = cur.fetchone()[0]

cur.execute('SELECT id FROM Pages')
rating = dict()
new_rating = dict()
for id in cur:
    rating[id[0]] = 1/elem_count
    new_rating[id[0]] = 0.0

cur.execute('SELECT from_id, to_id FROM Links')
links = dict()
for from_id, to_id in cur:
    val = links.get(int(from_id), list())
    val.append(to_id)
    links[int(from_id)] = val

for node in rating:
    incoming_edges = []
    for link in links:
        if node in links[link]: incoming_edges.append(link)

    r = (1-0.85)/elem_count + 0.85*sum(rating[edge]/len(links[edge]) for edge in incoming_edges)
    new_rating[node] = r

new_rating = {node: r/sum(new_rating.values()) for node, r in new_rating.items()}

for node, r in new_rating.items():
    cur.execute('UPDATE Pages SET rank = ? WHERE id = ?', (r, node))

conn.commit()
cur.close()