from server import app, mongo
from flask import request
import utils


def unauthorized_response(callback):
    return utils.response(401, 'Unauthorized')


@app.route('/api/user_answer', methods=['POST'])
def user():
    user_id = request.headers.get('user_id')
    data = request.get_json()
    # data = {
    #     "article_id": "121212",
    #     "answers": ["Thang", "Dung", "Tuan", "Lan", "Dat"],
    #     "score": 8.5,
    #     "user_id": user_id
    # }
    mongo.user_answer.insert_one(data)
    return utils.response(200, "Success")
