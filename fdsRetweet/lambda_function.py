import os
import twitter as tw
import tweetnewsfinder as tf
from datetime import datetime, timedelta


API_ENV_KEY = ['TOKEN', 'TOKEN_SECRET', 'CONSUMER_KEY', 'CONSUMER_SECRET']


def lambda_handler(event, context):
    target_terms = set(os.environ['RETWEET_TERMS'].split(','))
    client = TwitterClient()
    client.set_seed_lists(os.environ['USER_LISTS'].split(','))
    client.set_checked_accounts(os.environ['CHECKED_ACCOUNTS'].split(','))
    client.run(target_terms)
    return True


class TwitterClient(object):
    def __init__(self):
        tf_conf = {k.lower(): os.environ[k] for k in API_ENV_KEY}
        oauth = tw.OAuth(**tf_conf)
        self.target_time = int((datetime.now() + timedelta(hours=-24)).strftime('%s'))
        self.finder = tf.TweetNewsFinder(auth=oauth)
        self.client = tw.Twitter(auth=oauth)

    def set_seed_lists(self, userlists):
        for l in userlists:
            self.finder.set_seed_list(*l.split('/'))

    def set_checked_accounts(self, accounts):
        self.finder.checked_accounts = set(accounts)

    def run(self, target_terms):
        tweets = self.finder.get_news_tweets(
                    target_terms, self.target_time, threshold=2, trials=1, bulk=10)
        for t in tweets:
            try:
                self.client.statuses.retweet(id=t['id'])
            except Exception as e:
                print(f"{t['id']}は既にリツイートされています")
