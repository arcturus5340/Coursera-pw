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
    rank REAL
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Links(
    from_id, to_id INTEGER,
    UNIQUE(from_id, to_id) 
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Webs(
    url TEXT UNIQUE 
)''')

conn.commit()

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cur.execute('SELECT id, url FROM Pages WHERE error ISNULL LIMIT 1')
fetched = cur.fetchone()

if not fetched:
    LANG = input('Enter wikipedia second-level domain ("en" by default): ') or 'en'
    if urllib.request.urlopen('https://{}.wikipedia.org/wiki/Main_Page'.format(LANG), context=ctx).getcode() != 200:
        print('Incorrect domain format entered. Script shutdown..')
        exit()

    from_id = 1
    start_url = 'https://{}.wikipedia.org/wiki/Main_Page'.format(LANG)

    cur.execute('INSERT OR IGNORE INTO Pages(url, error) VALUES (?, ?)', (start_url, 200))
    cur.execute('INSERT OR IGNORE INTO Webs(url) VALUES (?)', (start_url, ))
    conn.commit()
else:
    from_id, start_url = fetched
    print('Restarting existing crawl...')
    LANG = re.findall('^https://(.+).wikipedia\.org.*', start_url)[0]

MAIN_URL = 'https://{}.wikipedia.org/'.format(LANG)

pages_count = int(input('How many pages? '))
while (pages_count > 0) and (start_url is not None):
    html = urllib.request.urlopen(start_url, context=ctx).read().decode()
    soup = BeautifulSoup(html, 'html.parser')
    raw_links = {tag.get('href').strip('/') for tag in soup('a') if tag.get('href') is not None}
    formatted_links = {MAIN_URL+link for link in raw_links if link.startswith('wiki/') and link.find(':') == -1}

    for link in formatted_links:
        if urllib.request.urlopen(link, context=ctx).getcode() != 200: continue
        cur.execute('SELECT id FROM Pages WHERE url = ?', (link,))
        to_id = cur.fetchone()
        if to_id and (from_id != int(to_id[0])):
            cur.execute('INSERT OR IGNORE INTO Links(from_id, to_id) VALUES (?, ?)', (from_id, int(to_id[0])))
        else:
            cur.execute('INSERT OR IGNORE INTO Pages(url) VALUES (?)', (link, ))
            to_id = cur.lastrowid
            cur.execute('INSERT OR IGNORE INTO Webs(url) VALUES (?)', (link,))
            cur.execute('INSERT OR IGNORE INTO Links(from_id, to_id) VALUES (?, ?)', (from_id, to_id))
        conn.commit()

    cur.execute('UPDATE Pages SET error = ? WHERE url = ?', (200, start_url,))
    cur.execute('SELECT id, url FROM Pages WHERE error IS NULL LIMIT 1')
    from_id, start_url = cur.fetchone()
    print('.')
    pages_count -= 1

conn.commit()
conn.close()
