import asyncio
import sqlite3 as sql
import nextcord

from datetime import date
from nextcord.ext import commands
from nextcord.ext.commands.errors import MissingPermissions as MP
from nextcord.ext.commands.errors import MemberNotFound as MNF 
from nextcord.ext.commands.errors import MissingRequiredArgument as MRA

class BankCommands(commands.Cog):
    def __init__(self,bot):
        self.bot=bot


    @commands.command()
    async def pay(self,ctx,receiver:nextcord.Member,amount:float):
        await ctx.message.delete()

        with sql.connect('./discord_extension/main.db') as mdb:
            cur = mdb.cursor()

            """
            UPDATING USERS BALANCE
            """

            srch = 'SELECT balance FROM members WHERE guild_id=? AND mem_id=?'
            val = (ctx.guild.id,ctx.message.author.id,)

            srch2 = 'SELECT balance FROM members WHERE guild_id=? AND mem_id=?'
            val2 = (ctx.guild.id,receiver.id,)

            current_sender_balance = cur.execute(srch, val).fetchone()
            current_receiver_balance = cur.execute(srch2, val2).fetchone()

            if current_sender_balance < amount:
                error=nextcord.Embed(
                    color=next.Colour.red(),
                    timestamp=ctx.message.created_at,
                    title=f'{ctx.guild.name}s\' Bank Notifications',
                    description=f'''Member Name: {ctx.message.author.name}
                                    Current Balance: ${current_sender_balance}
                                    Amount To Send: ${amount}
                                    '''
                ).add_field(
                    name='Error Message',
                    value=':red_circle:Insufficient Funds!:red_circle:',
                    inline=False
                ).set_thumbnail(
                    url=ctx.guild.icon_url
                )

                await ctx.message.author.send(embed=error)
            else:
                new_sender_balance = current_sender_balance[0] - amount
                new_receiver_balance = current_receiver_balance[0] + amount

                srch3 = 'UPDATE members SET balance=? WHERE guild_id=? AND mem_id=?'
                val3 = (ctx.guild.id,ctx.message.author.id,new_sender_balance)
                val4 = (ctx.guild.id,ctx.message.author.id,new_receiver_balance)

                cur.execute(srch3, val3)
                cur.execute(srch3, val4)

                srch5 = 'SELECT bank_notification_status FROM members WHERE guild_id=? AND mem_id=?'
                val5 = (ctx.guild.id,ctx.message.author.id,)
                val6 = (ctx.guild.id,receiver.id,)

                current_sender_status = cur.execute(srch5, val5).fetchone()
                current_receiver_status = cur.execute(srch5, val6).fetchone()

                embed=nextcord.Embed(
                    color=nextcord.Colour.random(),
                    timestamp=ctx.message.created_at,
                    title=f'{ctx.guild.name}s\' Bank Notifications',
                    description=f'''Sender Name: {ctx.message.author.name}
                                    Receiver Name: {receiver.name}
                                    Amount Being Sent: ${amount}
                                    '''
                ).set_thumbnail(
                    url=ctx.guild.icon_url
                )

                if current_sender_status == "yes":
                    embed.add_field(
                        name='Balance Updates',
                        value=f'''Previous Balance: ${current_sender_balance}
                                New Balance: ${new_sender_balance}''',
                        inline=False
                    )
                    await ctx.message.author.send(embed=embed)
                
                if current_receiver_status == "yes":
                    embed.add_field(
                        name='Balance Updates',
                        value=f'''Previous Balance: ${current_receiver_balance}
                                New Balance: ${new_receiver_balance}''',
                        inline=False
                    )
                    await receiver.send(embed=embed)

            """
            UPDATING TRANSACTIONS TABLE
            """

            srch7 = 'INSERT INTO transactions(guild_id,sender,receiver,amount,reason,date) VALUES (?,?,?,?,?,?)'
            val7 = (ctx.guild.id,ctx.message.author.id,receiver.id,amount,date.today().__format__('%m/%d/%y -- %H:%M:%S'))


    @commands.command()
    async def balance(self,ctx):
        with sql.connect('./discord_extension/main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT balance FROM members WHERE guild_id=? AND mem_id=?'
            val = (ctx.guild.id,ctx.message.author.id,)

            current_member_balance = cur.execute(srch, val).fetchone()

            embed=nextcord.Embed(
                color=nextcord.Colour.random(),
                timestamp=ctx.message.created_at,
                title=f'{ctx.guild.name}s\' Bank Notifications',
                description=f'''Member Name: {ctx.message.author.name}
                                Balance: ${current_member_balance}'''
            ).set_thumbnail(
                url=ctx.guild.icon_url
            )

            msg = await ctx.message.author.send(embed=embed)

            await asyncio.sleep(10)
            await msg.delete()


    @pay.error
    async def pay_error(self,ctx,error):
        if isinstance(error,MRA):
            msg = await ctx.send(f'Command Example:```!pay JohnDoe#1234 17.00```Remeber: You Must Type The Amount As A Decimal! Example: 17.00 or 13.53')
            await asyncio.sleep(10)
            await msg.delete()
        elif isinstance(error,MP):
            msg = await ctx.send(f'You Are Missing The Required Permissions To Execute This Command!')
            await asyncio.sleep(10)
            await msg.delete()
        elif isinstance(error,MNF):
            msg = await ctx.send('That Member Is Not A Memeber Of This Discord!')
            await asyncio.sleep(10)
            await msg.delete()

    
def setup(bot):
    bot.add_cog(BankCommands(bot))