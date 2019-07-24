import unittest

from scraper import Scraper
from twitter import TwitterAuthentication


class TestSimpleScraping(unittest.TestCase):

    def testCanScrapeTerm(self):
        """Tests that scraper can scrape one term."""

        twauth = TwitterAuthentication.autodetect_twitter_auth()

        scraper = Scraper(twitter_authentication=twauth)

        results = scraper.scrape_terms({"fire"}, count=1)

        self.assertIn('fire', results)

        self.assertIsInstance(results['fire'], list)

        self.assertEqual(len(results.keys()), 1)

        self.assertIsInstance(results['fire'][0].get_text(), str)

    def testCanScrapeAccount(self):
        """Tests that scraper can scrape one account."""
        twauth = TwitterAuthentication.autodetect_twitter_auth()

        scraper = Scraper(twitter_authentication=twauth)

        results = scraper.scrape_accounts({"@RedCross"}, count=1)

        self.assertIn('@RedCross', results)

        self.assertEqual(len(results.keys()), 1)

        self.assertIsInstance(results['@RedCross'], list)

        self.assertIsInstance(results['@RedCross'][0].get_text(), str)

    def testCanScrapeMethod(self):
        """Tests that the Scraper's `scrape` method works."""

        twauth = TwitterAuthentication.autodetect_twitter_auth()

        scraper = Scraper(twitter_authentication=twauth)

        results = scraper.scrape(terms={"fire"}, accounts={"@RedCross"})

        self.assertIn('fire', results.keys())
        self.assertIn('@RedCross', results.keys())

        self.assertEqual(len(results.keys()), 2)

        self.assertIsInstance(results['fire'], list)
        self.assertIsInstance(results['@RedCross'], list)

    def _disabled_testLotsOfTweets(self):
        """Tests if the Scraper can retrieve 1000 tweets for one term"""
        twauth = TwitterAuthentication.autodetect_twitter_auth()

        scraper = Scraper(twitter_authentication=twauth)

        results = scraper.scrape(terms={"fire"}, count=1000)

        self.assertIn('fire', results.keys())

        self.assertEqual(len(results.keys()), 1)

        self.assertIsInstance(results['fire'], list)

        self.assertEqual(len(results['fire']), 1000)
