import sys
from enum import Enum

sys.path.append("..")

from tweepy import Status
from typing import Dict, List, Union

from util import status_from_dict


class ERelevancy(Enum):
    """An enumeration that represents if something is uncategorized, relevant, or irrelevant."""
    UNCATEGORIZED = "UNCATEGORIZED"
    RELEVANT = "RELEVANT"
    IRRELEVANT = "IRRELEVANT"


class TweetResult(object):
    """An object representing a single Tweet along with metadata such as tags and relevancy."""

    def __init__(self,
                 data: Union[Status, dict],
                 tags: List[str],
                 relevancy: ERelevancy):

        # Convert a dict to a Status automatically
        if isinstance(data, dict):
            data = status_from_dict(data)

        if not isinstance(data, Status):
            raise ValueError("You must pass a Status object to the TweetResult constructor!")

        self.data = data
        self.tags = tags
        self.relevancy = relevancy

    def get_json(self) -> dict:
        """The JSON value that the Twitter API returns for this tweet."""
        return self.data._json

    def get_id(self):
        """The ID of a Tweet. This is unique."""
        return self.data.id

    def get_text(self):
        """The content of a tweet.

        Returns either "full_text" or "text", favoring the former as it is longer."""

        if hasattr(self.data, "full_text"):
            return self.data.full_text

        elif hasattr(self.data, 'text'):
            return self.data.text

        else:
            raise KeyError("Tweet has no text!")

    def serialize(self):
        """Serialize this TweetResult object to a JSON-like object that can be saved to a MongoDB database"""

        if type(self.tags) is set:
            self.tags = list(self.tags)

        return {
            # Base attributes, these are needed to fully reconstruct the object.
            'data': self.get_json(),
            'tags': self.tags,
            'relevancy': self.relevancy.value,

            # Derived attributes, these are inferred or created from the base attributes.
            '_id': self.get_id(),
        }

    @classmethod
    def deserialize(cls, dict: Dict):
        """Deserialize a JSON-like object to a TweetResult. Like the opposite of serializing."""

        status = status_from_dict(dict['data'])

        return TweetResult(data=status,
                           tags=dict['tags'],
                           relevancy=ERelevancy(dict['relevancy']))
