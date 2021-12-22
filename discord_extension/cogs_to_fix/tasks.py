import sqlite3 as sql 
import json
import nextcord 
import datetime
import time

from nextcord.ext import commands 
from nextcord.ext import tasks
from datetime import date

class TasksToDo(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

        self.check_exp_members.start()


    @tasks.loop(minutes=131400)
    async def check_exp_members(self):
        await self.bot.wait_until_ready()

        def days_between(today,msg_date):
            today = datetime.strptime(today, "%Y-%m-%d")
            msg_date = datetime.strptime(msg_date, "%Y-%m-%d")

            diff = abs((today-msg_date).days)

            return diff

        for guild in self.bot.guilds:
            for member in guild.members:
                if not member.bot:
                    async for message in member.history(limit=1):
                        today = datetime.today()
                        msg_date = message.created_at

                        diff = days_between(today,msg_date)

                        if diff > 90:
                            with open('./json_files/tmp_list_inactive_members.json','r',encoding='utf-8-sig') as f:
                                data = json.load(f)

                            current_members_to_kick = data[str(guild.id)].keys()

                            if member.id in current_members_to_kick:
                                pass
                            else:
                                data[str(guild.id)] = {str(len(current_members_to_kick)+1) : member.id}

                                with open('./json_files/tmp_list_inactive_members.json','a',encoding='utf-8-sig') as new:
                                    data = json.dump(data,new,indent=4)

                            embed=nextcord.Embed(
                                color=nextcord.Colour.random(),
                                timestamp=datetime.today().__format__('%m/%d/%y -- %H:%M:%S'),
                                title=f'{guild.name}s\' Member Tracker',
                                description='The Following Members Have Not Been Active In Text Channels For Atleast 90 Days.'
                            ).add_field(
                                name='Members:',
                                value=f'{[m.name for m in current_members_to_kick]}',
                                inline=False
                            ).set_thumbnail(
                                url=guild.icon_url
                            )

                            await guild.system_channel.send(embed=embed)
                            
                        else:
                            time.sleep(1)


    @tasks.loop(days=1)
    async def backup(self):
        await self.bot.wait_until_ready()

        with sql.connect('main.db') as mdb: 
            cur = mdb.cursor()

            """GET GUILDS TABLE INFO"""

            table1 = "guilds"

            for guild_id in self.bot.guilds:
                srch = 'SELECT * FROM guilds WHERE guild_id=?'
                val = (guild_id,)

                all_guild_info = cur.execute(srch, val).fetchall()

            """GET MEMBERS TABLE INFO"""

            table2 = "members"

            for guild_id in self.bot.guilds:
                for mem_id in guild_id.members:
                    if not mem_id.bot:
                        srch2 = 'SELECT * FROM members WHERE guild_id=? AND mem_id=?'
                        val2 = (guild_id,mem_id,)

                        all_member_info = cur.execute(srch2, val2).fetchall()


            """GET BANK TABLE INFO"""

            table3 = "bank"

            for guild_id in self.bot.guilds:
                srch3 = 'SELECT * FROM bank WHERE guild_id=?'
                val3 = (guild_id,)

                all_guild_bank_info = cur.execute(srch3, val3).fetchall()


            """GET NEWSLETTERS TABLE INFO"""

            table4 = "newsletters"

            for guild_id in self.bot.guilds:
                srch4 = 'SELECT * FROM newsletters WHERE guild_id=?'
                val4 = (guild_id,)

                all_guild_news_info = cur.execute(srch4, val4).fetchall()


            """GET TRANSACTIONS TABLE INFO"""

            table5 = "transactions"

            for guild_id in self.bot.guilds:
                for mem_id in guild_id.members:
                    if not mem_id.bot:
                        srch5 = 'SELECT * FROM transactions WHERE guild_id=? AND mem_id=?'
                        val5 = (guild_id,mem_id,)

                        all_mem_trans_info = cur.execute(srch5, val5).fetchall()

            """GET BADWORDS TABLE INFO"""

            table6 = "badwords"

            for guild_id in self.bot.guilds:
                srch6 = 'SELECT * FROM badwords WHERE guild_id=?'
                val6 = (guild_id,)

                all_guild_bad_words = cur.execute(srch6, val6).fetchall()


            """GET STATUSES TABLE INFO"""

            table7 = "statuses"

            for guild_id in self.bot.guilds:
                srch7 = 'SELECT * FROM statuses WHERE guild_id=?'
                val7 = (guild_id,)

                all_guild_status_info = cur.execute(srch7, val7).fetchone()

            """GET PROFILES TABLE INFO"""

            table8 = "profiles"

            for guild_id in self.bot.guilds:
                for mem_id in guild_id.members:
                    if not mem_id.bot:
                        srch8 = 'SELECT * FROM profiles WHERE guild_id=? AND mem_id=?'
                        val8 = (guild_id,mem_id,)

                        all_member_profile_info = cur.execute(srch8, val8).fetchall()

            await self.write_to_backup_file(table1,all_guild_info,table2,all_member_info,
                table3,all_guild_bank_info,table4,all_guild_news_info,table5,all_mem_trans_info,
                table6,all_guild_bad_words,table7,all_guild_status_info,table8,all_member_profile_info
            )

    async def write_to_backup_file(self,table1,all_guild_info,table2,all_member_info,table3,all_guild_bank_info,table4,all_guild_news_info,table5,all_mem_trans_info,table6,all_guild_bad_words,table7,all_guild_status_info,table8,all_member_profile_info):
        with open('backups.json','r',encoding='utf-8-sig') as f:
            data = json.load(f)

        todays_date = str(date.today().__format__('%m_%d_%y_%H_%M_%S'))


        

def setup(bot):
    bot.add_cog(TasksToDo(bot))