import asyncio
import sqlite3 as sql 
import nextcord

from datetime import date 
from nextcord.ext import commands
from nextcord.ext.commands.errors import MissingRequiredArgument as MRA
from nextcord.ext.commands.errors import MissingPermissions as MP
from nextcord.ext.commands.errors import MemberNotFound as MNF

class AdminBankCommands(commands.Cog):
    def __init__(self,bot):
        self.bot=bot


    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def fixbal(self,ctx,command:str,receiver:nextcord.Member,amount:float,):
        await ctx.message.delete()

        if command == "add":
            with sql.connect('./discord_extension/main.db') as mdb:
                cur = mdb.cursor()

                srch = 'SELECT balance FROM members WHERE guild_id=? AND mem_id=?'
                val = (ctx.guild.id, receiver.id,)

                curr_receiver_bal = cur.execute(srch, val).fetchone()

                new_balance = curr_receiver_bal[0] + amount

                srch2 = 'UPDATE members SET balance=? WHERE guild_id=? AND mem_id=?'
                val2 = (ctx.guild.id, receiver.id, new_balance)

                cur.execute(srch2, val2)

            confirmation=nextcord.Embed(
                color=nextcord.Colour.green(),
                timestamp=ctx.message.created_at,
                title=f'{ctx.guild.name}s\' Bank Notifications',
                description=f'''Administrator: {ctx.message.author.name}
                                Receiver: {receiver.name}
                                Receiver Current Balance: ${curr_receiver_bal}
                                Receiver Updated Balance: ${new_balance}
                                Difference: ${amount}'''
            ).set_thumbnail(
                url=ctx.guild.icon_url
            )

            await receiver.send(embed=confirmation)

            srch3 = 'INSERT INTO transactions(guild_id,sender,receiver,amount,date) VALUES (?,?,?,?,?)'
            val3 = (ctx.guild.id,ctx.message.author.id,receiver.id,amount,str(date.today().__format__('%m/%d/%y -- %H:%M:%S')))

            cur.execute(srch3, val3)
        else:
            with sql.connet('main.db') as mdb:
                cur = mdb.cursor()

                srch = 'SELECT balance FROM members WHERE guild_id=? AND mem_id=?'
                val = (ctx.guild.id,receiver.id,)

                curr_receiver_bal = cur.execute(srch, val).fetchone()

                new_balance = curr_receiver_bal[0] - amount

                srch2 = 'UPDATE members SET balance=? WHERE guild_id=? AND mem_id=?'
                val2 = (ctx.guild.id,receiver.id,new_balance)

                cur.execute(srch2, val2)

            confirmation=nextcord.Embed(
                color=nextcord.Colour.green(),
                timestamp=ctx.message.created_at,
                title=f'{ctx.guild.name}s\' Bank Notifications',
                description=f'''Administrator: {ctx.message.author.name}
                                Receiver: {receiver.name}
                                Receiver Current Balance: ${curr_receiver_bal}
                                Receiver Updated Balance: ${new_balance}
                                Difference: ${amount}'''
            ).set_thumbnail(
                url=ctx.guild.icon_url
            )

            await receiver.send(embed=confirmation)

            srch3 = 'INSERT INTO transactions(guild_id,sender,receiver,amount,date) VALUES (?,?,?,?,?)'
            val3 = (ctx.guild.id,ctx.message.author.id,receiver.id,amount,str(date.today().__format__('%m/%d/%y -- %H:%M:%S')))

            cur.execute(srch3, val3)

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def clearbal(self,ctx,member:nextcord.Member,*,reason:str):
        await ctx.message.delete()

        with sql.connect('./discord_extension/main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT balance FROM members WHERE guild_id=?,mem_id=?'
            val = (ctx.guild.id,member.id)

            curr_mem_bal = cur.execute(srch,val).fetchone()

            new_bal = 0

            embed=nextcord.Embed(
                color=nextcord.Colour.random(),
                timestamp=ctx.message.created_at,
                title=f'{ctx.guild.name}s\' Bank System',
                description=f'''Member Name: {member.name}
                                Current Balance: ${curr_mem_bal}
                                Amount To Adjust: -${curr_mem_bal}
                                Adjusted Balance: {new_bal}
                                ''',
                inline=False
            ).add_field(
                name='Reason',
                value=f'{reason}',
            inline=False
            ).set_thumbnail(
                url=ctx.guild.icon_url
            )

            await member.send(embed=embed)

            msg = await ctx.send(embed=embed)
            await asyncio.sleep(10)
            await msg.delete()

            srch2 = 'INSERT INTO transactions(guild_id,sender,receiver,amount,date) VALUES (?,?,?,?,?)'
            val2 = (ctx.guild.id,ctx.message.author.id,member.id,new_bal,str(date.today().__format__('%m/%d/%y -- %H:%M:%S')))

            cur.execute(srch2, val2)


    @clearbal.error
    async def clearbal_error(self,ctx,error):
        if isinstance(error,MP):
            msg = await ctx.send('You Do Not Have The Required Permissions To Execute This Command')
            await asyncio.sleep(5)
            await msg.delete()
        elif isinstance(error,MRA):
            msg = await ctx.send('Example: `!clearbal ButtlerBot <reason>')
            await asyncio.sleep(5)
            await msg.delete()
        else:
            embed=nextcord.Embed(
                color=nextcord.Colour.red(),
                timestamp=ctx.message.created_at,
                title='ButtlerBot Error System',
                description='Hmmmm....I\'m not sure what happened there. Please report to the [support discord](https://discord.gg/weREZMjr3s).',
                inline=False
            ).set_thumbnail(
                url = self.bot.user.avatar_url
            ).set_footer(
                text = 'This is an automated message. Please report to the support discord for further assistance. Message will delete in 30 seconds'
            )

            msg = await ctx.send(
                embed=embed
            )

            await asyncio.sleep(10)
            await msg.delete()


    @fixbal.error
    async def fixbal_error(self,ctx,error):
        if isinstance(error, MNF):
            msg = await ctx.send('That Member Does Not Exist!')
            await asyncio.sleep(10)
            await msg.delete()
        elif isinstance(error, MRA):
            msg = await ctx.send(f'Command Example: `!fixbal Shellbyy#8025 500.00` or `!fixbal Shellbyy#8025 -500.00`')
            await asyncio.sleep(10)
            await msg.delete()
        elif isinstance(error, MP):
            msg = await ctx.send('You Do Not Have The Required Permissions To Execute This Command!')
            await asyncio.sleep(10)
            await msg.delete()


def setup(bot):
    bot.add_cog(AdminBankCommands(bot))