import json
import os
from bson import ObjectId
import datetime
from flask import Flask
from switch.scraper import get_top_5


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='switch1',
        MONGO_URI=os.environ.get('DB') or "mongodb+srv://switch:switch1@flask-switch-larnu.mongodb.net/dbswitch",
        DEBUG=os.environ.get('ENV') or "development"
    )
    app.scraper = get_top_5
    from . import db
    with app.app_context():
        db.init_app(app)
    from switch.controller import francesinhas
    app.register_blueprint(francesinhas)
    app.json_encoder = JSONEncoder
    return app
