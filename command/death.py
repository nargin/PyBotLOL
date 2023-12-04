import discord
import requests
import json
from riotwatcher import ApiError

def death_counter(data, lol_watcher):
	try :
		url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{data.puuid}/ids?queue=420&type=ranked&start=0&count=20&api_key={data.lol_token}"
	except ApiError as err:
		print(err)
		return discord.Embed(title='No solo ranked stats found', description=f'User {data.actual_name} has no solo ranked stats', color=0xff0000, type='rich')

	response = requests.get(url)
	if response.status_code != 200:
		return discord.Embed(title='No ranked stats found', description=f'User {data.actual_name} has no ranked stats', color=0xff0000, type='rich')
	
	matchs = response.json()
	number_of_death = 0
	for match in matchs:
		try :
			match_detail = lol_watcher.match.by_id('EUW1', match)
		except ApiError as err:
			print(err)
			return discord.Embed(title='Game not found', description=f'Game {match} not found', color=0xff0000, type='rich')
		
		for participant in match_detail['info']['participants']:
			if participant['puuid'] == data.puuid:
				number_of_death += participant['deaths']
				break
	return discord.Embed(title=f'Deaths of {data.actual_name}', description=f'{number_of_death} deaths in 20 last games', color=0x00ff00, type='rich')