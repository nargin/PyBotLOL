import discord
import requests
import json
from riotwatcher import LolWatcher, ApiError

def	winrate_ranked(data, lol_watcher):
	try:
		user = lol_watcher.summoner.by_name(data.regions, data.summoner_name)
	except ApiError as err:
		return discord.Embed(title='User not found', description=f'User {data.actual_name} not found', color=0xff0000, type='rich')

	user_id = user['id']

	try:
		ranked_stats = lol_watcher.league.by_summoner(data.regions, user_id)
	except ApiError as err:
		return discord.Embed(title='No ranked stats found', description=f'User {data.actual_name} has no ranked stats', color=0xff0000, type='rich')

	queue_type = 'RANKED_SOLO_5x5'
	if data.option == 'f':
		queue_type = 'RANKED_FLEX_SR'

	queue_ranked_stats = None
	for queue in ranked_stats:
		if queue['queueType'] == queue_type:
			queue_ranked_stats = queue
			break

	if queue_ranked_stats == None:
		return discord.Embed(title='No ranked stats found', description=f'User {data.actual_name} has no ranked stats', color=0xff0000, type='rich')

	wins = queue_ranked_stats['wins']
	losses = queue_ranked_stats['losses']
	winrate = wins / (wins + losses) * 100

	message = f'Wins : {wins} - Losses : {losses} - Winrate : {winrate:.2f}% '
	message += ':warning:' if winrate < 50 else ':white_check_mark:'

	color = 0xff0000 if winrate < 50 else 0x00ff00
	queue_type_message = 'Soloq' if queue_type == 'RANKED_SOLO_5x5' else 'Flex'
	embed = discord.Embed(title=f'{data.actual_name}\'s {queue_type_message} winrate', description=message, color=color, type='rich')
	
	return embed