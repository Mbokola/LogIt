from db import DB

database = DB()

result = database.get_table('Test_Log')
print(result)
