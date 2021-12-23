import json
import os
import nextcord

from nextcord.ext import commands
from createDB import create_db

with open('./discord_extension/master.json','r',encoding='utf-8-sig') as f:
    data = json.load(f)

token = data["bot_info"]["token"]
cp = data["bot_info"]["cp"]

intents = nextcord.Intents.all()

bot = commands.Bot(command_prefix=cp,intents=intents)

@bot.event
async def on_ready():
    print('online')

for filename in os.listdir('./discord_extension/cogs'):
    if filename.endswith('py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(filename, 'loaded')

@bot.command()
@commands.has_any_role('Team Owners', 'Owners', 'Head Dev', 'Head Developer','Head Admin','Head Administrator')
async def update(ctx):
    async def start():
        os.system("python ./discord_extension/bot.py")
        await confirm()
    await ctx.send("Bot will reset now")
    await start()

async def confirm(ctx):
    await ctx.send("Restart Complete")


if __name__ == '__main__':
    create_db()
    bot.run(token)