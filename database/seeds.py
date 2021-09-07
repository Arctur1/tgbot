import datetime
from random import randrange
from mongo import collection, time_stamp, user_collection

post_test = [{"author": "TestUser",
              "text": "Test post!",
              "tags": ["mongodb", "python", "pymongo"],
              "timestamp": datetime.datetime.utcnow()} for i in range(2)]


def seed():
    collection.insert_many(post_test)
    return


print(post_test)
seed()
