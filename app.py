from flask import Flask
from flask import jsonify
from bson.objectid import ObjectId
import datetime
import json
from scraper import get_top_5
from flask_pymongo import PyMongo


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


def update_database(websites):
    names = []
    for website in websites:
        mongo.db.websites.replace_one({'name': website['name']}, website, upsert=True)
        names.append(website['name'])
    mongo.db.websites.delete_many({"name": {"$nin": names}})


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://switch:switch1@flask-switch-larnu.mongodb.net/dbswitch"
mongo = PyMongo(app)
app.json_encoder = JSONEncoder
update_database(get_top_5())


'''@app.route("/")
def hello():
    return "Hello"


@app.route("/up")
def hello():
    return "Hello"


@app.route("/top5")
def get_websites():
    websites = list(mongo.db.websites.find())
    json_res = []
    for website in websites:
        json_res.append(website)
    return jsonify(json_res)


if __name__ == "__main__":
    app.run()
'''