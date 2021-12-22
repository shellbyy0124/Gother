import nextcord
import asyncio 
import sqlite3 as sql 

from nextcord.ext import commands
from nextcord.ext.commands.errors import MissingRequiredArgument as MRA 
from nextcord.ext.commands.errors import MissingPermissions as MP 
from nextcord.ext.commands.errors import MemberNotFound as MNF 

class CreateUserProfile(commands.Cog):
    def __init__(self,bot):
        self.bot=bot 


    @commands.command()
    async def create_profile(self,ctx):
        await ctx.message.delete()

        def check(m):
            return ctx.message.author.id == m.author.id

        member = ctx.message.author

        await member.send('Would you like to use a nickname or respond with None :)')

        member_nick = await self.bot.wait_for('message',check=check,timeout=30)

        await member.send('Would you like to enter your birthday or respond with None :)')

        member_dob = await self.bot.wait_for('message',check=check,timeout=30)

        await member.send('Would you like to share your interests or respond with None :)')

        interests = await self.bot.wait_for('message',check=check,timeout=30)

        await member.send('Would you like to show your hobbies or respond with None :)')

        hobbies = await self.bot.wait_for('message',check=check,timeout=30)

        await member.send('Would you like to describe yourself in 2-3 sentence or respond with None :)')

        descrip = await self.bot.wait_for('message',check=check,timeout=30)

        await member.send('Would you like to share your favorite color or respond with None :)')

        color = await self.bot.wait_for('message',check=check,timeout=30)

        await member.edit(nick=member_nick)

        for col in nextcord.Colour():
            if color in col:
                color=nextcord.Colour.color()
            else:
                color=nextcord.Colour.random()

        final_embed=nextcord.Embed(
            color=color,
            timestamp=ctx.message.created_at,
            title=f'{ctx.gulid.name}s\' Profile Creator',
            description=f'''Name: {member.name}
                            Nickname: {member_nick}
                            Date Of Birth: {member_dob}
                            Interests: {interests}
                            Hobbies: {hobbies}
                            Favorite Color: {color}'''
        ).add_field(
            name='How I See Myself:',
            value=f'{descrip}',
            inline=False
        ).add_field(
            name='Confirmation',
            value='''Please Read The Information Above. Respond With `yes` if correct.
                     If your information is wrong, please repond with no and execute
                     the command again. Thanks :)'''
        ).set_thumbnail(
            url=member.display_avatar
        )

        await member.send(embed=final_embed)

        confirmation_answer = await self.bot.wait_for('message',check=check,timeout=30)

        if confirmation_answer.content.lower() == "yes":
            with sql.connect('./discord_extension/main.db') as mdb:
                cur = mdb.cursor()

                srch = 'SELECT mem_id FROM profiles WHERE guild_id=?'
                val = (ctx.guild.id,)

                all_member_ids = cur.execute(srch, val).fetchall()

                if member.id in all_member_ids:
                    srch2 = 'UPDATE profiles SET nick=? AND dob=? AND interests=? AND hobbies=? AND desc=? AND color=? WHERE guild_id=? AND mem_id=?'
                    val2 = (ctx.guild.id,member.id,member_nick.content,member_dob.content,interests.content,hobbies.content,descrip.content,color.content)

                    cur.execute(srch2, val2)
                else:
                    srch3 = 'INSERT INTO profiles(guild_id,mem_id,nick,dob,interests,hobbies,desc,color) VALUES (?,?,?,?,?,?,?,?)'
                    val3 = (ctx.guild.id,member.id,member_nick.content,member_dob.content,interests.content,hobbies.content,descrip.content,color.content)

                    cur.execute(srch3, val3)
        else:
            await member.send('You Have Entered No. Terminating Command.')


    @create_profile.error
    async def create_profile_error(self,ctx,error):
        if isinstance(error,TimeoutError):
            msg = await ctx.send('You Did Not Answer Within 30 Seconds. Terminating Command.')
            await asyncio.sleep(10)
            await msg.delete()

def setup(bot):
    bot.add_cog(CreateUserProfile(bot))