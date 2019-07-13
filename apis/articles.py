from bson.objectid import ObjectId
from server import app, mongo
import pymongo
from flask import request
import datetime
import utils


def get_querystr(key, default):
    return request.args.get(key) if key in request.args else default


@app.route('/api/<topic>/articles', methods=['GET'])
def get_topic_articles(topic):
    start = int(get_querystr('start', 0))
    max_count = int(get_querystr('max_count', 10))
    articles = mongo.db.articles.find({'topic': topic}) \
                    .sort([('created_time', pymongo.DESCENDING)]) \
                    .skip(start) \
                    .limit(max_count)
    filtered_articles = []
    for art in articles:
        tmp_art = {}
        for key in art:
            if key not in ['content', '_id', 'audio']:
                tmp_art[key] = art[key]
        filtered_articles.append(tmp_art)
    return utils.response(200, 'Success', list(filtered_articles))


@app.route('/api/articles/<article_id>', methods=['GET'])
def get_article_details(article_id):
    article = mongo.db.articles.find_one({'id': article_id})
    if article is None:
        return utils.response(404, "Article not found", {})
    questions = mongo.db.questions.find({'article_id': article_id})
    ret = {'questions': list(questions)}
    for key in article:
        if key not in ['_id']:
            ret[key] = article[key]
    return utils.response(200, 'Success', dict(ret))
