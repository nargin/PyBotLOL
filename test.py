
def add_alias(new_alias, name_ref):
	if not hasattr(add_alias, 'list_name'):
		add_alias.list_name = {}
	
	if new_alias == None or name_ref == None:
		return None
	
	if new_alias in add_alias.list_name:
		return 'Alias already exists'
	
	add_alias.list_name[new_alias] = name_ref
	return add_alias.list_name

# get input from user


while True:
	alias = input("Enter your alias: ")
	name = input("Enter your name: ")

	list_alias = add_alias(alias, name)
	if list_alias == None:
		print('Error')
	else:
		print(list_alias)