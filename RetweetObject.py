class RetweetObject:
    def __init__(self, tweet):
        # We are NOT a plain retweet bot anymore and will not get a retweeted status from our quoted tweets.
        ##if(not hasattr(tweet, "retweeted_status")):
        ##    raise ValueError("Tweet needs to contain a retweeted status")
        ##self.id = tweet.retweeted_status.id
        ##self.authorId = tweet.retweeted_status.user.id
        self.id = tweet.id
        self.authorId = tweet.user.id
        self.tweet = tweet

    def hasUserId(self, userId):
        return self.authorId == userId

    def getUserId(self):
        return self.authorId

    def hasTweetId(self, tweetId):
        return self.id == tweetId

    def getTweetId(self):
        return self.id

    def getTweet(self):
        return self.tweet
