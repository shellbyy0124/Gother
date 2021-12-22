import nextcord 
import asyncio
import sqlite3 as sql 

from nextcord.ext import commands
from nextcord.ext.commands.errors import MissingRequiredArgument as MRA
from nextcord.ext.commands.errors import MemberNotFound as MNF
from nextcord.ext.commands.errors import MissingPermissions as MP 


class GeneralUserCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.command()
    async def whois(self,ctx,member:nextcord.Member=None):
        await ctx.message.delete()

        if member is None:
            member=ctx.message.author

        with sql.connect('./discord_extension/main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT message_count FROM members WHERE guild_id=? AND mem_id=?'
            val = (ctx.guild.id,member.id,)

            message_count = cur.execute(srch, val).fetchone()

            srch2 = 'SELECT nick FROM profiles WHERE guild_id=? AND mem_id=?'
            srch3 = 'SELECT dob FROM profiles WHERE guild_id=? AND mem_id=?'
            srch4 = 'SELECT interests FROM profiles WHERE guild_id=? AND mem_id=?'
            srch5 = 'SELECT hobbies FROM profiles WHERE guild_id=? AND mem_id=?'
            srch6 = 'SELECT desc FROM profiles WHERE guild_id=? AND mem_id=?'
            srch7 = 'SELECT color FROM profiles WHERE guild_id=? AND mem_id=?'

            nick = cur.execute(srch2, val).fetchone()
            dob = cur.execute(srch3, val).fetchone()
            interests = cur.execute(srch4, val).fetchone()
            hobbies = cur.execute(srch5, val).fetchone()
            desc = cur.execute(srch6, val).fetchone()
            fav_color = cur.execute(srch7, val).fetchone()

        embed=nextcord.Embed(
            color=nextcord.Colour.random(),
            timestamp=ctx.message.created_at,
            title=f'Who Is {member.name}',
            description=f'''Member Name: {member.name}
                            Member ID: {member.id}
                            Member Created On: {member.created_at}
                            Member Joined On: {member.joined_at.__format__("%m/%d/%y -- %H:%M:%S")}
                            Number Of Messages Sent: {message_count}
                            Highest Role: {member.top_role}
                            All Roles: {member.roles}'''
        ).add_field(
            name='More Information',
            value=f'''Nickname: {nick}
                      Date Of Birth: {dob}
                      Favorite Color: {fav_color}''',
            inline=False
        ).add_field(
            name='Interests',
            value=f'{interests}',
            inline=False
        ).add_field(
            name='Hobbies',
            value=f'{hobbies}',
            inline=False
        ).add_field(
            name='How I See Myself:',
            value=f'{desc}',
            inline=False
        ).set_thumbnail(
            url=member.display_avatar
        )

        msg = await ctx.send(embed=embed)
        await asyncio.sleep(10)
        await msg.delete()


    @commands.command()
    async def ping(self,ctx):
        current_latency = self.bot.latency

        if current_latency > 200:
            owner_id = 260009824945831936
            me = await self.bot.get_user(owner_id)
            await me.send(f'I Have A High Latency! {current_latency}')


    @commands.command()
    async def suggest(self,ctx):
        await ctx.message.delete()

        def check(m):
            return ctx.message.author.id == m.author.id


        msg = await ctx.send('What is the name of your suggestion?')
        name = await self.bot.wait_for('message',check=check,timeout=30)

        msg2 = await ctx.send('What part of ButtlerBot does this suggestion take place?')
        sugg_part = await self.bot.wait_for('message',check=check,timeout=30)

        msg3 = await ctx.send('What is your suggestion?')
        suggest = await self.bot.wait_for('messgae',check=check,timeout=30)

        embed=nextcord.Embed(
            color=nextcord.Colour.orange(),
            timestamp=ctx.message.created_at,
            title=f'{self.bot.user.name}s\' Suggestion Editor',
            desrcription=f'Please Review And Confirm Your Suggestion\n\nName Of Suggestion: {name.content}\nPart Of ButtlerBot: {sugg_part.content}'
        ).add_field(
            name='Suggestion',
            value=f'{suggest.content}',
            inline=False
        ).set_thumbnail(
            url=ctx.message.author.avatar_url
        )

        msg4 = await ctx.send(embed=embed)

        msg5 = await ctx.send('Please Enter Send Or Edit')

        answer = await self.bot.wait_for('message',check=check,timeout=30)

        if answer.content.lower() == 'enter':
            owner_id=260009824945831936
            me = self.bot.get_user(owner_id)

            await me.send(embed=embed)

            await msg.delete()
            await msg2.delete()
            await msg3.delete()
            await msg4.delete()
            await msg5.delete()
            await name.delete()
            await sugg_part.delete()
            await suggest.delete()
            await answer.delete()
        else:
            msg6 = await ctx.send('You Selected Edit. Please Run The Command Again.')
            
            await msg.delete()
            await msg2.delete()
            await msg3.delete()
            await msg4.delete()
            await msg5.delete()
            await msg6.delete()
            await name.delete()
            await sugg_part.delete()
            await suggest.delete()
            await answer.delete()


def setup(bot):
    bot.add_cog(GeneralUserCommands(bot))