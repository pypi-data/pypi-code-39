from typing import Union

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from database.TweetResult import TweetResult


class TweetResultDAO(object):
    """
    A DAO that lets you save, modify, and retrieve TweetResults from the database.
    """

    def __init__(self, mongoclient: MongoClient, database_name='tweets', collection_name='all_tweets'):
        self.client: MongoClient = mongoclient

        self.database_name = database_name
        self.db: Database = self.client[self.database_name]

        self.collection_name = collection_name
        self.collection: Collection = self.db[self.collection_name]

    def save_one(self, tweetresult: TweetResult):
        """Save a single TweetResult object."""
        self.collection.insert_one(tweetresult.serialize())

    def get_by_id(self, id) -> Union[TweetResult, None]:
        """Return a tweet by ID.

        Returns None if no tweet is found."""
        cursor = self.collection.find({"_id": id})

        if cursor.count() == 0:
            return None

        result = cursor.next()

        cursor.close()

        return TweetResult.deserialize(result)

    def delete_by_id(self, id):
        self.collection.delete_one({"_id": id})
