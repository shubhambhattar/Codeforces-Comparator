import sqlite3
import time
import matplotlib.pyplot as plt

# Connect to the UsersDB database
conn_usersdb = sqlite3.connect('UsersDB.sqlite')
cur_usersdb = conn_usersdb.cursor()

# cur_usersdb.executescript('''
# DROP TABLE IF EXISTS PlotTable;
#
# CREATE TABLE PlotTable (
#     contest_id INTEGER,
#     rating_user1 INTEGER,
#     rating_user2 INTEGER
# );
# ''')

# Extracting the data of the first User
cur_usersdb.execute('''SELECT contest_id, newRating FROM User1''')
user1_data = cur_usersdb.fetchall()

# Splitting contest_id's and ratings
contest_data1 = [data[0] for data in user1_data]
rating_data1 = [data[1] for data in user1_data]

# Extracting the data of the second User
cur_usersdb.execute('''SELECT contest_id, newRating FROM User2''')
user2_data = cur_usersdb.fetchall()

# Splitting contest_id's and ratings
contest_data2 = [data[0] for data in user2_data]
rating_data2 = [data[1] for data in user2_data]

# Plotting the details of the first User
plt.plot(contest_data1, rating_data1, color = 'k', linestyle = '-',
        marker = 'o', markerfacecolor = 'k', linewidth = 1.5,
        label = 'User1')

# Plotting the details of the second User
plt.plot(contest_data2, rating_data2, color = 'r', linestyle = '-',
        marker = 'o', markerfacecolor = 'r', linewidth = 1.5,
        label = 'User2')

# Plot Figure settings
plt.grid(True)
my_plot = plt.gca()

# Userful labels in graph
plt.xlabel('Contest id\'s')
plt.ylabel('Rating')
plt.title('Codeforces User Comparison with Rating Graph')

# Getting the legent outside by shrinking the main box to 80% of its size
box = my_plot.get_position()
my_plot.set_position([box.x0, box.y0, box.width * 0.85, box.height])
plt.legend(loc = 'center left', bbox_to_anchor = (1, 0.5))

# Autoscaling the view
my_plot.autoscale_view(tight = None, scalex = 'True', scaley = 'True')

plt.show()


# for data in user1_data:
#     cur_usersdb.execute('''INSERT INTO PlotTable (contest_id, rating_user1)
#                         VALUES (?, ?)''', data)
#     conn_usersdb.commit()
#
# cur_usersdb.execute('''SELECT contest_id, newRating FROM User2''')
# user2_data = cur_usersdb.fetchall()
#
# for data in user2_data:
#     #cur_usersdb.execute('''SELECT contest_id FROM PlotTable
#     #                    WHERE ''')
#     cur_usersdb.execute('''INSERT OR IGNORE INTO PlotTable (contest_id)
#                         VALUES (?)''', (data[0],))
#     cur_usersdb.execute('''UPDATE PlotTable SET rating_user2 = ?
#                         WHERE contest_id = ?''', (data[1], data[0]))
#     conn_usersdb.commit()
#
# cur_usersdb.execute('SELECT * FROM PlotTable')
# all_data = cur_usersdb.fetchall()
# all_data = sorted(all_data)
# for data in all_data:
#     print data
# #print all_data
# all_user1_data = [(data[0], data[1]) for data in all_data]
# all_user2_data = [(data[0], data[2]) for data in all_data]
#
# #for data in all_data:
# #    print data
#
# contest_data = [data[0] for data in all_data]
# user1_data = [data[1] for data in all_data]
# user2_data = [data[2] for data in all_data]

# plt.plot(contest_data, user1_data, color = 'k', linestyle = '-',
#             marker = 'o', markerfacecolor = 'k', label = 'user1')
# plt.plot(contest_data, user2_data, label = 'user2')
# plt.xlabel('Contest id\'s')
# plt.ylabel('Rating')
# plt.title('Codeforces User Comparison with Rating Graph')
# plt.legend()
#
# plt.show()

# Closing the connection
conn_usersdb.close()
