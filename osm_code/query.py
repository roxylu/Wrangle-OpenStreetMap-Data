#!/usr/bin/env python
from pymongo import MongoClient


def get_db(db_name):
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db


def make_pipeline():
    pipeline = [
        {'$match': {'type': {'$exists': 1}}},
        {'$group': {'_id': '$created.user',
                    'count': {'$sum': 1}}},
        {'$sort': {'count': -1}}
    ]
    return pipeline


def aggregate(db, pipeline):
    return [doc for doc in db.shanghai.aggregate(pipeline)]


def process_result(db, result):
    # Number of contributing users
    print "Number of contributing users: "
    total_users = len(result)
    print total_users

    # Top contributing user as a percentage of total documents
    print "Top contributing user as a percentage of total documents:"
    top_user = result[0]
    print "{0:.2f} [%]".format(top_user['count'] * 100.0 / db.shanghai.count())

    # Top 10% of contributing user as a percentage of total documents
    print "Top 10% of contributing user as a percentage of total documents:"
    sum = 0
    for i in range(int(total_users * 0.1)):
        sum += result[i]['count']
    print "{0:.2f} [%]".format(sum * 100.0 / db.shanghai.count())


if __name__ == "__main__":
    db = get_db('osm')
    pipeline = make_pipeline()
    result = aggregate(db, pipeline)
    process_result(db, result)
