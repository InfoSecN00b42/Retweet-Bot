import datetime
from settings import minimum_account_age
from settings import minimum_account_follower
from time import sleep

# The below is a bug from __init__ see commented line
# [22404415, 13862172]
#<class 'list'>
#Traceback (most recent call last):
#  File "retweet.py", line 31, in <module>
#    retweetGuard = RetweetGuard(api.blocks_ids())
#  File "/home/steve/mCode/Retweet-Bot/RetweetGuard.py", line 11, in __init__
#    self._blocked_ids = blocked_ids['ids']
#TypeError: list indices must be integers or slices, not str


class RetweetGuard:
    _blocked_ids = []

    def __init__(self, blocked_ids):
        #self._blocked_ids = blocked_ids['ids']
        self._blocked_ids = blocked_ids

    def preliminary_tweet_test(self, tweet):
        # check if user blocked
        if tweet.user.id in self._blocked_ids:
            return False

        # check user for age (bar all younger than <M days)
        account_age = datetime.datetime.now() - tweet.user.created_at
        if account_age.days < minimum_account_age:
            # print("User too young")
            return False

        # check user for follower count (bar everyone with less than N followers)
        if tweet.user.followers_count < minimum_account_follower:
            # print("User too little followers")
            return False

        # okay passed preliminary checks
        return True

    def clean_up_retweets(self, tweetStore, api):
        ids = []
        for retweet in tweetStore.getAllRetweets():
            if retweet.getUserId() in self._blocked_ids:
                # Remove a retweet from timeline and store
                print("Trying to unretweet from " + retweet.getTweet().retweeted_status.user.name)
                api.unretweet(retweet.getTweetId())
                ids.append(retweet.getTweetId())
                sleep(0.5)
        for id in ids:
            tweetStore.removeRetweet(id)
