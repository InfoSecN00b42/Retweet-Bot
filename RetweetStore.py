import pickle
from RetweetObject import RetweetObject


class RetweetStore:
    __fileName = ""
    __tweetStore = {}

    # initializes the TweetStore
    def __init__(self, fileName):
        self.__fileName = fileName
        opened = False
        try:
            fileHandle = open(fileName, mode='rb')
            opened = True
            self.__tweetStore = pickle.load(fileHandle)

        except FileNotFoundError:
            print("No store present")

        except TypeError:
            print("File stored incompatible information")

        finally:
            if opened:
                fileHandle.close()

    # Saves the Store to disk
    def saveStoreToDisk(self):
        opened = False
        try:
            fileHandle = open(self.__fileName, mode='wb')
            opened = True
            pickle.dump(self.__tweetStore, fileHandle)
        finally:
            if opened:
                fileHandle.close()

    # fetches a RetweetObject from the Store
    def getRetweetObject(self, tweetId):
        return self.__tweetStore[tweetId]

    # Returns all stored RetweetObjects
    def getAllRetweets(self):
        return self.__tweetStore.values()

    # Checks if tweet has already been stored
    def hasBeenStored(self, tweetId):
        return tweetId in self.__tweetStore

    # Adds a retweet to the store
    def addRetweet(self, tweetId, retweet):
        self.__tweetStore[tweetId] = retweet

    # Synchronizes with external dictionary
    def synchronize(self, externalTweetStore):
        self.__tweetStore.update(externalTweetStore)
