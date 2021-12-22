import asyncio
import sqlite3 as sql
import nextcord

from nextcord.ext import commands
from datetime import date

class CogListeners(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    
    @commands.Cog.listener()
    async def on_message(self,message):
        with sql.connect('./discord_extension/main.db') as mdb:
            cur = mdb.cursor()

            support = cur.execute('SELECT supp_disc_info FROM botInfo').fetchone()

            if not message.author.bot:
                if message.content.startswith('_prefix'):
                    msg = await message.channel.send(f'My Prefix Is: {cp}')
                    await asyncio.sleep(10)
                    await msg.delete()

                    srch = 'SELECT message_count FROM members WHERE guild_id=? AND mem_id=?'
                    val = (message.guild.id,message.author.id,)

                    curr_count = cur.execute(srch, val)

                    new_count = curr_count[0] + 1

                    srch2 = 'UPDATE members SET message_count=? WHERE guild_id=? AND mem_id=?'
                    
                    cur.execute(srch2, val)


                elif message.content.startswith('_support'):
                    msg = await message.channel.send(f'Support Discord: {support}')
                    await asyncio.sleep(10)
                    await msg.delete()

                    srch = 'SELECT message_count FROM members WHERE guild_id=? AND mem_id=?'
                    val = (message.guild.id,message.author.id,)

                    curr_count = cur.execute(srch, val).fetchone()

                    new_count = curr_count[0] + 1 

                    srch2 = 'UPDATE members SET message_count=? WHERE guild_id=? AND mem_id=?'
                    val2 = (message.guild.id,message.author.id,new_count)

                    cur.execute(srch2, val2)
                    
                elif message.content.startswith('#GBot'):
                    question = 'SELECT message_count FROM membes WHERE guild_id=? AND mem_id=?'
                    q_val = (message.guild.id,message.author.id,)

                    curr_count = cur.execute(question, q_val).fetchone()

                    new_count = curr_count[0] + 1

                    question2 = 'UPDATE members SET message_count=? WHERE guild_id=? AND mem_id=?'
                    q_val2 = (message.guild.id,message.author.id,new_count)

                    hash_count = cur.execute('SELECT hash_count FROM botInfo').fetchone()

                    new_hash_count = hash_count[0] + 1 

                    question3 = 'UPDATE botInfo SET hash_count=?'
                    q_val3 = (message.guild.id,message.author.id,new_hash_count)

                    cur.execute(question3, q_val3)

                else:
                    """
                    UPDATING MESSAGE COUNT
                    """

                    srch = 'SELECT message_count FROM members WHERE guild_id=? AND mem_id=?'
                    val = (message.guild.id,message.author.id,)

                    curr_msg_count = cur.execute(srch, val).fetchone()

                    new_count = curr_msg_count[0] + 1

                    srch2 = 'UPDATE members SET message_count=? WHERE guild_id=? AND mem_id=?'
                    val2 = (message.guild.id,message.author.id,new_count)

                    cur.execute(srch2, val2)

                    """
                    GETTING REWARDS FOR HIDDEN WORDS FOUND
                    """

                    srch3 = 'SELECT balance FROM members WHERE guild_id=? AND mem_id=?'
                    val3 = (message.guild.id,message.author.id,)

                    msg_author_curr_bal = cur.execute(srch3, val3).fetchone()

                    all_words = cur.execute('SELECT word FROM randomWords').fetchall()

                    len_of_words_total = 0

                    hidden_words_found = []

                    for word in message.content.lower():
                        if word in all_words:
                            len_of_words_total += len(word)
                            hidden_words_found.append(word)

                    awarded_balance = len_of_words_total/100

                    new_balance = msg_author_curr_bal + awarded_balance

                    embed=nextcord.Embed(
                        color=nextcord.Colour.random(),
                        timestamp=message.created_at,
                        title=f'{message.guild.name}s\' Random Word Finder',
                        description=f'''{message.author.name} You Found The Hidden Words: ```{" ".join(hidden_words_found)}```'''
                    ).add_field(
                        name='Details',
                        value=f'''Member Current Balance: ${msg_author_curr_bal}
                                  Member New Balance: ${new_balance}
                                  Awarded Balance: ${awarded_balance}''',
                        inline=False
                    ).set_thumbnail(
                        url=message.guild.icon_url
                    )

                    await message.author.send(embed=embed)

                    srch4 = 'INSERT INTO transactions(guild_id,sender,receiver,amount,date) VALUES (?,?,?,?,?)'
                    val4 = (message.guild.id,self.bot.user.id,message.author.id,awarded_balance,str(date.today().__format__('%m/%d/%y -- %H:%M:%S')))

                    cur.execute(srch4, val4)


def setup(bot):
    bot.add_cog(CogListeners(bot))