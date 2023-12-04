import discord
import requests
import json
from riotwatcher import LolWatcher, ApiError

def mastery_champion(data, lol_watcher):
	
	data.option = 3 if data.option == 0 else 20 if data.option > 20 else data.option # 3 at min and 25 at max

	try:
		user = lol_watcher.summoner.by_name(data.regions, data.summoner_name)
	except ApiError as err:
		return discord.Embed(title='User not found', description=f'User {data.summoner_name} not found', color=0xff0000, type='rich')

	user_id = user['id']

	try:
		masteries = lol_watcher.champion_mastery.by_summoner(data.regions, user_id)
	except ApiError as err:
		return discord.Embed(title='User not found', description=f'User {data.summoner_name} not found', color=0xff0000, type='rich')

	masteries = sorted(masteries, key=lambda k: k['championPoints'], reverse=True)

	versions = lol_watcher.data_dragon.versions_for_region(data.regions)
	current_version = versions['n']['champion']

	color_bg = 0xFFB233
	embed = discord.Embed(title=f'{data.summoner_name}\'s mastery', description='', color=color_bg, type='rich')

	num_champs = len(lol_watcher.data_dragon.champions(current_version)['data'])
	# for all champs
	for i in range(data.option):

		champion_id = masteries[i]['championId']
		champion_level = masteries[i]['championLevel']
		champion_points = masteries[i]['championPoints']
		champion_data = lol_watcher.data_dragon.champions(current_version, False, 'en_US')
		
		champion_key = None
		for key, value in champion_data['data'].items():
			if value['key'] == str(champion_id):
				champion_key = key
				break


		champion_name = champion_data['data'][champion_key]['name']
		champion_icon = lol_watcher.data_dragon.champions(current_version)['data'][champion_key]['image']['full']
		champion_icon_url = f'http://ddragon.leagueoflegends.com/cdn/{current_version}/img/champion/{champion_icon}'
		
		match champion_level:
			case 7:
				mastery_icon = '<:mastery_7:1179010217963438172>'
			case 6:
				mastery_icon = '<:mastery_6:1179010170127388772>'
			case 5:
				mastery_icon = '<:mastery_5:1179010136505856011>'
			case 4:
				mastery_icon = '<:mastery_4:1179010098610315264>'
			case 3:
				mastery_icon = '<:mastery_3:1179010071779344437>'
			case 2:
				mastery_icon = '<:mastery_2:1179010025096761416>'
			case 1:
				mastery_icon = '<:mastery_1:1179009953231556638>'
			case _:
				mastery_icon = ':zero:'

		embed.add_field(name=f'{champion_name}', value=f'Level {mastery_icon} - {champion_points}', inline=False)
		if i == 0:
			if champion_level == 7:
				color_bg = 0x3396FF
			elif champion_level == 6:
				color_bg = 0xFF33E9
			elif champion_level == 5:
				color_bg = 0xC42D0B
			embed.set_thumbnail(url=champion_icon_url)

	embed.color = color_bg
	return embed