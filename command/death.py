import discord
import requests
import json

def death_counter(data, lol_watcher):
	print(data.puuid)
	try :
		url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{data.puuid}/ids?queue=420&type=ranked&start=0&count=20&api_key={data.lol_token}"
	except ApiError as err:
		print(err)
		return discord.Embed(title='No ranked stats found', description=f'User {data.actual_name} has no ranked stats', color=0xff0000, type='rich')

	response = requests.get(url)
	if response.status_code != 200:
		return discord.Embed(title='No ranked stats found', description=f'User {data.actual_name} has no ranked stats', color=0xff0000, type='rich')
	
	matchs = response.json()
	for match in matchs:
		
	print(matchs)
	return discord.Embed(title='No ranked stats found', description=f'User {data.actual_name} has no ranked stats', color=0xff0000, type='rich')