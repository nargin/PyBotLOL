# Env import
import os, sys
from dotenv import load_dotenv

# Web import
import discord
import requests
import json
import time
from riotwatcher import LolWatcher, ApiError

# parsing.py
from parsing import *

# Command Folder #
from command.alias import command_alias
from command.mastery import mastery_champion
from command.profile import profile_ranked
from command.winrate import winrate_ranked
from command.death import death_counter

# Other
from personal import personal

test = False


# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
RIOT_API_KEY = os.getenv('LOL_TOKEN')
region = os.getenv('LOL_REGION')

# Initialize RiotWatcher
lol_watcher = LolWatcher(RIOT_API_KEY)

# Discord client
intents = discord.Intents.all()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
	if message.channel.name != 'que_pour_robin' and test == True:
		return

	if message.author == client.user or message.author.bot:
		return

	input_message = message.content.lower()

	if input_message.startswith('!') == False:
		return

	split = input_message.split(' ')
	data_command = Command(split, region, lol_watcher, RIOT_API_KEY)

	print(f'command : {data_command.command}, option : {data_command.option}, summoner_name : {data_command.summoner_name}')

	# To test

	# function = {
	# 	'big': lambda: message.channel.send("https://tenor.com/view/big-snoopa-gif-18474914"),
	# 	'profile': profile_ranked(data_command, lol_watcher),
	# 	'mastery': mastery_champion(data_command, lol_watcher),
	# 	'winrate': winrate_ranked(data_command, lol_watcher),
	# 	'help': helper(),
	# 	'morpion': morpion(),
	# }

	# embed = function.get(data_command.command, None)

	# if embed != None:
	# 	await message.channel.send(embed=embed)


	match data_command.command:
		case None :
			pass

		case 'big':
			await message.channel.send("https://tenor.com/view/big-snoopa-gif-18474914")
			return
		
		case 'profile': # Summoner Profile
			await message.channel.send(embed=profile_ranked(data_command, lol_watcher))
			return

		case 'death':
			start_time = time.time()
			await message.channel.send(embed=death_counter(data_command, lol_watcher))
			end_time = time.time()
			print(f'Execution time : {end_time - start_time}')
			return

		case 'mastery': # Mastery
			await message.channel.send(embed=mastery_champion(data_command, lol_watcher))
			return
		
		case 'winrate':
			await message.channel.send(embed=winrate_ranked(data_command, lol_watcher))
			return

		case 'help':
			await message.channel.send(embed=helper())
			return
		
		case 'morpion':
			await message.channel.send(morpion())
			return

		case _:
			pass

	command_personal = personal(input_message)

	if command_personal != None :
		await message.channel.send(command_personal)

	else :
		print(f'#{message.channel.name} {message.author} : {message.content} - Command not found')
	
	

# TO DO :
# Gain lp command
# death of 20 last games

test = 1 if len(sys.argv) > 1 and sys.argv[1] == 'test' else 0
client.run(DISCORD_TOKEN)

