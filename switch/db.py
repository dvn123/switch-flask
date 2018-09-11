from flask_pymongo import PyMongo
from flask import current_app, g
from flask.cli import with_appcontext
import click
import datetime
from datetime import timedelta
def get_db():
    if 'db' not in g:
        g.db = PyMongo(current_app).db

    return g.db


def init_db():
    db = get_db()
    websites = list(db.websites.find())
    if len(websites) == 5:
        yesterday = datetime.datetime.utcnow() - timedelta(days=1)
        for website in websites:
            if website['last-modified'] < yesterday:
                return update_database(current_app.scraper())
    else:
        db.websites.drop()
        return update_database(current_app.scraper())



@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.cli.add_command(init_db_command)
    init_db()


def update_database(websites):
    names = []
    for website in websites:
        g.db.websites.update_one({'name': website['name']},
                                  {'$set': {'address': website['address'],
                                            'email': website['email'],
                                            'link': website['link'],
                                            'name': website['name'],
                                            'last-modified': datetime.datetime.utcnow(),
                                            'phone-number': website['phone-number']}}, upsert=True
                                 )
        names.append(website['name'])
    g.db.websites.delete_many({"name": {"$nin": names}})
