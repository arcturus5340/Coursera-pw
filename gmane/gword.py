import sqlite3


conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

cur.execute('SELECT subject, body FROM Messages')

big_dict = {}
for row in cur:
    for text in row:
        for word in text.split():
            if len(word) < 5: continue
            big_dict[word.lower()] = big_dict.get(word.lower(), 0) + 1

max_count = max(big_dict.values())
min_count = min(big_dict.values())

fhandle = open('gword.js', 'w')
print('gword = [', file=fhandle)
for k in sorted(big_dict, key=big_dict.get, reverse=True)[:300]:
    size = int((big_dict[k] - min_count) / float(max_count - min_count) * 80 + 20)
    print('{{text: "{}", size: {}}},'.format(k, size), file=fhandle)
print('];', file=fhandle)

conn.close()
