import dateutil.parser
import re
import sqlite3
import urllib.request


conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Messages ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'sender_server TEXT,'
            'sender_name TEXT,'
            'sender_username TEXT,'
            'recipient_server TEXT,'
            'recipient_name TEXT,'
            'recipient_username TEXT,'
            'sent_at TEXT,'
            'subject TEXT,'
            'body TEXT)')

cur.execute('CREATE TABLE IF NOT EXISTS Senders ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'name TEXT,'
            'username TEXT,'
            'server TEXT)')

cur.execute('CREATE TABLE IF NOT EXISTS Recipients ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'name TEXT,'
            'username TEXT,'
            'server TEXT)')


cur.execute('SELECT MAX(id) FROM Messages')
start = cur.fetchone()[0]
if start:
    start = int(start)
else:
    start = 1

message_data_list = []
count = int(input('How many messages? '))
for i in range(start, start+count):
    message_data = {'sender': None, 'recipient': None, 'sent_at': None, 'subject': None}
    url = 'http://mbox.dr-chuck.net/sakai.devel/{}/{}'.format(i, i+1)
    html = urllib.request.urlopen(url).read().decode()
    email = re.findall('\\nFrom: (.*?) <(\S+)@(\S+)>\\n', html)
    if email:
        data = [field.strip('"') for field in email[0]]
        message_data['sender'] = data
    email = re.findall('\\nTo: (.*?) <(\S+)@(\S+)>\\n', html)
    if email:
        data = [field.strip('"') for field in email[0]]
        message_data['recipient'] = data

    date = re.findall('\\nDate: (.*?)[\\n(]', html)[0]
    pdate = dateutil.parser.parse(date)
    message_data['sent_at'] = pdate.isoformat()[:7]

    message_data['subject'] = re.findall('\nSubject:(?:\sR[eE]:)*\s(.*)\n', html)[0]

    message_data['body'] = html.split('\n\n', 1)[1]

    message_data_list.append(message_data)
    conn.commit()

print(message_data_list)
conn.close()