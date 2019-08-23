import sys
import time
sys.path.append('recommendation')
from question_recommender import QuestionRecommender
from article_recommender import ArticleRecommender
from configs import constants
import schedule


def refresh_question_recommender():
    recommender = QuestionRecommender(constants.MONGO_URI, constants.MONGO_DB)
    recommender.refresh()


def refresh_article_recommender():
	recommender = ArticleRecommender(mongo_uri=constants.MONGO_URI, mongo_db=constants.MONGO_DB)
	recommender.fit()


def schedule_job():
	schedule.every(1).day.at("02:30").do(refresh_article_recommender)
	schedule.every(1).day.at("03:30").do(refresh_question_recommender)

	while True:
		schedule.run_pending()
		time.sleep(1)


if __name__ == '__main__':
	import sys
	if len(sys.argv) > 1 and sys.argv[1] == 'schedule':
		print("Recommenders started!")
		schedule_job()
	else:
		print("Refreshing recommenders manually")
		refresh_question_recommender()
		refresh_article_recommender()
