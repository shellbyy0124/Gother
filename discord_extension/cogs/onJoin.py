import datetime
import sqlite3 as sql
import nextcord
import json

from nextcord.ext import commands

class OnJoinFunctions(commands.Cog):
    def __init__(self,bot):
        self.bot=bot


    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        await self.update_botInfo_table(guild)
        
        
    async def update_botInfo_table(self,guild):
        with sql.connect('./discord_extension/main.db') as mdb:
            cur = mdb.cursor()
            
            guild_count = cur.execute('SELECT guild_count FROM botInfo').fetchone()
            
            new_count = guild_count[0] + 1
            
            srch = 'UPDATE botInfo SET guild_count=?'
            val = (new_count,)
            
            cur.execute(srch, val)
            
        await self.update_guilds_table(guild)
        
    
    async def update_guilds_table(self,guild):
        with sql.connect('./discord_extension/main.db') as mdb:
            cur = mdb.cursor()
            
            srch2 = 'SELECT status FROM guilds WHERE guild_id=?'
            val2 = (guild.id,)
                
            current_status = cur.execute(srch2, val2).fetchone()
                
            if current_status is None:
                memberCount = 0
                    
                for member in guild.members:
                    if not member.bot:
                        memberCount += 1
                            
                srch3 = 'INSERT INTO guilds(guild_id,status,member_count) VALUES (?,?,?)'
                val3 = (guild.id,"active",memberCount)
                    
                cur.execute(srch3, val3)
            elif current_status == "inactive":
                memberCount = 0
                    
                for member in guild.members:
                    if not member.bot:
                        memberCount += 1
                        
                srch4 = 'UPDATE guilds SET status=? AND member_count=? WHERE guild_id=?'
                val4 = (guild.id,"active",memberCount)
                
                cur.execute(srch4, val4)
                
        await self.update_members_table(guild)
                    
                    
    async def update_members_table(self,guild):
        with sql.connect('./discord_extension/main.db') as mdb:
            cur = mdb.cursor()
            
            all_members = []
            
            for member in guild.members:
                if not member.bot:
                    all_members.append(member.id)
                    
            for memberId in all_members:
                try:
                    srch5 = 'INSERT INTO members(guild_id,mem_id,warnings,mutes,balance,status,sub_status,message_count) VALUES (?,?,?,?,?,?,?,?)'
                    val5 = (guild.id,memberId,0,0,0,"active","inactive",0)
                    
                    cur.execute(srch5, val5)
                except:
                    srch6 = 'UPDAET members SET warnings=? AND mutes=? AND balance=? AND status=? AND sub_status=? AND message_count=? WHERE guild_id=? AND mem_id=?'
                    val6 = (guild.id,memberId,0,0,0,"active","inactive",0)
                    
                    cur.execute(srch6, val6)
                        
        await self.update_bank_table(guild)
        
    
    async def update_bank_table(self,guild):
        with sql.connect('./discord_extension/main.db') as mdb:
            cur = mdb.cursor()
            
            srch8 = 'SELECT guild_bal FROM bank WHERE guild_id=?'
            val8 = (guild.id,)
            
            curr_bal = cur.execute(srch8, val8).fetchone()
            
            if curr_bal is None:
                srch9 = 'INSERT INTO bank(guild_id,jackpot,guild_bal) VALUES (?,?,?)'
                val9 = (guild.id,0,1000000000)
                
                cur.execute(srch9, val9)
            else:
                srch10 = 'UPDATE bank SET jackpot=? AND guild_bal=? WHERE guild_id=?'
                val10 = (guild.id,0,1000000000)
                
                cur.execute(srch10, val10)
                
                
        await self.check_channel(guild)
        
    
    async def check_channel(self,guild):
        reason = "Needed For Logs -Mekasu"
        
        cat_check = nextcord.utils.get(guild.categories,name="Logs")
        chan1 = nextcord.utils.get(guild.text_channels, name='nickname_logs')
        chan2 = nextcord.utils.get(guild.text_channels, name='warning_logs')
        chan3 = nextcord.utils.get(guild.text_channels, name='mute_logs')
                
        if cat_check is None:
            cat = await guild.create_category(name="Logs",reason=reason)
            catPerms = cat.overwrites_for([m for m in guild.members if not m.bot])
            catPerms.send_messages=False
            catPerms.read_messages=False
            catPerms.read_message_history=False
            
        if chan1 is None:
            new_chan = await guild.create_text_channel(name="nickname_logs",category=cat_check,reason=reason)
            chanPerms = new_chan.overwrites_for([m for m in guild.members if not m.bot])
            chanPerms.send_messages=False
            chanPerms.read_messages=False
            chanPerms.read_message_history=False
            
        if chan2 is None:
            new_chan = await guild.create_text_channel(name="warning_logs",category=cat_check,reason=reason)
            chanPerms = new_chan.overwrites_for([m for m in guild.members if not m.bot])
            chanPerms.send_messages=False
            chanPerms.read_messages=False 
            chanPerms.read_message_history=False
            
        if chan3 is None:
            new_chan = await guild.create_text_channel(name="mute_logs",category=cat_check,reason=reason)
            chanPerms = new_chan.overwrites_for([m for m in guild.members if not m.bot])
            chanPerms.send_messages=False 
            chanPerms.read_messages=False 
            chanPerms.read_message_history=False
            
    
    @commands.Cog.listener()
    async def on_member_join(self,ctx,member):
        with sql.connect('./discord_extension/main.db') as mdb:
            cur = mdb.cursor()
            
            srch = 'SELECT status FROM members WHERE guild_id=? AND mem_id=?'
            val = (member.guild.id,member.id,)
            
            current_status = cur.execute(srch, val).fetchone()
            
            if current_status is None:
                srch2 = 'INSERT INTO members(guild_id,mem_id,warnings,mutes,balance,status,sub_status,message_count) VALUES (?,?,?,?,?,?,?,?)'
                val2 = (member.guild.id,member.id,0,0,0,"active","inactive",0)
                
                cur.execute(srch2, val2)
            elif current_status == "inactive":
                srch3 = 'UPDATE members SET status=? WHERE guild_id=? AND mem_id=?'
                val3 = (member.guild.id,member.id,"active")
                
                cur.execute(srch3, val3)

def setup(bot):
    bot.add_cog(OnJoinFunctions(bot))