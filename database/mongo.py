import pymongo
import datetime
from settings import *
import asyncio

client = pymongo.MongoClient(ADDRESS, PORT)
db = client[DB]
collection = db['test']
user_collection = db['users']
stats_collection = db['collections_stats']


def update_stats():
    count = collection.find().count()
    stats_collection.update_one({'collection': 'test'}, {'$set': {'collection': 'test', 'count': count}}, upsert=True)


def show_stats():
    stats = list(stats_collection.find({'collection': 'test'}))[0]['count']
    return stats


def count():
    res = collection.find().count()
    return res


def find_posts(user_id):  # Finds posts created after latest user look-up
    user = list(user_collection.find({"user": user_id}))
    if len(user) == 1:
        user_time_stamp = user[0]["timestamp"]
    else:
        user_collection.insert({"user": user_id, "timestamp": datetime.datetime.min})
        user_time_stamp = list(user_collection.find({"user": user_id}))[0]["timestamp"]

    res = list(collection.find({
        "timestamp": {
            "$gte": user_time_stamp
            }}))
    return str(res)


def time_stamp(user): # Updates latest user look-up
    user_collection.update({"user": user}, {"user": user, "timestamp": datetime.datetime.utcnow()}, upsert=True)
