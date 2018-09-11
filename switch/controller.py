import os
from flask import jsonify, Blueprint
from bson import ObjectId
from switch.db import get_db, init_db, update_database
from switch.scraper import get_top_5

ROOT_PATH = os.environ.get('ROOT_PATH')
francesinhas = Blueprint('francesinhas', __name__, url_prefix='/francesinhas')


@francesinhas.route("/top_5", methods=['GET'])
def get_websites():
    websites = list(get_db().websites.find())
    json_res = []
    for website in websites:
        json_res.append(website)
    return jsonify(json_res), 200


@francesinhas.route("/update_top_5", methods=['GET'])
def update_top_5():
    try:
        update_database(get_top_5())
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    finally:
        return jsonify(success=True), 200


@francesinhas.route("/rate/<restaurant_id>/<int:rating>", methods=['PUT'])
def rate_restaurant(restaurant_id, rating):
    try:
        restaurant_id = ObjectId(restaurant_id)
    except Exception as e:
        return jsonify({'success': False, 'message': "String is not a valid ID"}), 400

    restaurant = get_db().websites.find_one({"_id": restaurant_id})
    if restaurant is None:
        return jsonify({'success': False, 'message': 'No restaurant with such an ID'}), 400

    if rating is None or rating > 5 or rating < 0:
        return jsonify({'success': False, 'message': 'Rating must be between 0 and 5'}), 400

    if 'n_ratings' not in restaurant:
        print("First time")
        restaurant['n_ratings'] = 1
        restaurant['rating'] = rating
    else:
        print("Not first time")
        restaurant['n_ratings'] = restaurant['n_ratings'] + 1
        mean = restaurant['rating']
        restaurant['rating'] = mean + (rating - mean)/restaurant['n_ratings']

    mongo_response = get_db().websites.replace_one({"_id": restaurant_id}, restaurant)
    print(mongo_response)
    return jsonify(success=True), 200
