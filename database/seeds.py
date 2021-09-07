import datetime
from random import randrange
from mongo import collection

post_test = [{"author": "TestUser",
              "text": "Test post!",
              "tags": ["mongodb", "python", "pymongo"],
              "timestamp": datetime.datetime.utcnow() - datetime.timedelta(minutes=randrange(10))} for i in range(10)]


def seed():
    collection.insert_many(post_test)
    return


print(post_test)
seed()
