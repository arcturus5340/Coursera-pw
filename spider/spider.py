import re
import sqlite3
import ssl
import urllib.request

from bs4 import BeautifulSoup

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Pages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE,
    error INTEGER,
    old_rank REAL,
    new_rank REAL
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Links(
    from_id INTEGER,
    to_id INTEGER
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Webs(
    url TEXT UNIQUE 
)''')

conn.commit()

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cur.execute('SELECT url FROM Pages WHERE error IS NULL LIMIT 1')
start_url = cur.fetchone()

if start_url is not None:
    print('Restarting existing crawl. Use spreset.py to start a fresh crawl.')
    start_url = str(start_url[0])
else:
    input_url = input('Enter wikipedia second-level domain ("en" by default): ') or 'en'
    try:
        urllib.request.urlopen('https://{}.wikipedia.org/'.format(input_url), context=ctx)
        start_url = MAIN_URL = 'https://{}.wikipedia.org/'.format(input_url)
    except:
        print('Incorrect domain format entered. Script shutdown..')
        exit()
    cur.execute('INSERT OR IGNORE INTO Pages(url, error) VALUES (?, ?)', (start_url, 200))
    cur.execute('INSERT OR IGNORE INTO Webs(url) VALUES (?)', (start_url, ))
    conn.commit()

cur.execute('SELECT url FROM Webs')
webs = []
for url in cur.fetchall():
    webs.append(str(url[0]))

print(webs)

pages_count = int(input('How many pages? '))
# pages_count = 1
while (pages_count > 0) and (start_url is not None):
    html = urllib.request.urlopen(start_url, context=ctx).read().decode()
    soup = BeautifulSoup(html, 'html.parser')
    raw_links = {tag.get('href').strip('/') for tag in soup('a') if tag.get('href') is not None}
    formatted_links = {MAIN_URL+link for link in raw_links if link.startswith('wiki/') and link.find(':') == -1}

    for link in formatted_links:
        try:
            urllib.request.urlopen(link, context=ctx)
        except:
            continue
        cur.execute('INSERT OR IGNORE INTO Pages(url) VALUES (?)', (link,))
        cur.execute('INSERT OR IGNORE INTO Webs(url) VALUES (?)', (link,))
        conn.commit()

    cur.execute('UPDATE Pages SET error = ? WHERE url = ?', (200, start_url,))
    cur.execute('SELECT url FROM Pages WHERE error IS NULL LIMIT 1')
    start_url = str(cur.fetchone()[0])
    print('.')
    pages_count -= 1

conn.commit()
conn.close()

