from discord.ext.commands import Bot
from asyncio import sleep

from datetime import datetime, timedelta
from json import load

from timetable_manager import check_class

bot = Bot(command_prefix='--')
bot.remove_command('help')

def getTokens():

	with open("res/TOKENS.json", 'r') as FPtr:
		tokens = load(FPtr)

	return tokens

sub_guild = []

@bot.event
async def on_ready():  
		print("\nLogged in as: " + str(bot.user))
		print("------------------")

@bot.command(name='test')
async def test(ctx):
	await ctx.channel.send('Hello world')

@bot.command(name = 'mention')
async def mention(ctx):
	await ctx.channel.send('@everyone')

@bot.command(name = 'getUpdates')
async def get_updates(ctx):

	if ctx.guild in sub_guild:
		await ctx.channel.send('Already subscribed')

	else:
		sub_guild.append(ctx.guild)

		while(True):

			update = check_class(datetime.now())

			await ctx.channel.send("Message: {}\nSleeping for: {} mins".format(update['content'], update['sleep_time']))
			await sleep(update['sleep_time'] * 60)

bot.run(getTokens()['discord-bot'])