# Retweet bot for Twitter, using Python and Tweepy.
# License: MIT License.

import tweepy
import dateparser
import pickle
from RetweetObject import RetweetObject
from RetweetStore import RetweetStore
from time import sleep

# Import in your Twitter application keys, tokens, and secrets.
# Make sure your settings.py file lives in the same directory as this .py file.
from settings import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

retweetStore = RetweetStore('tweetStore.obj')

# Make sure you read Twitter's rules on automation - don't spam!
fetchedTweets = []
for tweet in tweepy.Cursor(api.search, q=hashtag).items(maximum_tweets_per_call):
    fetchedTweets.append(tweet)

for tweet in reversed(fetchedTweets):
    try:
        # print('\nRetweet Bot found tweet by @' + tweet.user.screen_name + '. ' + 'Attempting to retweet.')
        if(not retweetStore.hasBeenStored(tweet.id)):
            tweet.retweet()
            retweetStore.addRetweet(tweet.id, RetweetObject(tweet))
            # Where sleep(10), sleep is measured in seconds.
            # Change 10 to amount of seconds you want to have in-between retweets.
            # Read Twitter's rules on automation. Don't spam!
            sleep(5)
            print('Retweet published successfully.')

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
