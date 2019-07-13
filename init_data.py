from bson.objectid import ObjectId
from pymongo import MongoClient
import datetime
import numpy as np
from utils import generate_filename
import random 

topics  = ['economy', 'society', 'sports', 'recommended', 'politics']
levels = ['easy', 'medium', 'hard']
publishers = ['wsj', 'bbc', 'kenh14']
types = ['text', 'audio']
articles = [
    {
        'id': generate_filename(),
        'topic': random.choice(topics),
        'created_time': datetime.datetime.utcnow(),
        'thumbnail': 'https://cdn.vuetifyjs.com/images/cards/docks.jpg',
        'type': random.choice(types),
        'audio': 'http://localhost:5000/audios/audio.mp3',
        'title': 'How to win a hackathon challenge?',
        'content': 'Template content',
        'publisher': random.choice(publishers),
        'source_url': 'https://www.bbc.co.uk/',
        'level': random.choice(levels)
    } for _ in range(200)
]

# articles = [
#     {
#         'id': generate_filename(),
#         'topic': 'society',
#         'created_time': datetime.datetime.utcnow(),
#         'thumbnail': 'https://cdn.vuetifyjs.com/images/cards/docks.jpg',
#         'type': 'text',
#         'title': 'How to win a hackathon challenge?',
#         'content': 'Template content',
#         'level': 'medium'
#     },
#     {
#         'id': generate_filename(),
#         'topic': 'study',
#         'created_time': datetime.datetime.utcnow(),
#         'thumbnail': 'https://cdn.vuetifyjs.com/images/cards/docks.jpg',
#         'type': 'audio',
#         'title': 'How to spend money after winning a hackathon challenge?',
#         'content': 'Template content',
#         'level': 'hard'
#     }
# ]

questions = [
    {
        'id': generate_filename(),
        'article_id': '2',
        'options': [
            'Bui Manh Thang',
            'Luong Tuan Dung',
            'Bui Duy Tuan',
            'Phan Ngoc Lan'
        ],
        'answer': 'Bui Manh Thang',
        'type': 'choice',
        'audio': 'http://localhost:5000/audios/audio.mp3'
    },
    {
        'id': generate_filename(),
        'article_id': '1',
        'options': [
            'Bui Manh Thang',
            'Luong Tuan Dung',
            'Bui Duy Tuan',
            'Phan Ngoc Lan'
        ],
        'answer': 'Bui Manh Thang',
        'type': 'fill',
        'audio': 'http://localhost:5000/audios/audio.mp3'
    },
    {
        'id': generate_filename(),
        'article_id': '2',
        'options': [
            'Bui Manh Thang',
            'Luong Tuan Dung',
            'Bui Duy Tuan',
            'Phan Ngoc Lan'
        ],
        'answer': 'Bui Manh Thang',
        'type': 'choice',
        'audio': 'http://localhost:5000/audios/audio.mp3'
    },
    {
        'id': generate_filename(),
        'article_id': '1',
        'options': [
            'Bui Manh Thang',
            'Luong Tuan Dung',
            'Bui Duy Tuan',
            'Phan Ngoc Lan'
        ],
        'answer': 'Bui Manh Thang',
        'type': 'choice',
        'audio': 'http://localhost:5000/audios/audio.mp3'
    }
]


client = MongoClient('localhost', 27017)
db = client['agc2019']


ids = []
for art in articles:
    ids.append(art['id'])
    db.articles.insert_one(art)

for que in questions:
    que['article_id'] = ids[np.random.randint(len(ids))]
    db.questions.insert_one(que)
