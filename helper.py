import discord

def	morpion():
	return '```  1 2 3\n1| | | \n2| | | \n3| | | \n```'

def helper():

	help_message = {
		'Profile': '!pr <summoner_name>\n',
		'Mastery': '!m [n] <summoner_name>\nNumber of champions to display (default: 3)\n',
		'Winrate': '!wr [s/f] <summoner_name>\nSoloq or flex (default: soloq)\n',
		'Help': '!help\n',
		'Misc': '!big\n'
	}

	embed = discord.Embed(title='Help', description='**List of commands :**', color=0x00ff00, type='rich')

	for i in range(0, len(help_message)):
		embed.add_field(name=f'**__{list(help_message.keys())[i]}__** :', value=list(help_message.values())[i], inline=False)
		# jump line
		embed.add_field(name='', value='', inline=False)
	embed.set_footer(text='Made by nargin')
	
	return embed

def	command_list(command):
	return {
		'!big': 'big',
		'!pr': 'profile',
		'!m': 'mastery',
		'!wr': 'winrate',
		'!help': 'help',
		'!morpion': 'morpion'
	}.get(command, None)

class Command:
	command = ''
	option = 0
	nickname = ''
	regions = ''
	lol_watcher = None

	def __init__(self, split, regions, lol_watcher):
		self.regions = regions
		self.lol_watcher = lol_watcher
		self.parser(split)

	def parser(self, split):
		
		self.command = command_list(split[0])
		split.pop(0) # Remove command

		if self.command == None or len(split) == 0:
			return None
		
		if split[0].isdigit() and self.command == 'mastery':
			self.option = int(split[0])
			split.pop(0) # Remove option

		elif (split[0] == 's' or split[0] == 'f') and self.command == 'winrate':
			self.option = split[0]
			split.pop(0)

		for value in split:
			self.nickname += value + ' '
		self.nickname = self.nickname[:-1]