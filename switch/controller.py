import os
from flask import request, jsonify
from bson import ObjectId
from app import app, mongo

ROOT_PATH = os.environ.get('ROOT_PATH')


@app.route("/top5", methods=['GET'])
def get_websites():
    websites = list(mongo.db.websites.find())
    json_res = []
    for website in websites:
        json_res.append(website)
    return jsonify(json_res)


@app.route("/rate/<restaurant_id>/<int:rating>", methods=['PUT'])
def rate_restaurant(restaurant_id, rating):
    if restaurant_id is None:
         return jsonify({'ok': False, 'message': 'Empty restaurant ID'}), 400
    restaurant_id = ObjectId(restaurant_id)
    restaurant = mongo.db.websites.find_one({"_id": restaurant_id})
    print(restaurant)
    if restaurant is None:
        return jsonify({'ok': False, 'message': 'Invalid restaurant ID'}), 400

    if rating is None or rating > 5 or rating < 0:
        jsonify({'ok': False, 'message': 'Rating Must be between 0 and 5'}), 400

    if 'n_ratings' not in restaurant:
        print("First time")
        restaurant['n_ratings'] = 1
        restaurant['rating'] = rating
        mongo_response = mongo.db.websites.replace_one({"_id": restaurant_id}, restaurant)
        print(mongo_response)
        return jsonify(), 200
    else:
        print("Not first time")
        restaurant['n_ratings'] = restaurant['n_ratings'] + 1
        mean = restaurant['rating']
        restaurant['rating'] = mean + (rating - mean)/restaurant['n_ratings']

        mongo_response = mongo.db.websites.replace_one({"_id": restaurant_id}, restaurant)
        print(mongo_response)
        return jsonify(), 200