#!/usr/bin/env python
from pymongo import MongoClient


def get_db(db_name):
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db


def make_pipeline_for_unique_users():
    pipeline = [
        {'$match': {'type': {'$exists': 1}}},
        {'$group': {'_id': '$created.user',
                    'count': {'$sum': 1}}},
        {'$sort': {'count': -1}}
    ]
    return pipeline


def make_pipeline_for_yearly_contribution():
    pipeline = [
        {'$project': {
            'contribute_year': {'$substr': ['$created.timestamp', 0, 4]}
        }},
        {'$group': {'_id': '$contribute_year',
                    'count': {'$sum': 1}}},
        {'$sort': {'_id': 1}}
    ]
    return pipeline


def make_pipeline_for_shops():
    pipeline = [
        {'$match': {'shop': {'$exists': 1}}},
        {'$group': {'_id': '$shop',
                    'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 5}
    ]
    return pipeline


def make_pipeline_for_supermarket():
    pipeline = [
        {'$match': {'shop': 'supermarket',
                    'name': {'$exists': 1}}},
        {'$group': {'_id': '$name',
                    'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 5}
    ]
    return pipeline


def make_pipeline_for_nodes():
    pipeline = [
        {'$match': {'type': 'node',
                    'address': {'$exists': 0}}},
        {'$group': {'_id': 'Nodes_without_address',
                    'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 5}
    ]
    return pipeline


def make_pipeline_for_streets():
    pipeline = [
        {'$match': {'address.street': {'$exists': 1}}},
        {'$group': {'_id': '$address.street',
                    'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 5}
    ]
    return pipeline


def aggregate(db, pipeline):
    return [doc for doc in db.shanghai.aggregate(pipeline)]


if __name__ == "__main__":
    db = get_db('osm')

    pipeline = make_pipeline_for_unique_users()
    result = aggregate(db, pipeline)
    # Number of contributing users
    print "Number of contributing users: "
    total_users = len(result)
    print total_users
    print "==========================================="

    # Top contributing user as a percentage of total documents
    print "Top contributing user as a percentage of total documents:"
    top_user = result[0]
    print "{0:.2f} [%]".format(top_user['count'] * 100.0 / db.shanghai.count())
    print "==========================================="

    # Top 10% of contributing user as a percentage of total documents
    print "Top 10% of contributing user as a percentage of total documents:"
    sum = 0
    for i in range(int(total_users * 0.1)):
        sum += result[i]['count']
    print "{0:.2f} [%]".format(sum * 100.0 / db.shanghai.count())
    print "==========================================="

    pipeline = make_pipeline_for_yearly_contribution()
    result = aggregate(db, pipeline)
    # Contributions by year
    print "Contributions by year:"
    print "Year: Contributions"
    for year in result:
        print year['_id'] + ": " + str(year['count'])
    print "==========================================="

    # Number of top 5 shops
    print "Number of top 5 shops:"
    pipeline = make_pipeline_for_shops()
    result = aggregate(db, pipeline)
    for shop in result:
        print shop['_id'] + ": " + str(shop['count'])
    print "==========================================="

    # Number of top 5 supermarket
    print "Number of top 5 supermarket:"
    pipeline = make_pipeline_for_supermarket()
    result = aggregate(db, pipeline)
    for shop in result:
        print shop['_id'] + ": " + str(shop['count'])
    print "==========================================="

    # Number of nodes without addresses
    print "Number of nodes without addresses:"
    pipeline = make_pipeline_for_nodes()
    result = aggregate(db, pipeline)
    for node in result:
        print node['_id'] + ": " + str(node['count'])
    print "==========================================="

    # Number of top 5 street addresses
    print "Number of top 5 street addresses:"
    pipeline = make_pipeline_for_streets()
    result = aggregate(db, pipeline)
    for node in result:
        print node['_id'] + ": " + str(node['count'])
