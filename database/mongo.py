import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client['TelegramPost']
collection = db['test']


def count():
    res = collection.find().count()
    return res


def find_posts():
    res = list(collection.find().sort([('timestamp', -1)]).limit(1))
    return str(res)


