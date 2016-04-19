import requests
import json
import time
import sqlite3

# Connecting to the database
conn = sqlite3.connect('Codeforces Comparison.sqlite')
cur = conn.cursor()

# Creating the table
cur.executescript('''
DROP TABLE IF EXISTS ContestDB;
CREATE TABLE ContestDB (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT,
    start datetime
);
''')

url = 'http://www.codeforces.com/api/contest.list'
try:
    r = requests.get(url)
except:
    print 'Wrong URL'

json_data = json.loads(r.content)
results = json_data["result"]
print json.dumps(results, indent = 4)

# Storing the results in the database
for result in results:
    try:
        name = result["name"]
        index = result["id"]
        start_Seconds = result["startTimeSeconds"]
    except:
        continue

    cur.execute('''INSERT INTO ContestDB (id, name, start)
                VALUES (?, ?, ?)''', (index, name, start_Seconds))

    conn.commit()


conn.close()
#print time.ctime(json_data["result"][3]["startTimeSeconds"])
