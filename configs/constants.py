# Rest API config
HOST = '0.0.0.0'
PORT = 5000

# MongoDB config
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'agc2019'
MONGO_URI = 'mongodb://%s:%d/%s' % (MONGO_HOST, MONGO_PORT, MONGO_DB)

# Public/static folder
STATIC_FOLDER = 'static'
PUBLIC_FOLDER = STATIC_FOLDER

# Others
TOPICS  = ['economy', 'society', 'sports', 'recommended', 'politics']
LEVELS = ['easy', 'medium', 'hard']
PUBLISHERS = ['wsj', 'bbc', 'kenh14']
TYPES = ['text', 'audio']