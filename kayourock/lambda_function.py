import os
import time
from datetime import datetime
from functools import partial

import twitter
from bs4 import BeautifulSoup


API_ENV_KEY = ['CONSUMER_KEY', 'CONSUMER_SECRET', 'ACCESS_TOKEN_KEY', 'ACCESS_TOKEN_SECRET']
CONFIGS = ['stopwords', 'stopaccounts', 'stopclients']
COUNT = 100


def lambda_handler(event, context):
    target_terms = _read_config('retweet_terms')
    is_target = partial(_is_target, *[_read_config(x) for x in CONFIGS])
    client = TwitterClient()
    client.run(target_terms, is_target)
    return True


def _read_config(target):
    with open(f'./config/{target}.txt') as f:
        texts = f.read()
    return [x.strip() for x in texts.split('\n')]


def _is_target(stopwords, stopaccounts, stopclients, tweet):
    if 'bot' in tweet.user.sceen_name:
        return False
    elif any(wrd in tweet.text for wrd in stopwords):
        return False
    elif tweet.user.screen_name in stopaccounts:
        return False
    elif len(tweet.urls) <= 0:
        return False
    elif _parse_client_name(tweet) in stopclients:
        return False
    return True


def _parse_client_name(tweet):
    soup = BeautifulSoup(tweet, 'lxml')
    return soup.text


class TwitterClient(object):
    def __init__(self):
        self.client = twitter.Api(*[os.environ[k] for k in API_ENV_KEY])
        self.nowtime = int(time.mktime(datetime.now().timetuple()))
        self.begin_time = self.nowtime - 60 * 60

    def run(self, terms, is_target):
        for term in terms:
            for tweet in self._search_tweet(term):
                if tweet.created_at_in_seconds in range(self.begin_time, self.nowtime):
                    if is_target(tweet):
                        self._post_retweet(tweet.id)

    def _search_tweet(self, term):
        # return self.client.GetSearch(term=term, count=COUNT, result_type='recent')
        a = self.client.GetSearch(term=term, count=COUNT, result_type='recent')
        print(a)
        return a

    def _post_retweet(self, tweet_id):
        try:
            self.client.PostRetweet(tweet_id)
        except:
            print(f'{tweet_id}は既にリツイートされています')


if __name__ == '__main__':
    lambda_handler(None, None)