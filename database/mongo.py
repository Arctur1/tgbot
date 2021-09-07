import pymongo
import datetime

client = pymongo.MongoClient('localhost', 27017)
db = client['TelegramPost']
collection = db['test']
user_collection = db['users']


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
