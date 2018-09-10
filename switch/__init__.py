import os
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
from scraper import get_top_5
from switch.db import update_database

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


# create the flask object
app = Flask(__name__)

# add mongo url to flask config, so that flask_pymongo can use it to make connection
#app.config['MONGO_URI'] = os.environ.get('DB')
app.config['MONGO_URI'] = "mongodb+srv://switch:switch1@flask-switch-larnu.mongodb.net/dbswitch"
mongo = PyMongo(app)
update_database(get_top_5())

# use the modified encoder class to handle ObjectId & datetime object while jsonifying the response.
app.json_encoder = JSONEncoder


from switch.controller import *