from pymongo import MongoClient
import datetime
import random 
import os
import uuid
import shutil
from configs import constants


MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'agc2019'
STATIC_FOLDER = 'static' # Change this path to webserver/static
client = MongoClient(constants.MONGO_URI)
db = client[constants.MONGO_DB]


def generate_filename():
    fname = uuid.uuid5(uuid.NAMESPACE_OID, str(datetime.datetime.now()))
    return str(fname).replace('-', '')


def get_save_path(filename):
    datetime_str = str(datetime.datetime.now()).replace('.', '_')
    date_str = datetime_str.split(' ')[0]
    save_path = os.path.join(STATIC_FOLDER, date_str)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    image_path = os.path.join(save_path, filename)
    return image_path


def save_article(article):
    article_id = generate_filename()
    final_article = {}
    final_article['id'] = article_id
    final_article['created_time'] = datetime.datetime.utcnow()
    for key in article:
        if key not in ['questions']:
            final_article[key] = article[key]

    # Save thumbnail image
    if 'thumbnail' in article and article['thumbnail'] != '':
        if article['thumbnail'][:4] != 'http':
            thumbnail_path = get_save_path(generate_filename()[:8] + '.' \
                                                + article['thumbnail'].split('.')[-1])
            shutil.copyfile(article['thumbnail'], thumbnail_path)
            final_article['thumbnail'] = '/' + thumbnail_path
        else:
            final_article['thumbnail'] = article['thumbnail']

    # Save audio file
    if 'audio' in article and article['audio'] != '':
        if article['audio'][:4] != 'http':
            audio_path = get_save_path(generate_filename()[:8] + '.' \
                                                + article['audio'].split('.')[-1])
            shutil.copyfile(article['audio'], audio_path)
            final_article['audio'] = '/' + audio_path
        else:
            final_article['audio'] = article['audio']

    # Save article to db
    db.articles.insert_one(final_article)

    for qs in article['questions']:
        qs['id'] = generate_filename()
        qs['article_id'] = article_id
        db.questions.insert_one(qs)

    print("Saved article: ", article['title'])


def n_previous_day(n):
    return datetime.datetime.now() - datetime.timedelta(days=n)


if __name__ == '__main__':
    num_items = min(10, 50)
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    result = list(db.user_click.aggregate([
        { '$match': { 'clicked_time': {'$gt': n_previous_day(3)} } },
        { '$group': { '_id': '$a_id', 'total': { '$sum': 1 } } },
        { '$sort': { 'total': -1 }},
        { '$limit': 50}
    ]))
    popular_ids = [x['_id'] for x in result[:num_items]]
    popular_items = list(db.articles.find({'id': {'$in': popular_ids}, 'flag': 1}))

    remaining_count = num_items - len(popular_ids)
    if remaining_count > 0:
        articles = db.articles.aggregate([
            {'$sample': {'size': remaining_count}},
            {'$match': {
                    'id': {'$nin': popular_ids}, 
                    'flag': 1
                    # 'publish_time': {'$gt': n_previous_day(30)}
                }
            }
        ])
        popular_items.extend(list(articles))
    # tags = db.questions.distinct('article_id', {})
    # articles = db.articles.find({'flag': 1})
    # print(len(list(articles)))
    # all_ai = []
    # for item in tags:
    #     all_ai.append(item['type'])
    # all_ai = set(all_ai)
    print(popular_ids)
    print([x['id'] for x in popular_items])
