# bot.py
import time
import os
import random
import discord
import datacrawler as ge_connection
from discord.ext import commands
my_secret = os.environ['token']
intents = discord.Intents(messages=True, guilds=True, members=True) 
 # If you also want reaction events enable the following:
intents.reactions = True

 # Somewhere else:
 # client = discord.Client(intents=intents)
 # or
 # from discord.ext import commands
 # bot = commands.Bot(command_prefix='!', intents=intents)
TOKEN = os.environ['token']
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot (command_prefix='.', intents=intents)
 

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to server!'
    )


@bot.command(name='test',help="Testing the discord bot.")
async def test(ctx): 
    await ctx.send("Testing, 1,2,3?")

@bot.command(name='roll', help='Rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))
    
@bot.command(name='createch',help='Creates a channel')
@commands.has_role('god mode')
async def create_channel(ctx, channel_name:str):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

@bot.command(name='price',help='Check price')
async def price(ctx, item_name:str):
    await ctx.send("Searching price of: "+ item_name)
    grab_price=ge_connection.start_finding_price(item_name.replace('_'," "))
    for x in grab_price:
        await ctx.send("Price of "+ x[0] +" is: " + x[1])
        time.sleep(0.1)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


bot.run(TOKEN)
