import discord,os,asyncio, discord,json,random,time
from discord.ext import commands
#---------------------------------------------------------#
with open('jsonfile/config.json', 'r') as f:
    Config = json.load(f)
prefix = Config['prefix']
token = Config['token']
bot_client_id = Config['bot_client_id']
#---------------------------------------------------------#
activity = discord.Activity(name='Nguyên Play Music️ 🎼', type=discord.ActivityType.watching)
client = commands.Bot(command_prefix=prefix, status=discord.Status.idle,activity=activity,intents=discord.Intents.all(),application_id=bot_client_id ,help_command=None)
#---------------------------------------------------------#
async def Four():
    async with client:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
            # cut off the .py from the file name
                await client.load_extension(f"cogs.{filename[:-3]}")
                print(f'load {filename[:-3]} susess')
            else:
                print(f'Unable to load {filename[:-3]}')
        await client.start(token)
asyncio.run(Four())
#---------------------------------------------------------#
