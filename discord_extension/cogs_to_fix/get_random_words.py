import sqlite3 as sql 
import nextcord 
import asyncio
import json

from datetime import datetime,timedelta,date
from nextcord.ext import commands, tasks
from time import sleep

class ScheduledEvents(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.get_words.start()

    
    @tasks.loop()
    async def get_words(self):
        await self.bot.wait_until_ready()

        # change loop below to counter = 0 and while counter != 0 with a step counter for testing

        while date.today().weekday() == 0:
            sleep(1)
        else:
            with sql.connect('main.db') as mdb:
                cur = mdb.cursor()

                all_words = cur.execute('SELECT * FROM randomWords').fetchall()

                for word in all_words:
                    srch = 'SELECT status FROM randomWords WHERE word=?'
                    val = (word,)

                    curr_status = cur.execute(srch, val).fetchone()

                    if curr_status == "in-use":
                        srch2 = 'UPDATE randomWords SET status=? WHERE word=?'
                        val2 = (word,"used",)

                        cur.execute(srch2, val2)

                        await self.get_list()


    async def get_list(self):
        new_list = []
        counter = 200

        while counter != 0:
            new_word = r.get_random_word()
            new_list.append(new_word)
        else:
            with sql.connect('main.db') as mdb:
                cur = mdb.cursor()

                for nw in new_list:
                    srch3 = 'INSERT INTO randomWords(word,status) VALUES (?,?)'
                    val3 = (nw,"in-use",)

                    cur.execute(srch3, val3)


    @tasks.loop()
    async def clean_myst_word_list(self):
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()