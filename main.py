import json

from models.maria_db_2_maria_db_sync import operator

data = json.load(open('config/db_info.json'))

operator(database_configuration=data)
