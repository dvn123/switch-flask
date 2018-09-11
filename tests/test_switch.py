import os
import tempfile
import json
import pytest

from switch import create_app
from switch.db import get_db, init_db
from switch.scraper import *


@pytest.fixture
def app():
    app = create_app()

    with app.app_context():
        init_db()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def test_scraper_get_5(client):
    websites = get_top_5()
    assert 'address' in websites[0]
    assert len(websites) == 5


def test_top_5(client, app):
    response = client.get('/francesinhas/top_5')
    json_r = json.loads(response.data)
    assert response.status_code == 200
    assert len(json_r) == 5


@pytest.mark.parametrize(('restaurant_id', 'rating', 'message'), (
        ('a', '4', 'String is not a valid ID'),
        ('5b96d7aa58e15ff446c294c5', '4', 'No restaurant with such an ID'),
        ('5b96d7aa58e15de446c294c5', '6', 'Rating must be between 0 and 5'),
))
def test_register_validate_input(client, restaurant_id, rating, message):
    response = client.put('/francesinhas/rate/'+ restaurant_id + '/' + rating)
    assert response.status_code == 400
    assert message in str(response.data)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('switch.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called