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
from settings import consumer_key
from settings import consumer_secret
from settings import access_token
from settings import access_token_secret
from settings import hashtag
from settings import maximum_tweets_per_call
from settings import testing

# Authenticating
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Initializing
retweetStore = RetweetStore('tweetStore.obj')

print("Using the Account: " + api.me().name)

number_of_tweets = api.me().statuses_count
number_per_page = 10
number_of_pages = 1+int((number_of_tweets-(number_of_tweets %
                                           number_per_page))/number_per_page)

print("Syncing: " + str(number_of_tweets) + " tweets")
print("Fetching " + str(number_of_pages) + " pages with " +
      str(number_per_page) + " tweets per page")

listOfOwnTweets = []
for i in range(1, number_of_pages+1):
    listOfOwnTweets.extend(api.user_timeline(count=number_per_page, page=i))

print("Collected : " + str(len(listOfOwnTweets)) + " tweets from timeline")

for tweet in listOfOwnTweets:
    if hasattr(tweet, "retweeted_status") and not retweetStore.hasBeenStored(tweet.retweeted_status.id):
        retweet = RetweetObject(tweet)
        retweetStore.addRetweet(retweet.getTweetId(), retweet)
        print(".", end="")
    else:
        print("!", end="")
print("DONE")
retweetStore.saveStoreToDisk()
