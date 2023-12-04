# Not used anymore



def add_alias(alias_list, new_alias, name_ref):
	alias_list[new_alias] = name_ref
	return 'Alias added'

def del_alias(alias_list, alias):
	if alias in alias_list:
		del alias_list[alias]
		return alias_list
	else:
		return 'Alias not found'

def edit_alias(alias_list, alias, name_ref):
	if alias in alias_list:
		alias_list[alias] = name_ref
		return alias_list
	else:
		return 'Alias not found'


def command_alias(data):

	if data.option == 'l':
		alias_list = 'Alias list :\n'
		for alias, name in command_alias.list_name.items():
			alias_list += f'{alias} -> {name}\n'
		return alias_list

	if data.alias_name == None or data.summoner_name == None:
		return None
	
	if data.alias_name in command_alias.list_name and data.option == 'a':
		return 'Alias already exists'

	match data.option:
		case 'a':
			add_alias(command_alias.list_name, data.alias_name, data.summoner_name)
			return f'Alias {data.alias_name} added to {data.summoner_name}'

		case 'd':
			del_alias(command_alias.list_name, data.alias_name)
			return f'Alias {data.alias_name} deleted from {data.alias_name}'

		case 'e':
			edit_alias(command_alias.list_name, data.alias_name, data.summoner_name)
			return f'Alias {data.alias_name} edited'

		case _:
			return 'Error'


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