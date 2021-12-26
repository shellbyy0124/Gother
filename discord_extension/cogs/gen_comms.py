import asyncio
import sqlite3 as sql 
import nextcord 

from nextcord.ext import commands 
from nextcord.ext.commands.errors import MissingRequiredArgument as MRA 
from nextcord.ext.commands.errors import MissingPermissions as MP 
from nextcord.ext.commands.errors import MemberNotFound as MNF 

class GeneralCommands(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        
        
    @commands.command()
    async def ping(self,ctx):
        
        
    
    # @commands.command()
    # async def whois(self,ctx,member:nextcord.Member=None):
    #     with sql.connect('./discord_extension/main.db') as mdb:
    #         cur=mdb.cursor()
            
    #         srch = 'SELECT dob FROM profiles WHERE guild_id=? AND mem_id=?'
    #         val = (ctx.guild.id,member.id,)
            
    #         dob = cur.execute(srch, val).fetchone()
            
    #         srch2 = 'SELECT interests FROM profiles WHERE guild_id=? AND mem_id=?'
            
    #         interests = cur.execute(srch2, val).fetchone()
            
    #         srch3 = 'SELECT hobbies FROM profiles WHERE guild_id=? AND mem_id=?'
            
    #         hobbies = cur.execute(srch3, val).fetchone()
            
    #         srch4 = 'SELECT desc FROM profiles WHERE guild_id=? AND mem_id=?'
            
    #         selfDesc = cur.execute(srch4, val).fetchone()
            
    #         srch5 = 'SELECT color FROM profiles WHERE guild_id=? AND mem_id=?'
            
    #         fav_color = cur.execute(srch5, val).fetchone()
            
    #     messageCount = 0
        
    #     for channel in ctx.guild.text_channels:
    #         async for message in channel.history(limit=None):
    #             if message.author.id == member.id:
    #                 messageCount += 1
                    
    #     embed=nextcord.Embed(
    #         color=nextcord.Colour.random(),
    #         timestamp=ctx.message.created_at,
    #         title=f'~~Who Is. . .:star:{member.name}:star:',
    #         description=f'''Member ID: {member.id}
    #                         Member Name: {member.name}
    #                         Member Nick: {member.display_name}
    #                         Member Favorite Color: {fav_color}
    #                         Member Created On: {member.created_at}
    #                         Member Joined On: {member.joined_at}
    #                         Number Of Messages Sent: {messageCount}'''
    #     ).add_field(
    #         name='Interests:',
    #         value=f'{interests}',
    #         inline=False
    #     ).add_field(
    #         name='Hobbies:',
    #         value=f'{hobbies}',
    #         inline=False
    #     ).add_field(
    #         name='Self Description:',
    #         value=f'{selfDesc}',
    #         inline=False
    #     ).set_thumbnail(
    #         url=member.avatar_url
    #     )
        
    # @whois.error 
    # async def whois_error(self,ctx,error):
    #     if isinstance(error,MRA):
    #         msg = await ctx.send(':rotating_light:You Are Missing The Required Arguements For This Command. `!whois <name/id>`:rotating_light:')
    #         await asyncio.sleep(10)
    #         await msg.delete()
    #     elif isinstance(error,MP):
    #         msg = await ctx.send(':rotating_light:You Are Missing The Required Permissions For This Command:rotating_light:')
    #         await asyncio.sleep(10)
    #         await msg.delete()
    #     elif isinstance(error,MNF):
    #         msg = await ctx.send(':rotating_light:That Member Does Not Exist. Check Spelling/ID:rotating_light:')
    
    
    @commands.command() 
    async def data(self,ctx):
        embed=nextcord.Embed(
            color=nextcord.Colour.random(),
            timestamp=ctx.message.created_at,
            title='Dont Ask To Ask',
            description='[click me ;)](https://dontasktoask.com/)'
        ).set_thumbnail(
            url=ctx.guild.icon_url
        ).set_footer(
            text="Don't ask can you ask a question. Just ask it! :D"
        )
        
        msg = await ctx.send(embed=embed)
        
        await asyncio.sleep(45)
        await msg.delete()
        
        
def setup(bot):
    bot.add_cog(GeneralCommands(bot))