import sqlite3
import json
import requests
import time

def handle_input():
    #Used to take Codeforces handle of the user

    username1 = raw_input('Enter first handle: ')
    username2 = raw_input('Enter second handle: ')
    return (username1, username2)


def getdata_user(handle):
    #Used to extract rating and contest information of user

    #global results_user1
    parameters = {"handle": handle}
    r = requests.get(user_rating_url, params = parameters)
    userating = json.loads(r.content)
    results_user1 = userating["result"]
    return results_user1


#global results_user1, results_user2
user_rating_url = 'http://www.codeforces.com/api/user.rating?'
user_info_url = 'http://www.codeforces.com/api/user.info?handles='

# Conecting to the Contest database
conn_contestdb = sqlite3.connect('Codeforces Comparison.sqlite')
cur_contestdb = conn_contestdb.cursor()

# Connecting to the UsersDB database
conn = sqlite3.connect('UsersDB.sqlite')
cur = conn.cursor()

# Creating the Tables
cur.executescript('''
DROP TABLE IF EXISTS User1;
DROP TABLE IF EXISTS User2;

CREATE TABLE User1 (
    contest_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    oldRating INTEGER,
    newRating INTEGER,
    rank INTEGER
);

CREATE TABLE User2 (
    contest_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    oldRating INTEGER,
    newRating INTEGER,
    rank INTEGER
);

''')

results_users = [None]*2

# Calls handle_input and stores the relevant data of each user
while True:
    handles = ';'.join(handle_input())
    r = requests.get(user_info_url + str(handles))
    userinfo = json.loads(r.content)
    #print json.dumps(userinfo, indent = 4)
    if userinfo["status"] == 'OK':
        results_users[0] = getdata_user(userinfo["result"][0]["handle"])
        results_users[1] = getdata_user(userinfo["result"][1]["handle"])
        break

print json.dumps(results_users[0], indent = 4)
print '\n\n\n'
print json.dumps(results_users[1], indent = 4)

# Adding the data to corresponding tables of the users
for item in xrange(2):
    for result in results_users[item]:
        contestName = result["contestName"]
        oldRating = result["oldRating"]
        newRating = result["newRating"]
        rank = result["rank"]

        # print contestName, oldRating, newRating, rank

        cur_contestdb.execute('''SELECT id FROM ContestDB
                    WHERE name = (?)''', (contestName, ))
        contestid = cur_contestdb.fetchone()[0]

        if item == 0:
            cur.execute('''INSERT INTO User1 VALUES (?, ?, ?, ?)''',
                        (contestid, oldRating, newRating, rank))
        else:
            cur.execute('''INSERT INTO User2 VALUES (?, ?, ?, ?)''',
                        (contestid, oldRating, newRating, rank))
        conn.commit()
    print '\n\n\n'


# Closing both the connections
conn.close()
conn_contestdb.close()
