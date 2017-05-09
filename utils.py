from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.cache

def get_cache(en_value):
    query = {'en': en_value }
    result = list(db.translate.find(query))
    if result:
        result = result[0].get('ch')
    return result 


def set_cache(en_value, ch_value):
    db.translate.insert({'en': en_value, 'ch': ch_value})
