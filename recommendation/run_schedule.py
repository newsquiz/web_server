import sys
sys.path.append('recommendation')
from question_recommender import QuestionRecommender
from configs import constants
import schedule


def refresh():
    recommender = QuestionRecommender(constants.MONGO_URI, constants.MONGO_DB)
    recommender.refresh()


def schedule_job():
    schedule.every(3).day.at("02:30").do(refresh)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    schedule_job()
