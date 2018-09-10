from app import app, mongo


def update_database(websites):
    names = []
    for website in websites:
        mongo.db.websites.replace_one({'name': website['name']}, website, upsert=True)
        names.append(website['name'])
    mongo.db.websites.delete_many({"name": {"$nin": names}})
