""" index file for REST APIs using Flask """
import os
import sys
from flask import Flask
from flask import jsonify, request, make_response, send_from_directory

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))

#app = Flask(__name__)
from switch import app

# Port variable to run the server on.
#PORT = os.environ.get('PORT')
PORT = 5000
#IP = os.environ.get('IP')
IP = "127.0.0.1"


@app.route("/")
def hello_world():
    return "Hello World!"


if __name__ == '__main__':
    #app.config['DEBUG'] = os.environ.get('ENV') == 'development'  # Debug mode if development env
    app.run(host=IP, port=int(PORT))  # Run the app