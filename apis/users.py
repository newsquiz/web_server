from server import app, mongo, bcrypt
from flask import request
import utils


@app.route('/api/register', methods=['POST'])
def register():
    try:
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
    except:
        return utils.response(400, 'Missing required information')
    if len(email) < 10 or '@' not in email or len(password) < 6:
        return utils.response(400, 'Email is not valid or password is too short')
    uid = utils.generate_numid()
    password_hash = bcrypt.generate_password_hash(password)
    try:
        user_exists = mongo.db.users.find_one({'email': email})
    except:
        user_exists = None
    if user_exists is not None:
        return utils.response(400, 'This email address is already used')
    mongo.db.users.insert_one({
        'name': name,
        'email': email,
        'id': uid,
        'password': password_hash
    })
    return utils.response(200, 'Success', {'id': uid})



@app.route('/api/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
    except:
        return utils.response(400, 'Bad request')
    user = mongo.db.users.find_one({'email': email})
    if user is None:
        return utils.response(400, 'Email or password is not correct')
    pw_hash = user['password']
    is_valid = bcrypt.check_password_hash(pw_hash, password)
    if not is_valid:
        return utils.response(400, 'Email or password is not correct')
    return utils.response(200, 'Success', {'id': user['id']})



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
    mongo.db.user_answer.insert_one(data)
    return utils.response(200, "Success")
