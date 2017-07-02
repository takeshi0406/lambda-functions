import os
import time
from datetime import datetime
import twitter


API_ENV_KEY = ['CONSUMER_KEY', 'CONSUMER_SECRET', 'ACCESS_TOKEN_KEY', 'ACCESS_TOKEN_SECRET']
COUNT = 100


def lambda_handler(event, context):
    target_terms = os.environ['RETWEET_TERMS'].split(',')
    client = TwitterClient()
    client.run(target_terms)
    return True


class TwitterClient(object):
    def __init__(self):
        self.client = twitter.Api(*[os.environ[k] for k in API_ENV_KEY])
        self.nowtime = int(time.mktime(datetime.now().timetuple()))
        self.begin_time = self.nowtime - 60 * 60

    def run(self, terms):
        for term in terms:
            for tweet in self._search_tweet(term):
                if tweet.created_at_in_seconds in range(self.begin_time, self.nowtime):
                    self._post_retweet(tweet.id)

    def _search_tweet(self, term):
        return self.client.GetSearch(term=term, count=COUNT, result_type='recent')

    def _post_retweet(self, tweet_id):
        try:
            self.client.PostRetweet(tweet_id)
        except:
            print(f'{tweet_id}は既にリツイートされています')
