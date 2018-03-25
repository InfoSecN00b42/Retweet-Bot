class RetweetObject:
    def __init__(self, tweet):
        self.id = tweet.id
        self.authorId = tweet.user.id
        self.tweet = tweet

    def hasUserId(self, userId):
        return self.authorId == userId

    def hasTweetId(self, tweetId):
        return self.id == tweetId

    def getTweetId(self):
        return self.id

    def getTweet(self):
        return self.tweet
