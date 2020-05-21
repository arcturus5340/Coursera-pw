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
            'dns TEXT)')

cur.execute('SELECT MAX(id) FROM Messages')
start = cur.fetchone()[0]
if start:
    start = int(start)
else:
    start = 1

message_data_list = []
dns_list = []
count = int(input('How many messages? '))
for i in range(start, start+count):
    message_data = {'sender': None, 'sent_at': None, 'subject': None, 'body': None}
    url = 'http://mbox.dr-chuck.net/sakai.devel/{}/{}'.format(i, i+1)
    html = urllib.request.urlopen(url).read().decode()
    email = re.findall('\\nFrom: .*? <\S+@(\S+)>\\n', html)
    if email:
        dns = email[0]
        if dns not in dns_list:
            dns_list.append(dns)
        id = dns_list.index(dns)
        message_data['sender'] = id

    date = re.findall('\\nDate: (.*?)[\\n(]', html)[0]
    pdate = dateutil.parser.parse(date)
    message_data['sent_at'] = pdate.isoformat()[:7]

    message_data['subject'] = re.findall('\nSubject:(?:\sR[eE]:)*\s(.*)\n', html)[0]

    body = html.split('\n\n', 1)[1]
    body = re.sub('[^a-zA-Z]+', ' ', body)
    message_data['body'] = body

    message_data_list.append(message_data)
    conn.commit()

for message in message_data_list:
    cur.execute('INSERT INTO Messages(sender_id, sent_at, subject, body) '
                'VALUES (?, ?, ?, ?)', (list(message.values())))
    conn.commit()

for i, dns in enumerate(dns_list):
    cur.execute('INSERT INTO Servers(id, dns) '
                'VALUES (?, ?)', (i, dns))
    conn.commit()

conn.close()