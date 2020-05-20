import dateutil.parser
import re
import sqlite3
import urllib.request


conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Messages ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'email TEXT,'
            'sent_at TEXT,'
            'subject TEXT,'
            'header TEXT,'
            'body TEXT)')

cur.execute('SELECT MAX(id) FROM Messages')
start = cur.fetchone()[0]
if start:
    start = int(start)
else:
    start = 1

count = int(input('How many messages? '))
for i in range(start, start+count):
    url = 'http://mbox.dr-chuck.net/sakai.devel/{}/{}'.format(i, i+1)
    html = urllib.request.urlopen(url).read().decode()
    email = re.findall('\\nFrom: .*? <(\S+@\S+)>\\n', html)
    if email:
        email = email[0]
    else:
        email = re.findall('\\nFrom: (.*?)\\n', html)[0]

    date = re.findall('\\nDate: (.*?)[\\n(]', html)[0]
    pdate = dateutil.parser.parse(date)
    formatted_data = pdate.isoformat()

    subject = re.findall('\\nSubject: (.*)\\n', html)[0]

    header, body = html.split('\n\n', 1)
    cur.execute('INSERT INTO Messages(email, sent_at, subject, header, body)'
                'VALUES (?, ?, ?, ?, ?)', (email, formatted_data, subject, header, body))

    conn.commit()