from pymongo import MongoClient
from bson.objectid import ObjectId


_MONFO_URL = '127.0.0.1'

_DATA_DB = 'firestone-data'

data_client = MongoClient(_MONFO_URL, 27018)
data_db = data_client[_DATA_DB]
res = data_db['trade_lock'].find_one({})
print(res)
data_db['trade_lock'].insert({'lock' : 1})
res = data_db['trade_lock'].find_one({})
print(res)
data_db['trade_lock'].remove()
res = data_db['trade_lock'].find_one({})
print(res)
