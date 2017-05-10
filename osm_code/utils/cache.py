from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017')
db = client.cache


def get_cache(en_value):
    """
    try to get the cached chinses translated value
    return [] if not exsits.
    """
    query = {'en': en_value}
    result = list(db.translate.find(query))
    if result:
        result = result[0].get('ch')
    return result


def set_cache(en_value, ch_value):
    """
    set cached translated result with given values
    """
    db.translate.insert({'en': en_value, 'ch': ch_value})
