import discord
import requests
import json

def helper():

	help_message = {
		'Profile': '!pr <summoner_name>-<tag_id>\nDefault id : EUW\n',
		'Mastery': '!m [n] <summoner_name>-<tag_id>\nNumber of champions to display (default: 3)\nDefault id : EUW\n',
		'Winrate': '!wr [s/f] <summoner_name>-<tag_id>\Soloq or flex (default: soloq)\nDefault id : EUW\n',
		'Help': '!help\n',
		'Misc': '!big\n'
	}

	embed = discord.Embed(title='Help', description='**List of commands :**', color=0x00ff00, type='rich')

	for i in range(0, len(help_message)):
		embed.add_field(name=f'**__{list(help_message.keys())[i]}__** :', value=list(help_message.values())[i], inline=False)
		embed.add_field(name='', value='', inline=False) # Add blank field = nl
	embed.set_footer(text='Made by nargin')
	
	return embed

def	command_list(command):
	command_list = {
		'!big': 'big',
		'!pr': 'profile',
		# '!pid': 'puuid',
		'!death': 'death',
		'!m': 'mastery',
		'!wr': 'winrate',
		'!help': 'help',
		'!track': 'track',
		'!alias': 'alias',
		'!morpion': 'morpion'
	}
	return command_list.get(command, None)



class Command:
	command = ''
	option = 0
	summoner_name = ''
	alias_name = ''
	actual_name = ''
	regions = ''
	puuid = ''
	lol_token = ''
	lol_watcher = None

	def __init__(self, split, regions, lol_watcher, lol_token):
		self.regions = regions
		self.lol_watcher = lol_watcher
		self.lol_token = lol_token
		self.parser(split, lol_token)


	def alias_parser(self, split):
		if len(split) == 0:
			self.option = 'l'
			return

		if split[0] == 'a' or split[0] == 'add':
			self.option = 'a'
			split.pop(0) # Remove option
		
		elif split[0] == 'd' or split[0] == 'del':
			self.option = 'd'
			split.pop(0)
		
		elif split[0] == 'e' or split[0] == 'edit':
			self.option = 'e'
			split.pop(0)
		
		if len(split) < 2 and self.option != 'd': # Test if there is at least 2 arguments (alias and summoner_name)
			return

		self.alias_name = split[0]
		split.pop(0) # Remove alias

		for value in split:
			self.summoner_name += value + ' '
		self.summoner_name = self.summoner_name[:-1]



	def default_parser(self, split):
		if split[0].isdigit() and self.command == 'mastery':
			self.option = int(split[0])
			split.pop(0) # Remove option

		elif (split[0] == 's' or split[0] == 'f') and self.command == 'winrate':
			self.option = split[0]
			split.pop(0)

		riot_id = ''
		for value in split:
			riot_id += value + ' '
		riot_id = riot_id[:-1]

		return self.GetSummonerName(riot_id, self.lol_token)
		


	def	GetSummonerName(self, riot_id, lol_token):
		tagLine = 'EUW'
		self.actual_name = riot_id
		if riot_id.find('-') != -1:
			tagLine = riot_id.split('-')[1]
			self.actual_name = riot_id.split('-')[0]
		try:
			url = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{self.actual_name}/{tagLine}?api_key={lol_token}'
		except Exception as e:
			print(e)
			return None

		response = requests.get(url)
		if response.status_code != 200:
			print(f'riot_id response : {response.status_code}')
			return None

		json_response = response.json()
		puuid = json_response['puuid']
		self.puuid = puuid

		try:
			url = f'https://{self.regions}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={lol_token}'
		except Exception as e:
			print(e)
			return None

		response = requests.get(url)
		if response.status_code != 200:
			print(f'puuid response : {response.status_code}')
			return None

		json_response = response.json()
		ret_summoner_name = json_response['name']

		return ret_summoner_name

	def parser(self, split, lol_token):
		self.command = command_list(split[0])
		split.pop(0) # Remove command

		if self.command == None:
			return None

		if self.command == 'alias':
			return self.alias_parser(split)

		elif len(split) != 0:
			self.summoner_name = self.default_parser(split)

