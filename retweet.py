# Retweet bot for Twitter, using Python and Tweepy.
# License: MIT License.

import tweepy
import dateparser
import pickle
from RetweetObject import RetweetObject
from RetweetStore import RetweetStore
from RetweetGuard import RetweetGuard
from time import sleep

# Import in your Twitter application keys, tokens, and secrets.
# Make sure your settings.py file lives in the same directory as this .py file.
from settings import consumer_key
from settings import consumer_secret
from settings import access_token
from settings import access_token_secret
from settings import hashtag
from settings import maximum_tweets_per_call
from settings import testing

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

retweetGuard = RetweetGuard(api.blocks_ids())
retweetStore = RetweetStore('tweetStore.obj')

# Where q='#example', change #example to whatever hashtag or keyword you want to search.
# Where items(5), change 5 to the amount of retweets you want to tweet.
# Make sure you read Twitter's rules on automation - don't spam!
fetchedTweets = []

for tweet in tweepy.Cursor(api.search, q=hashtag).items(maximum_tweets_per_call):
    if(retweetGuard.preliminary_tweet_test(tweet)):
        #print("Tweet was approved.")
        fetchedTweets.append(tweet)

for tweet in reversed(fetchedTweets):
    try:
        if (not retweetStore.hasBeenStored(tweet.id)):
            if(not testing):
                tweet.retweet()
                retweetStore.addRetweet(tweet.id, RetweetObject(tweet))
                sleep(5)
            else:
                print(tweet.text)

    # Some basic error handling. Will print out why retweet failed, into your terminal.
    except tweepy.TweepError as error:
        if(error.api_code == 327):
            print('Already retweeted, but not yet in store')
            retweetStore.addRetweet(tweet.id, RetweetObject(tweet))
        else:
            print('\nError. Retweet not successful. Reason: ')
            print(error.reason)
    except StopIteration:
        break

retweetStore.saveStoreToDisk()
