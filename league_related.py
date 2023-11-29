import discord
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

def profile_ranked(data, lol_watcher): # command !pr
	try:
		user = lol_watcher.summoner.by_name(data.regions, data.nickname)
	except ApiError as err:
		return discord.Embed(title='User not found', description=f'User {data.nickname} not found', color=0xff0000, type='rich')

	user_id = user['id']

	try:
		ranked_stats = lol_watcher.league.by_summoner(data.regions, user_id)
	except ApiError as err:
		return discord.Embed(title='No ranked stats found', description=f'User {data.nickname} has no ranked stats', color=0xff0000, type='rich')

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
	
	else:
		message = 'No ranked stats found'


	if soloq_stats != None:	
		embed = discord.Embed(title=f'{data.nickname}\'s soloq rank', description='', color=color, type='rich')
		embed.add_field(name='Soloq :', value=f'{message}', inline=False)
		embed.set_thumbnail(url=f'https://raw.communitydragon.org/latest/game/assets/ux/tftmobile/particles/tft_regalia_{tier.lower()}.png')
	
	if flex_stats != None:
		embed.add_field(name='Flex :', value=f'{tier_flex} {rank_flex} {lp_flex} LP', inline=False)
		embed.add_field(name='', value=f'Wins : {wins_flex} - Losses : {losses_flex} - Winrate : {winrate_flex:.2f}% ', inline=False)
		if soloq_stats == None:
			embed.set_thumbnail(url=f'https://raw.communitydragon.org/latest/game/assets/ux/tftmobile/particles/tft_regalia_{tier_flex.lower()}.png')
	return embed




def	winrate_ranked(data, lol_watcher):
	try:
		user = lol_watcher.summoner.by_name(data.regions, data.nickname)
	except ApiError as err:
		return discord.Embed(title='User not found', description=f'User {data.nickname} not found', color=0xff0000, type='rich')

	user_id = user['id']

	try:
		ranked_stats = lol_watcher.league.by_summoner(data.regions, user_id)
	except ApiError as err:
		return discord.Embed(title='No ranked stats found', description=f'User {data.nickname} has no ranked stats', color=0xff0000, type='rich')

	queue_type = 'RANKED_SOLO_5x5'
	if data.option == 'f':
		queue_type = 'RANKED_FLEX_SR'

	queue_ranked_stats = None
	for queue in ranked_stats:
		if queue['queueType'] == queue_type:
			queue_ranked_stats = queue
			break

	if queue_ranked_stats == None:
		return discord.Embed(title='No ranked stats found', description=f'User {data.nickname} has no ranked stats', color=0xff0000, type='rich')

	wins = queue_ranked_stats['wins']
	losses = queue_ranked_stats['losses']
	winrate = wins / (wins + losses) * 100

	message = f'Wins : {wins} - Losses : {losses} - Winrate : {winrate:.2f}% '
	message += ':warning:' if winrate < 50 else ':white_check_mark:'

	color = 0xff0000 if winrate < 50 else 0x00ff00
	queue_type_message = 'Soloq' if queue_type == 'RANKED_SOLO_5x5' else 'Flex'
	embed = discord.Embed(title=f'{data.nickname}\'s {queue_type_message} winrate', description=message, color=color, type='rich')
	
	return embed




def mastery_champion(data, lol_watcher):
	
	data.option = 3 if data.option == 0 else 20 if data.option > 20 else data.option # 3 at min and 25 at max

	try:
		user = lol_watcher.summoner.by_name(data.regions, data.nickname)
	except ApiError as err:
		return discord.Embed(title='User not found', description=f'User {data.nickname} not found', color=0xff0000, type='rich')

	user_id = user['id']

	try:
		masteries = lol_watcher.champion_mastery.by_summoner(data.regions, user_id)
	except ApiError as err:
		return discord.Embed(title='User not found', description=f'User {data.nickname} not found', color=0xff0000, type='rich')

	masteries = sorted(masteries, key=lambda k: k['championPoints'], reverse=True)

	versions = lol_watcher.data_dragon.versions_for_region(data.regions)
	current_version = versions['n']['champion']

	color_bg = 0xFFB233
	embed = discord.Embed(title=f'{data.nickname}\'s mastery', description='', color=color_bg, type='rich')

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




def profile_user(data, lol_watcher):
	version = lol_watcher.data_dragon.versions_for_region(data.regions)['n']['champion']

	try:
		user = lol_watcher.summoner.by_name(data.regions, data.nickname)
	except ApiError as err:
		return discord.Embed(title='User not found', description=f'User {data.nickname} not found', color=0xff0000, type='rich')

	nick = user['name']
	level = user['summonerLevel']
	icon = user['profileIconId']
	icon_url = f'http://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{icon}.png'
	

	print(f'{nick} {level} {icon_url}')

	embed = discord.Embed(title=f'{nick}', description=f'Level {level}', color=0x00ff00, type='rich')
	embed.set_thumbnail(url=icon_url)
	return embed