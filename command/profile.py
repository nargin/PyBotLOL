import discord
import requests
import json
from riotwatcher import LolWatcher, ApiError

def color_ranked(tier):
	match tier:
		case 'IRON':
			color = 0x434343
		case 'BRONZE':
			color = 0x8B4513
		case 'SILVER':
			color = 0xC0C0C0
		case 'GOLD':
			color = 0xFFD700
		case 'PLATINUM':
			color = 0x00FFFF
		case 'EMERALD':
			color = 0x00FF00
		case 'DIAMOND':
			color = 0x00BFFF
		case 'MASTER':
			color = 0xFF00FF
		case 'GRANDMASTER':
			color = 0xFF0000
		case 'CHALLENGER':
			color = 0xFFA500
		case _:
			color = 0x000000
	return color

def profile_user(data, lol_watcher):
	version = lol_watcher.data_dragon.versions_for_region(data.regions)['n']['champion']

	try:
		user = lol_watcher.summoner.by_name(data.regions, data.summoner_name)
	except ApiError as err:
		return discord.Embed(title='User not found', description=f'User {data.summoner_name} not found', color=0xff0000, type='rich')

	nick = user['name']
	level = user['summonerLevel']
	icon = user['profileIconId']
	icon_url = f'http://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{icon}.png'
	

	print(f'{nick} {level} {icon_url}')

	embed = discord.Embed(title=f'{nick}', description=f'Level {level}', color=0x00ff00, type='rich')
	embed.set_thumbnail(url=icon_url)
	return embed

def profile_ranked(data, lol_watcher): # command !pr
	try:
		user = lol_watcher.summoner.by_name(data.regions, data.summoner_name)
	except ApiError as err:
		return discord.Embed(title='User not found', description=f'User {data.summoner_name} not found', color=0xff0000, type='rich')

	user_id = user['id']

	try:
		ranked_stats = lol_watcher.league.by_summoner(data.regions, user_id)
	except ApiError as err:
		return discord.Embed(title='No ranked stats found', description=f'User {data.summoner_name} has no ranked stats', color=0xff0000, type='rich')

	soloq_stats = None
	for queue in ranked_stats:
		if queue['queueType'] == 'RANKED_SOLO_5x5':
			soloq_stats = queue
			break

	flex_stats = None
	for queue in ranked_stats:
		if queue['queueType'] == 'RANKED_FLEX_SR':
			flex_stats = queue
			break

	if soloq_stats != None:
		tier = soloq_stats['tier']
		rank = soloq_stats['rank']
		lp = soloq_stats['leaguePoints']
		wins = soloq_stats['wins']
		losses = soloq_stats['losses']
		winrate = wins / (wins + losses) * 100

	if flex_stats != None:
		tier_flex = flex_stats['tier']
		rank_flex = flex_stats['rank']
		lp_flex = flex_stats['leaguePoints']
		wins_flex = flex_stats['wins']
		losses_flex = flex_stats['losses']
		winrate_flex = wins_flex / (wins_flex + losses_flex) * 100


	color = 0x000000
	if soloq_stats != None:
		color = color_ranked(tier)

	elif flex_stats != None:
		color = color_ranked(tier_flex)



	if soloq_stats != None:
		message = f'{tier} {rank} {lp} LP\n'
		message += f'Wins : {wins} - Losses : {losses} - Winrate : {winrate:.2f}% '
	
	elif flex_stats != None:
		message = f'{tier_flex} {rank_flex} {lp_flex} LP\n'
		message += f'Wins : {wins_flex} - Losses : {losses_flex} - Winrate : {winrate_flex:.2f}% '
	
	embed = discord.Embed(title=f'{data.actual_name}\'s ranked stats', description='', color=color, type='rich')

	if soloq_stats == None and flex_stats == None:
		embed.add_field(name='No ranked stats found', value='', inline=False)
		return embed

	if soloq_stats != None:	
		embed = discord.Embed(title=f'{data.actual_name}\'s soloq rank', description='', color=color, type='rich')
		embed.add_field(name='Soloq :', value=f'{message}', inline=False)
		embed.set_thumbnail(url=f'https://raw.communitydragon.org/latest/game/assets/ux/tftmobile/particles/tft_regalia_{tier.lower()}.png')
	
	if flex_stats != None:
		embed.add_field(name='Flex :', value=f'{tier_flex} {rank_flex} {lp_flex} LP', inline=False)
		embed.add_field(name='', value=f'Wins : {wins_flex} - Losses : {losses_flex} - Winrate : {winrate_flex:.2f}% ', inline=False)
		if soloq_stats == None:
			embed.set_thumbnail(url=f'https://raw.communitydragon.org/latest/game/assets/ux/tftmobile/particles/tft_regalia_{tier_flex.lower()}.png')
	


	return embed