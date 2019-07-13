from pymongo import MongoClient
import datetime
import random 
import os
import uuid
import shutil


MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'agc2019'
STATIC_FOLDER = 'static' # Change this path to webserver/static
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]


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
        thumbnail_path = get_save_path(generate_filename()[:8] + '.' \
                                            + article['thumbnail'].split('.')[-1])
        shutil.copyfile(article['thumbnail'], thumbnail_path)
        final_article['thumbnail'] = '/' + thumbnail_path

    # Save audio file
    if 'audio' in article and article['audio'] != '':
        audio_path = get_save_path(generate_filename()[:8] + '.' \
                                            + article['audio'].split('.')[-1])
        shutil.copyfile(article['audio'], audio_path)
        final_article['audio'] = '/' + audio_path

    # Save article to db
    db.articles.insert_one(final_article)

    for qs in article['questions']:
        qs['id'] = generate_filename()
        qs['article_id'] = article_id
        db.questions.insert_one(qs)

    print("Saved article: ", article['title'])




if __name__ == '__main__':
    sample_input = {
        "topic": "society",
        "thumbnail": "data/xb.jpg",
        "type": "audio",
        "title": "How to spend money after winning hackathon challenge?",
        "level": "medium",
        "content": "<div></div>",
        "audio": "data/die.wav",
        "publisher":"bbc",
        "source_url": "https://www.bbc.co.uk/",
        "questions": [{
            "content": "Who is president of the USA",
            "options": [
                "Bui Manh Thang",
                "Luong Tung Dung",
                "Phan Ngoc Lan",
                "Bui Duy Tuan"
            ],
            "answer": "Bui Manh Thang",
            "type": "choice"
        }]
    }
    save_article(sample_input)
