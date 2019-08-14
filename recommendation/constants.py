# MongoDB config
MONGO_HOST = '172.104.185.102'
MONGO_PORT = 8600
MONGO_DB = 'newsquiz'
MONGO_USER = 'newsquiz'
MONGO_PASS = 'grdVGACnq$2019'
MONGO_URI = 'mongodb://%s:%s@%s:%d/%s?authSource=admin' % (MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_PORT, MONGO_DB)

# Models
A_RECOMMENDER_MODEL = 'models/'