from discord.ext.commands import Bot, CommandNotFound
from asyncio import sleep

from datetime import datetime, timedelta
from json import load

from utils.timetable_manager import check_class

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

@bot.command(name = 'help')
async def help(ctx):
	await ctx.channel.send('--test: Check status.\n--getUpdates: start timetable watchdog\nand other testing commands')

@bot.command(name = 'test')
async def test(ctx):
	await ctx.channel.send('Hello world')

@bot.command(name = 'testArgs')
async def test_args(ctx, *args):
	
	if (len(args)) != 2:
		await ctx.channel.send('Invalid format')

	else:
		await ctx.channel.send(args)

@bot.command(name = 'mention')
async def mention(ctx):
	await ctx.channel.send('@everyone')

@bot.command(name = 'timetable-watchdog')
async def get_updates(ctx, *args):

	if (len(args)) != 2:
		await ctx.channel.send('Invalid format')

	elif args[0] not in ['batch-1', 'batch-2']:
		await ctx.channel.send('Invalid batch format. Try again.')

	elif args[1] not in ['1', '2']:
		await ctx.channel.send('Invalid week format. Try again.')

	elif ctx.guild in sub_guild:
		await ctx.channel.send('Already subscribed')

	else:
		sub_guild.append(ctx.guild)

		while(True):

			update = check_class(datetime.now())

			await ctx.channel.send("Message: {}\nSleeping for: {} mins".format(update['content'], update['sleep_time']))
			await sleep(update['sleep_time'] * 60)

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, CommandNotFound):
		await ctx.channel.send("Sorry {} ! Unknown command\nTry `--help` to see what I can do.".format(ctx.message.author.mention))

bot.run(getTokens()['discord-bot'])