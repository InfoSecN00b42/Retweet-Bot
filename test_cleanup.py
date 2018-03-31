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

# Authenticating
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Initializing
retweetGuard = RetweetGuard(api.blocks_ids())
retweetStore = RetweetStore('tweetStore.obj')

print("Using the Account: " + api.me().name)
print("This account blocks " + str(len(retweetGuard._blocked_ids)) + " Accounts")
sleep(4)

# Clean up possible new blocks
retweetGuard.clean_up_retweets(retweetStore, api)

# Save updated store to disk
retweetStore.saveStoreToDisk()
