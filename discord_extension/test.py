link_to_invite_bot = "https://discord.com/oauth2/authorize?client_id=847975528454422548&permissions=8&scope=bot%20applications.commands"

"""
TESTING DATETIME FOR VARIOUS FORMATS
"""
# import calendar

# from datetime import date, datetime, timedelta

# today = date.today()

# start = today - timedelta(days=today.weekday())
# end = start + timedelta(days=6)

# print(today, calendar.day_name[today.weekday()])
# print(start, calendar.day_name[start.weekday()])
# print(end, calendar.day_name[end.weekday()])
# print('\n')
# print('\n')
# print(f'{calendar.day_name[start.weekday()]},{start.__format__("%m/%d/%y")} through {calendar.day_name[end.weekday()]}, {end.__format__("%m/%d/%y")}')

"""
TESTING MESSAGE COUNT COUNTER
"""

# import sqlite3 as sql

# with sql.connect('main.db') as mdb:
#     cur = mdb.cursor()

#     srch = 'SELECT * FROM members WHERE guild_id=? AND mem_id=?'
#     val = (779290532622893057,260009824945831936,)

#     results = cur.execute(srch, val).fetchall()

#     for row in results:
#         print(row)

# import sqlite3 as sql

# with sql.connect('main.db') as mdb:
#     cur = mdb.cursor()

#     srch = 'SELECT message_count FROM members WHERE guild_id=? AND mem_id=?'
#     val = (779290532622893057, 260009824945831936)

#     curr_msg_count = cur.execute(srch, val).fetchone()

#     print(type(curr_msg_count))

#     new_bal = curr_msg_count[0] + 1

#     print(type(new_bal))

#     srch2 = 'UPDATE members SET message_count=? WHERE guild_id=? AND mem_id=?'
#     val2 = (779290532622893057, 260009824945831936, new_bal)

#    cur.execute(srch2,val2)

"""
CREATING BAD WORD LIST
SPLITTING LIST
WRITING TO DATABASE
IDK
"""

# words = "bad suck fuck tit coochie dick penis boobs sex lick"

# for word in words.split(' '):
#     print(word)

# import sqlite3 as sql

# with sql.connect('main.db') as mdb:
#     cur = mdb.cursor()

#     curr_count = cur.execute('SELECT guild_count FROM botInfo').fetchone()

#     print(curr_count)

    # new_count = curr_count[0] + 1

"""
LOGGING
"""

# import logging
# import datetime
# from time import sleep

# today_date = datetime.date.today().strftime('%m-%d-%y')
# logging.basicConfig(level=logging.DEBUG, filename=today_date, filemode='a', format='%(name)s - %(levelname)s - %(message)s')

# for a in range(10):
#     logging.info(f"The loop has made it {a + 1} times through the loop")
#     if a == 5:
#         logging.critical(f"THIS IS {a}!!!! AHHHH!")

# logging.warning("Your loop is complete.")

"""
Use the weekday() Method to Get the Name of the Day in Python
Use the isoweekday() Method to Get the Name of the Day in Python
Use the calendar Module to Get the Name of the Day in Python
Use the strftime() Method to Get the Name of the Day in Python
"""

#from datetime import datetime, date, timedelta
#import calendar

#print(datetime.today().weekday())
#prints 6

#print(datetime.today().isoweekday())
#prints 7

# curr_date = date.today()
# tomorrow = curr_date + timedelta(days=1)
# monday = curr_date - timedelta(days=6)
# print(calendar.day_name[curr_date.weekday()])
# print(calendar.day_name[tomorrow.weekday()])
# print(calendar.day_name[monday.weekday()])
#prints Sunday

#print(datetime.today().strftime('%A'))
#prints Sunday

#print(calendar.day_name[date.today().weekday()])

"""
TESTING ALGORYTHM FOR REWARDS ON HIDDEN WORDS FOUND
"""

# test_string = "This is a test string"

# hidden_words = ["this","a","string"]

# len_of_words_total = 0

# for word in test_string.split():
#     if word in hidden_words:
#         len_of_words_total += len(word)

# awarded_balance = len_of_words_total/100

# print(awarded_balance)


"""
LOOPING THROUGH JSON FILE
TO SHOW ALL INFORMATION
"""

# import json

# with open('./master.json','r',encoding='utf-8-sig') as f:
#     data = json.load(f)

# for a in data.keys():
#     for b in data[a].keys():
#         print(a,b)


import sqlite3 as sql 

with sql.connect('./main.db') as mdb:
    cur = mdb.cursor()
    
    guild_count = cur.execute('SELECT guild_count FROM botInfo').fetchone()
    
    new_count = guild_count[0] + 1
    
    print(new_count)