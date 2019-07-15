from unittest import TestCase

from storage import StorageRepository
from team_domain import TeamDomain

class TestTeamDomain(TestCase):
    def setUp(self):
        with open('data/P1.csv', 'r') as file:
            self.files = [file.readlines()]
        self.storage = StorageRepository(self.files)
        self.storage.build()
        self.team_domain = TeamDomain()

    def test_get_all_teams(self):
        all_teams = self.team_domain.get_all_teams()
        self.assertIsInstance(all_teams, list)
        self.assertTrue(len(all_teams) == 18)

    def test_get_all_matches_by_team_name(self):
        matches = self.team_domain.get_all_matches_by_team_name('BENFICA')
        self.assertIsInstance(matches, list)
        self.assertTrue(len(matches) == 34)

    def test_get_all_home_matches_by_team_name(self):
        matches = self.team_domain.get_all_home_matches_by_team_name('BENFICA')
        self.assertIsInstance(matches, list)
        self.assertTrue(len(matches) == 17)

    def test_get_all_away_matches_by_team_name(self):
        matches = self.team_domain.get_all_away_matches_by_team_name('BENFICA')
        self.assertIsInstance(matches, list)
        self.assertTrue(len(matches) == 17)

    def test_get_all_home_matches_winner_by_team_name(self):
        matches = self.team_domain.get_all_home_matches_winner_by_team_name('BENFICA')
        self.assertIsInstance(matches, list)
        self.assertTrue(len(matches) > 0)

    def test_get_all_home_matches_lose_by_team_name(self):
        matches = self.team_domain.get_all_home_matches_lose_by_team_name('BENFICA')
        self.assertIsInstance(matches, list)
        self.assertTrue(len(matches) > 0)

    def test_get_all_home_matches_draw_by_team_name(self):
        matches = self.team_domain.get_all_home_matches_draw_by_team_name('BENFICA')
        self.assertIsInstance(matches, list)
        self.assertTrue(len(matches) > 0)

    def test_get_all_away_matches_winner_by_team_name(self):
        matches = self.team_domain.get_all_away_matches_winner_by_team_name('BENFICA')
        self.assertIsInstance(matches, list)
        self.assertTrue(len(matches) > 0)

    def test_get_all_away_matches_lose_by_team_name(self):
        matches = self.team_domain.get_all_away_matches_lose_by_team_name('BENFICA')
        self.assertIsInstance(matches, list)
        self.assertTrue(len(matches) > 0)

    def test_get_all_away_matches_draw_by_team_name(self):
        matches = self.team_domain.get_all_away_matches_draw_by_team_name('BENFICA')
        self.assertIsInstance(matches, list)
        self.assertTrue(len(matches) > 0)

    def test_get_all_matches_winner_by_team_name(self):
        matches = self.team_domain.get_all_matches_winner_by_team_name('BENFICA')
        self.assertIsInstance(matches, list)
        self.assertTrue(len(matches) == 28)

    def test_get_all_matches_lose_by_team_name(self):
        matches = self.team_domain.get_all_matches_lose_by_team_name('BENFICA')
        self.assertIsInstance(matches, list)
        self.assertTrue(len(matches) == 3)

    def test_get_all_matches_draw_by_team_name(self):
        matches = self.team_domain.get_all_matches_draw_by_team_name('BENFICA')
        self.assertIsInstance(matches, list)
        self.assertTrue(len(matches) == 3)