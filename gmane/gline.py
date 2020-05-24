import sqlite3


conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

cur.execute('SELECT dns, sent_at FROM Messages JOIN Servers ON Messages.sender_id = Servers.id')

date_dict = {}
dns_dict = {}
for dns, date in cur:
    dns_dict[dns] = dns_dict.get(dns, 0) + 1
    dns_dict = date_dict.get(date, dict())
    dns_dict[dns] = dns_dict.get(dns, 0) + 1
    date_dict[date] = dns_dict

dns_list = sorted(dns_dict.keys(), key=dns_dict.get, reverse=True)[:10]
fhandle = open('gline.js', 'w')
print('gline = [', file=fhandle)
print('[ "Year",', ', '.join(list('"'+x+'"' for x in dns_list)), '],', file=fhandle)
for k in date_dict:
    print('[ "{}",'.format(k), ', '.join([str(date_dict[k].get(dns, 0)) for dns in dns_list]), '],', file=fhandle)
print('];', file=fhandle)

conn.close()
