import os
from time import sleep
import twitter as tw
from tweetmaker import make_url_tweet
import fdj2today_parser as fdj2

EXEC_SPAN = os.environ('EXEC_SPAN')
API_ENV_KEY = ['TOKEN', 'TOKEN_SECRET', 'CONSUMER_KEY', 'CONSUMER_SECRET']


def lambda_handler(event, context):
    client = TwitterClient()
    client.run()


class TwitterClient(object):
    def __init__(self):
        tw_conf = {k.lower(): os.environ[k] for k in API_ENV_KEY}
        oauth = tw.OAuth(**tw_conf)
        self.client = tw.Twitter(auth=oauth)

    def run(self):
        articles = fdj2.request_fudosan_articles(exec_span=EXEC_SPAN)
        for i, a in enumerate(articles):
            sleep(10)
            self.tweet_article(a)

    def tweet_article(self, article):
        url = article['urls'][0]
        message = make_url_tweet(text=article['title'], url=url)
        self.client.statuses.update(status=message)
