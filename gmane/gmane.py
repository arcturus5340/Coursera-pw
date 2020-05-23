import dateutil.parser
import re
import sqlite3
import urllib.request


conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Messages ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'sender_id INTEGER,'
            'sent_at TEXT,'
            'subject TEXT,'
            'body TEXT)')

cur.execute('CREATE TABLE IF NOT EXISTS Servers ('
            'id INTEGER PRIMARY KEY,'
            'dns TEXT UNIQUE)')

cur.execute('SELECT MAX(id) FROM Messages')
start = cur.fetchone()[0]
if start:
    start = int(start)
else:
    start = 1

message_data_list = []

cur.execute('SELECT dns FROM Servers ORDER BY id')
dns_list = [x[0] for x in cur]
dns_count = len(dns_list)
count = int(input('How many messages? '))
for i in range(start, start+count):
    if i == 60421:
        print('All emails are downloaded!')
        break
    message_data = {'sender': None, 'sent_at': None, 'subject': None, 'body': None}
    url = 'http://mbox.dr-chuck.net/sakai.devel/{}/{}'.format(i, i+1)
    html = urllib.request.urlopen(url).read().decode()
    email = re.findall('\nFrom:\s.*?<?\S+@(\S+?)>?\n', html)
    if email:
        dns = email[0]
        if dns not in dns_list:
            dns_list.append(dns)
        server_id = dns_list.index(dns)
        message_data['sender'] = server_id

    date = re.findall('\\nDate:\s(.*?)[\\n(]', html)[0]
    pdate = dateutil.parser.parse(date)
    try:
        message_data['sent_at'] = pdate.isoformat()[:7]
    except dateutil.parser.UnknownTimezoneWarning:
        continue

    message_data['subject'] = re.findall('\nSubject:(?:\sR[eE]:)*\s(.*)\n', html)[0]

    body = html.split('\n\n', 1)[1]
    body = re.sub('[^a-zA-Z]+', ' ', body)
    message_data['body'] = body

    message_data_list.append(message_data)

    if i % 100 == 0:
        for message in message_data_list:
            cur.execute('INSERT INTO Messages(sender_id, sent_at, subject, body) '
                        'VALUES (?, ?, ?, ?)', (list(message.values())))
        conn.commit()
        message_data_list = []

for message in message_data_list:
    cur.execute('INSERT INTO Messages(sender_id, sent_at, subject, body) '
                'VALUES (?, ?, ?, ?)', (list(message.values())))
    conn.commit()

for i, dns in enumerate(dns_list[dns_count:], dns_count):
    cur.execute('INSERT OR IGNORE INTO Servers(id, dns) '
                'VALUES (?, ?)', (i, dns))
    conn.commit()

conn.close()
