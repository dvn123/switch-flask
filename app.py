from flask import Flask
from flask import jsonify
from bson.objectid import ObjectId
from bson import json_util
import datetime
import json
from flask_pymongo import PyMongo


app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
#app.config["MONGO_URI"] = "mongodb+srv://switch_admin:switch_admin2@flask-switch-larnu.mongodb.net/test?retryWrites=true"
app.config["MONGO_URI"] = "mongodb+srv://switch_admin:switch_admin2@flask-switch-larnu.mongodb.net/dbswitch"
mongo = PyMongo(app)


class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

app.json_encoder = JSONEncoder

@app.route("/")
def hello():
    mongo.db.users.insert_one({'name': 'david'})
    david = mongo.db.users.find({'name': 'david'})
    print(david)
    json_res = []
    for d in david:
        print(d)
        json_res.append(d)
    return jsonify(json_res)


@app.route("/top5")
def asd():
    return mongo.db.websites.find()


if __name__ == "__main__":
    print("asd")
    app.run()

    print(mongo.db.users.insert_one({'name': 'david'}).inserted_id)
    print("asd2")
