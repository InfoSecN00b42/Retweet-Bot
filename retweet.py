# Retweet bot for Twitter, using Python and Tweepy.
# License: MIT License.

import tweepy
import dateparser
import pickle
from RetweetObject import RetweetObject
from RetweetStore import RetweetStore
from RetweetGuard import RetweetGuard
from time import sleep
from helper_functions import printTweet

from patterns import substitutions

import re
import sys

# Import in your Twitter application keys, tokens, and secrets.
# Make sure your settings.py file lives in the same directory as this .py file.
from settings import consumer_key
from settings import consumer_secret
from settings import access_token
from settings import access_token_secret
from settings import hashtag
from settings import maximum_tweets_per_call
from settings import testing
from settings import seconds_between_retweets

testing = False

# Authenticating
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Initializing
retweetGuard = RetweetGuard(api.blocks_ids())
retweetStore = RetweetStore('tweetStore.obj')


if testing:
    print("Using the Account: " + api.me().name)
    print("This account blocks " +
          str(len(retweetGuard._blocked_ids)) + " Accounts")
    sleep(4)

# Clean up possible new blocks
retweetGuard.clean_up_retweets(retweetStore, api)

# Search Tweets and Retweet
fetchedTweets = []
# Make sure you read Twitter's rules on automation - don't spam!
for tweet in tweepy.Cursor(api.search, q=hashtag).items(maximum_tweets_per_call):
    # Collect a list of approved tweets
    if not hasattr(tweet, "retweeted_status") and not hasattr(tweet, "twitter_quoted_status") and not testing:
        # Original
        if(retweetGuard.preliminary_tweet_test(tweet)):
            fetchedTweets.append(tweet)
    elif not hasattr(tweet, "retweeted_status") and hasattr(tweet, "twitter_quoted_status") and not testing:
        # Quote
        if(retweetGuard.preliminary_tweet_test(tweet)):
            fetchedTweets.append(tweet)
    # Check if Retweet
    elif hasattr(tweet, "retweeted_status") and not hasattr(tweet, "twitter_quoted_status") and not testing:
        # Retweet
        if(retweetGuard.preliminary_tweet_test(tweet.retweeted_status)):
            fetchedTweets.append(tweet.retweeted_status)
    elif testing:
        print("Testing mode on")
    else:
        raise ValueError("unexpected tweet object")

# Retweet them in reverse order so older tweets are retweeted first
print("Fetched tweets: " + str(len(fetchedTweets)))
for tweet in reversed(fetchedTweets):
    try:
        textToQuote=tweet.text
        if not retweetStore.hasBeenStored(tweet.id) and not testing:
            URL_to_RT='https://twitter.com/'+ str(tweet.user.screen_name) + '/status/' + str(tweet.id)
            # Do the substitions, edit patterns.py
            for pattern in substitutions:
                textToQuote=re.sub(pattern.split(':')[0], pattern.split(':')[1], textToQuote)
            if tweet.text == textToQuote:
                print("There was nothing changed to the RT")
                print(textToQuote+" - "+URL_to_RT)
                continue
            retweet = api.update_status(textToQuote, URL_to_RT)
            ##retweet = api.update_status(infoReplace.sub('#InfoSex', tweet.getTweet().retweeted_status.text))
            ##retweet = tweet.retweet()
            ##print(retweet._json)
            retweetStore.addRetweet(tweet.id, RetweetObject(retweet))
            print("Sleeping: "+ str(seconds_between_retweets) + "s")
            sleep(seconds_between_retweets)

    # Some basic error handling. Will print out why retweet failed, into your terminal.
    except tweepy.TweepError as error:
        if(error.api_code == 327):
            print('Already retweeted,not in store, please synchronize tweetstore')
        elif(error.api_code == 326):
            print('This account is temporarily locked. Please log in to https://twitter.com to unlock your account.')
            sleep(60)
        else:
            print('\nError. Retweet not successful. Reason: ')
            print(error.reason)
    except StopIteration:
        break

retweetStore.saveStoreToDisk()
