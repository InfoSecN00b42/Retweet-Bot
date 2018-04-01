
def printTweet(tweet):
    if not hasattr(tweet, "retweeted_status") and not hasattr(tweet, "twitter_quoted_status"):
        # Original
        print("Tweet is directly from author " +
              tweet.user.name + " @" + tweet.user.screen_name)

    elif not hasattr(tweet, "retweeted_status") and hasattr(tweet, "twitter_quoted_status"):
        # Quote
        print("Tweet is a quote by " + tweet.user.name + " @" + tweet.user.screen_name + " from author " +
              tweet.twitter_quoted_status.user.name + " @" + tweet.twitter_quoted_status.user.screen_name)
    # Check if Retweet
    elif hasattr(tweet, "retweeted_status") and not hasattr(tweet, "twitter_quoted_status"):
        # Retweet
        print("Tweet is a retweet by " + tweet.user.name + " @" + tweet.user.screen_name + " from author " +
              tweet.retweeted_status.user.name + " @" + tweet.retweeted_status.user.screen_name)
    else:
        raise ValueError("unexpected tweet object")
