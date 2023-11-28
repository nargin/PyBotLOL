import discord
import json
from riotwatcher import LolWatcher, ApiError

def mastery_champion(summoner_name, lol_watcher):
	try:
		user = lol_watcher.summoner.by_name('euw1', summoner_name)
	except ApiError as err:
		return discord.Embed(title='User not found', description=f'User {summoner_name} not found', color=0xff0000, type='rich')

	user_id = user['id']

	try:
		masteries = lol_watcher.champion_mastery.by_summoner('euw1', user_id)
	except ApiError as err:
		return discord.Embed(title='User not found', description=f'User {summoner_name} not found', color=0xff0000, type='rich')

	masteries = sorted(masteries, key=lambda k: k['championPoints'], reverse=True)

	versions = lol_watcher.data_dragon.versions_for_region('euw1')
	current_version = versions['n']['champion']

	embed = discord.Embed(title=f'{summoner_name}\'s mastery', description='', color=0x00ff00, type='rich')

	for i in range(3):

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
		
		embed.add_field(name=f'{champion_name}', value=f'Level {champion_level} - {champion_points} points', inline=False)
		if i == 0:
			embed.set_thumbnail(url=champion_icon_url)

	return embed




def profile_user(summoner_name, lol_watcher):
	version = lol_watcher.data_dragon.versions_for_region('euw1')['n']['champion']

	try:
		user = lol_watcher.summoner.by_name('euw1', summoner_name)
	except ApiError as err:
		return discord.Embed(title='User not found', description=f'User {summoner_name} not found', color=0xff0000, type='rich')

	nick = user['name']
	level = user['summonerLevel']
	icon = user['profileIconId']
	icon_url = f'http://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{icon}.png'

	print(f'{nick} {level} {icon_url}')

	embed = discord.Embed(title=f'{nick}', description=f'Level {level}', color=0x00ff00, type='rich')
	embed.set_thumbnail(url=icon_url)
	return embed