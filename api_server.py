import json
from datetime import datetime
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from recommendation.recommender import QuestionRecommender


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__, static_folder='data')
CORS(app)
app.config.from_pyfile('configs/constants.py')
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
app.json_encoder = JSONEncoder
question_recommender = QuestionRecommender()

from apis.articles import *
from apis.users import *


if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'])