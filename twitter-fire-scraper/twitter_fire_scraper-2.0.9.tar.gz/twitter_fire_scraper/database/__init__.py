"""
A set of classes that allows access to a MongoDB database to save, update, and retrieve TweetResult objects.
"""
import os
import sys

# Append parent directory to enhance portability.
sys.path.append((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
