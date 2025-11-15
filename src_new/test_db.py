from databaseModules.classUsersDB import UsersDB_module


# print(CreatorTables().create_regions())
# print(CreatorTables().create_cities())
# print(CreatorTables().create_roles())
# print(CreatorTables().create_users())

print(UsersDB_module().select_with_mail(mail='fin2@gmail.com'))
# print(UsersDB_module().check_presence_mail(mail='oleg@mail.ru'))

# CityRegionDB_module().get_cities_list_with_region()