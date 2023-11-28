import os
import discord
from riotwatcher import LolWatcher, ApiError
from dotenv import load_dotenv
from league_related import mastery_champion, profile_user
from personal import personal

test = False

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
RIOT_API_KEY = os.getenv('LOL_TOKEN')

lol_watcher = LolWatcher(RIOT_API_KEY)


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
	input_message = input_message.split(' ', 1)

	print(f'#{message.channel.name} {message.author} : {message.content}')

	if input_message[0] == '!big':
		await message.channel.send("https://tenor.com/view/big-snoopa-gif-18474914")
	
	if input_message[0] == '!s':
		await message.channel.send(embed=profile_user(input_message[1], lol_watcher))

	if input_message[0] == '!m':
		await message.channel.send(embed=mastery_champion(input_message[1], lol_watcher))

	
	# command_personal = personal(input_message)

	# if command_personal != None and type(command_personal) == str:
	# 	await message.channel.send(command_personal)
	# elif command_personal != None and type(command_personal) == list:
	# 	await message.channel.send(command_personal[0])
	# 	await message.channel.send(command_personal[1])
	
	if input_message[0] == '!help':
		await message.channel.send("**Commands : \n\t!big\n\t!s <summoner_name>\n\t!jupuceau\n\t!dodo\n\t!roisouffrant**")
	

test = False
client.run(DISCORD_TOKEN)

