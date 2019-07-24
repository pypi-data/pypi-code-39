import unittest

from pymongo import MongoClient

from config import Config
from database.TweetResult import TweetResult, ERelevancy
from database.TweetResultDAO import TweetResultDAO
from tests.test.incur_api_hits.cached_tweets import CachedTweets


class TestDaoSimple(unittest.TestCase):

    def setUp(self) -> None:
        # connect to localhost
        self.client = MongoClient(Config.Defaults.MONGODB_CONNECTION_STRING)

        # make a DAO with our connection
        self.dao = TweetResultDAO(self.client, collection_name=self.__class__.__name__)

    def tearDown(self) -> None:
        self.client.close()

    def testRealData(self):
        """Tests that the DAO can successfully insert and delete a few real records."""
        self.assertTrue(True)  # TODO

        # small amount of tweets
        tweetResultDict = CachedTweets.tweets_small()


        # save all of them
        for term, tweetResults in tweetResultDict.items():

            for tweetResult in tweetResults:

                # Make sure it doesn't already exist if we're running this SUPER fast or twice.
                if self.dao.get_by_id(tweetResult.get_id()) is not None:
                    self.dao.delete_by_id(tweetResult.get_id())

                self.dao.save_one(tweetResult)

        # using our local copy, retrieve them and compare them
        for term, tweetResults in tweetResultDict.items():

            for tweetResult in tweetResults:

                database_tweetResult = self.dao.get_by_id(tweetResult.get_id())

                # for brevity, compare their serialized forms.
                self.assertEqual(tweetResult.serialize(), database_tweetResult.serialize())

    def testMockData(self):
        """Tests that the DAO can successfully insert and delete a single mock record."""

        # delete if it somehow exists
        if self.dao.get_by_id('test_id') is not None:
            self.dao.delete_by_id('test_id')

        # mock tweetresult
        tweetResult = TweetResult(
            data={"id": "test_id",
                  "full_text": "hello!"},
            tags=["test", "deleteme"],
            relevancy=ERelevancy.IRRELEVANT)

        # save a tweetresult
        self.dao.save_one(tweetResult)

        # delete our local copy!
        del tweetResult

        # deserialize it from db
        database_result = self.dao.get_by_id("test_id")

        # It should exist
        self.assertNotEqual(database_result, None)

        # it should be of type TweetResult
        self.assertIsInstance(database_result, TweetResult)

        # it should have its tags,
        self.assertIn("test", database_result.tags)
        self.assertIn("deleteme", database_result.tags)

        # it should have its ERelevancy
        self.assertEqual(ERelevancy.IRRELEVANT, database_result.relevancy)

        # delete it now
        self.dao.delete_by_id(database_result.get_id())

        # it should be None since it's gone
        self.assertEqual(self.dao.get_by_id("test_id"), None)
