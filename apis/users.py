from api_server import app, mongo, bcrypt
from flask import request
from datetime import datetime
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



@app.route('/api/user_answers', methods=['POST'])
def user_answer():
    user_id = request.headers.get('User-Id')
    if user_id is None:
        return utils.response(400, 'Unauthorized')
    data = request.get_json()
    q_count = len(data['questions'])
    correct_count = 0
    saved_data = []
    for ques, u_ans in zip(data['questions'], data['answers']):
        r_answer = ques['answer']
        is_correct = r_answer.lower() == u_ans.lower()
        if is_correct:
            correct_count += 1
        tmp_data = {
            'u_answer': u_ans,
            'u_id': user_id,
            'q_id': ques['id'],
            'a_id': ques['article_id'],
            "q_tags": ques['tags'],
            'level': ques['level'],
            'is_correct': is_correct,
            'submited_time': datetime.utcnow()
        }
        saved_data.append(tmp_data)

    mongo.db.user_answers.insert_many(saved_data)

    return utils.response(200, "Success", {'sum': q_count, 'correct': correct_count})
