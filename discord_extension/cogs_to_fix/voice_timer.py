import asyncio

from nextcord.ext import commands 
from datetime import timedelta as td

class VoiceTimer(commands.Cog):
    def __init__(self,bot):
        self.bot=bot


    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        current_nick = member.nick

        if before.channel is None and after.channel is None:
            await self.timer()
        elif before.channel is None and after.channel is not None:
            await self.timer()
        elif before.channel is not None and after.channel is None:
            await self.timer()
        elif before.channel is not None and after.channel is not None:
            await self.timer()
        else:
            print('SUM TING WONG')


    async def timer(self,member,current_nick):
        time = td(seconds=0)

        await member.edit(nick=f'{member.display_name[:20]}: {time}')

        while member.voice_state == True:
            await asyncio.sleep(self.total_seconds_needed)
            
            time += td(self.total_seconds_needed)

            await member.edit(nick=f'{member.display_name[:20]}: {time}')
        else:
            await member.edit(nick=current_nick)


    async def check_seconds_needed(self):
        members_in_voice = 0
        total_guilds = 0
        members_per_second = 4

        for guild in self.bot.guilds:
            total_guilds += 1

            for member in guild.members:
                if member.voice_state == True:
                    members_in_voice += 1
                else:
                    pass

        total_seconds_needed = round((total_guilds*members_in_voice)/members_per_second)

        return total_seconds_needed


def setup(bot):
    bot.add_cog(VoiceTimer(bot))