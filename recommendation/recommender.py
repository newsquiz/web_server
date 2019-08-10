import pymongo
import numpy as np
from configs import constants
import random
import pickle
import os


class QuestionRecommender:
    def __init__(self, mongo_uri=None, mongo_db=None, max_count=50000, user_count_limit=100):
        if mongo_uri is not None:
            client = pymongo.MongoClient(mongo_uri)
            self.db = client[mongo_db]
        self.max_count = max_count
        self.user_count_limit = user_count_limit


    def get_all_tags(self):
        return ['listening-comprehension', 'paraphrase', 'reading-comprehension', \
                'nummod', 'yes', 'grammar', 'phrasal_verb', 'LOCATION', 'TIME', \
                'subj', 'dobj', 'nmod', 'no', 'phonetic', 'PERSON', 'ccomp/xcomp', \
                'DATE', 'tense', 'NUMBER', 'homophone', 'ORGANIZATION', 'vocab']


    def get_all_levels(self):
        return ['Easy', 'Medium', 'Hard']


    def get_all_users(self):
        users = self.db.users.find({}, {'id': 1})
        return [x['id'] for x in users]


    def load_data(self):
        all_users = self.get_all_users()

        # Get all items
        all_tags = self.get_all_tags()
        all_levels = self.get_all_levels()
        all_items = [lvl + '_' + tag for lvl in all_levels for tag in all_tags]
        self.n_users = len(all_users)
        self.n_items = len(all_items)

        # Count wrong answers each items
        raw_user_answers = self.db.user_answers.find({}, {
                                'q_tags': 1, 
                                'level': 1, 
                                'u_id': 1,
                                'is_correct': 1
                            }) \
                            .sort([('submited_time', pymongo.DESCENDING)]) \
                            .limit(self.max_count)
        self.USER2IDX = {x: i for i, x in enumerate(all_users)}
        self.IDX2USER = {i: x for i, x in enumerate(all_users)}
        self.ITEM2IDX = {x: i for i, x in enumerate(all_items)}
        self.IDX2ITEM = {i: x for i, x in enumerate(all_items)}
        wrong_counts = {}
        user_counts = {}
        for u_a in raw_user_answers:
            lvl = u_a['level']
            u_id = u_a['u_id']
            if u_id not in user_counts:
                user_counts[u_id] = 0
            else:
                if user_counts[u_id] > self.user_count_limit:
                    continue
            user_counts[u_id] += 1
            for tag in u_a['q_tags']:
                item = lvl + '_' + tag
                if not u_a['is_correct']:
                    key = (self.USER2IDX[u_id], self.ITEM2IDX[item])
                    if key not in wrong_counts:
                        wrong_counts[key] = 0
                    wrong_counts[key] += 1.0
        list_wrong_counts = [[u_idx, item_idx, count] \
                            for (u_idx, item_idx), count in zip(wrong_counts.keys(), wrong_counts.values())]
        return np.array(list_wrong_counts)


    def refresh(self):
        data = self.load_data()
        item_weights = {}
        for u_idx in range(self.n_users):
            item_weights[u_idx] = [0 for _ in range(self.n_items)]
        for u_idx, item_idx, count in data:
            item_weights[int(u_idx)][int(item_idx)] = count
        for key in item_weights:
            value = item_weights[key]
            w_sum = sum(value)
            value = [x / w_sum for x in value]
            item_weights[key] = value
        decoded_item_weights = {self.IDX2USER[u_idx]: [(self.IDX2ITEM[item_idx], weight) \
                                for item_idx, weight in enumerate(item_weights[u_idx])] \
                                for u_idx in item_weights }
        pickle.dump(decoded_item_weights, open(constants.Q_RECOMMENDER_MODEL, 'wb'))


    def recommend(self, questions, user_id=None, max_count=5, new_ratio=0.4):
        if not os.path.exists(constants.Q_RECOMMENDER_MODEL):
            data = {}
        else:
            data = pickle.load(open(constants.Q_RECOMMENDER_MODEL, 'rb'))
        if user_id not in data or len(questions) < max_count:
            random.shuffle(questions)
            return sorted(questions[:max_count], key=lambda x: x['sent_id'])
        
        # If user has recommending data
        weights = data[user_id]
        weights = {key: value for key, value in weights}
        question_scores = []
        for ques in questions:
            lvl = ques['level']
            score = 0
            for tag in ques['tags']:
                item = lvl + '_' + tag
                score += weights[item]
            question_scores.append(score)
        question_scores = np.array(question_scores)
        question_scores /= np.sum(question_scores)

        recommended = []
        suggest_count= int((1 - 0.4) * max_count)
        rcm_sent_ids, rcm_answers = [], []
        i = 0
        while i < 1000 and len(recommended) < suggest_count:
            i += 1
            chosen = np.random.choice(questions, 1, p=question_scores)[0]
            if chosen['answer'] not in rcm_answers and chosen['sent_id'] not in rcm_sent_ids:
                recommended.append(chosen)
                rcm_answers.append(chosen['answer'])
                rcm_sent_ids.append(chosen['sent_id'])
        remaining = [x for x in questions if x not in recommended]
        recommended.extend(np.random.choice(remaining, max_count - len(recommended)))
        return sorted(recommended, key=lambda x: x['sent_id'])
        


def get_article_questions(article_id):
    from api_server import mongo
    article = mongo.db.articles.find_one({'id': article_id})
    if article is None:
        return []
    questions = mongo.db.questions.find({'article_id': article_id})
    return list(questions)


def main():
    recommender = QuestionRecommender(constants.MONGO_URI, constants.MONGO_DB)
    r_q = recommender.recommend(get_article_questions('a89333c77e645461b1a8f1bcd8fea1d0'), '02318')
    print(r_q)


if __name__ == '__main__':
    main()
    