from bson.objectid import ObjectId
from api_server import app, mongo, question_recommender
import pymongo
from flask import request
import datetime
import utils


def get_querystr(key, default):
    return request.args.get(key) if key in request.args else default


def filter(data, ignores):
    filtered = []
    for item in data:
        tmp_item = {}
        for key in item:
            if key not in ignores:
                tmp_item[key] = item[key]
        filtered.append(tmp_item)
    return filtered


@app.route('/api/<topic>/articles', methods=['GET'])
def get_topic_articles(topic):
    start = int(get_querystr('start', 0))
    max_count = int(get_querystr('max_count', 10))
    topic_search = {} if topic == 'new' else {'topic': topic}
    topic_search['flag'] = 1
    articles = mongo.db.articles.find(topic_search) \
                    .sort([('created_time', pymongo.DESCENDING)]) \
                    .skip(start) \
                    .limit(max_count)
    data = list(filter(articles, ['content', '_id', 'audio', 'content_raw']))
    return utils.response(200, 'Success', data)


@app.route('/api/articles/<article_id>', methods=['GET'])
def get_article_details(article_id):
    user_id = request.headers.get('User-Id')
    article = mongo.db.articles.find_one({'id': article_id})
    if article is None:
        return utils.response(404, "Article not found", {})
    questions = list(mongo.db.questions.find({'article_id': article_id}))
    questions = question_recommender.recommend(questions, user_id)
    questions = filter(questions, ['answer', 'explain'])
    ret = {'questions': list(questions)}
    for key in article:
        if key not in ['_id']:
            ret[key] = article[key]
    return utils.response(200, 'Success', dict(ret))


@app.route('/api/search', methods=['GET'])
def search():
    start = int(get_querystr('start', 0))
    max_count = int(get_querystr('max_count', 10))
    conditions = []
    fields = ['title', 'level', 'publisher', 'type', 'topic', 'content']
    for fld in fields:
        query_str = get_querystr(fld, None)
        if query_str is None:
            continue
        conditions.append({
            fld: {
                '$regex': '.*%s.*' % query_str,
                '$options': 'i'
            }    
        })
    if len(conditions) == 0:
        conditions.append({
            'title': {
                '$regex': '.*'
            }
        })
    articles = mongo.db.articles.find({'$or': conditions, 'flag': 1}) \
                                .sort([('created_time', pymongo.DESCENDING)]) \
                                .skip(start) \
                                .limit(max_count)
    
    data = list(filter(articles, ['content', '_id', 'audio', 'content_raw']))
    return utils.response(200, 'Success', data)


@app.route('/api/recommend/articles', methods=['GET'])
def recommend():
    num_item = int(get_querystr('num_item', 3))
    articles = mongo.db.articles.aggregate([{'$sample': {'size': num_item}}])
    data = list(filter(articles, ['content', '_id', 'audio', 'content_raw']))
    return utils.response(200, 'Success', data)


def generate_questions(content):
    return list(mongo.db.questions.find().skip(0).limit(50))


@app.route('/api/generate_questions', methods=['POST'])
def api_generate_questions():
    user_id = request.headers.get('User-Id')
    json_data = request.get_json()
    if 'content' not in json_data or len(json_data['content']) < 20:
        return utils.response(400, 'Content is not valid')
    content = json_data['content']
    num_sent = sum([1 if len(sent) > 20 else 0 for sent in content.split('.')])
    max_count = min(num_sent, 10)
    questions = generate_questions(content)
    questions = question_recommender.recommend(questions, user_id, max_count=max_count)
    return utils.response(200, 'Success', questions)
