"""
This is a suite of tests that can incur API rate limiting, segregated due to the potentially unwanted affects that can
have.
"""
import os
import sys

# Append parent directory to enhance portability.
sys.path.append((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
