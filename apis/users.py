from server import app, mongo
from flask import request


def unauthorized_response(callback):
    return utils.response(401, 'Unauthorized')


@app.route('/api/user', methods=['GET', 'DELETE', 'PUT'])
def user():
    current_user_email = get_jwt_identity()
    user = mongo.db.users.find_one({'email': current_user_email})
    if user is None:
        return utils.response(404, 'Không tìm thấy người dùng')
    if request.method == 'GET':
        return utils.response(200, 'Thành công', user)

    if request.method == 'DELETE':
        db_response = mongo.db.users.delete_one({'email': current_user_email})
        return utils.response(200, 'Thành công')

    if request.method == 'PUT':
        data = request.get_json()
        is_valid, data = utils.validate_data(data, constants.USER_FIELDS, constants.USER_REQUIRED_FIELD)
        if is_valid:
            if data['email'] != current_user_email:
                return utils.response(400, 'Không thể thay đổi email')
            mongo.db.users.update_one({'email': current_user_email}, {'$set': data})
            return utils.response(200, 'Thành công', data)
        else:
            return utils.response(400, 'Vui lòng nhập đầy đủ thông tin')
