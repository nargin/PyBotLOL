import os, sys
import discord
from riotwatcher import LolWatcher, ApiError
from dotenv import load_dotenv
from league_related import mastery_champion, profile_ranked, winrate_soloq
from personal import personal
from helper import helper, Command, command_list, morpion

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
	data_command = Command(split, region, lol_watcher)

	# print(f'command : {data_command.command}, option : {data_command.option}, summoner_name : {data_command.nickname}')

	match data_command.command:
		case None :
			pass

		case 'big':
			await message.channel.send("https://tenor.com/view/big-snoopa-gif-18474914")
			return
		
		case 'profile': # Summoner Profile
			await message.channel.send(embed=profile_ranked(data_command, lol_watcher))
			return

		case 'mastery': # Mastery
			await message.channel.send(embed=mastery_champion(data_command, lol_watcher))
			return
		
		case 'winrate':
			await message.channel.send(embed=winrate_soloq(data_command, lol_watcher))
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
# rank and lp soloq command

test = 1 if len(sys.argv) > 1 and sys.argv[1] == 'test' else 0
client.run(DISCORD_TOKEN)

