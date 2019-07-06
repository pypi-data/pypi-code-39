import requests
from datetime import datetime
import hashlib
import json


class Connector:

    def __init__(self, dev_id, auth):
        self.devID = dev_id
        self.auth = auth
        self.url = "http://api.smitegame.com/smiteapi.svc/"
        self.session_id = self.create_session()

    def _create_signature(self, method):
        """
        Create the signature to be used in url of each method

        :param method: String: name of method to create signature for
        :return: Signature and time
        """

        time = _get_time()

        to_be_encoded = self.devID + method + self.auth + time

        result = hashlib.md5(to_be_encoded.encode())

        return result.hexdigest(), time

    def create_session(self):
        """
        Create a session with the smite API

        :return: str
        """

        signature, time = self._create_signature("createsession")

        site = self.url + "createsessionjson/" + self.devID + "/" + signature + "/" + time

        result = requests.get(site)

        response = json.loads(result.text)

        return response["session_id"]

    def new_session(self):
        """
        Create a new session

        :return: None
        """
        self.session_id = self.create_session()

    def _check(self):
        """
        Check if connection is still valid, if not create a new session

        :return: None
        """

        result = self.test_session().split()

        if result[0] == "Invalid":
            # Check was invalid
            self.new_session()

    def test_session(self):
        """
        A means of validating that a session is established.

        :return: list
        """

        signature, time = self._create_signature("testsession")

        site = self.url + "testsessionjson/" + self.devID + "/" + signature + "/" + self.session_id + "/" + time

        return self._get_result(site)

    def ping(self):
        """
        A quick way of validating access to the Hi-Rez API.

        :return: list
        """

        self._check()

        site = self.url + "pingjson"

        return self._get_result(site)

    def get_gods(self):
        """
        Mirrors the get_gods request in the smite API, returns a list of all gods and their information in smite, where
        each god is represented by a dictionary

        :return: list
        """

        self._check()

        signature, time = self._create_signature("getgods")

        site = self.url + "getgodsjson/" + self.devID + "/" + signature + "/" + self.session_id + "/" + time + "/" + "1"

        return self._get_result(site)

    def get_data_used(self):
        """
        Returns API Developer daily usage limits and the current status against those limits

        :return: list
        """

        self._check()

        signature, time = self._create_signature("getdataused")

        site = self.url + "getdatausedjson/" + self.devID + "/" + signature + "/" + self.session_id + "/" + time

        return self._get_result(site)

    def get_esports_pro_league_details(self):
        """
        Returns the match up information for each match up for the current eSports Pro League season. An important
        return value is “match_status” which represents a match being scheduled (1), in-progress (2), or complete (3)

        :return: list
        """

        self._check()

        signature, time = self._create_signature("getesportsproleaguedetails")

        site = self.url + "getesportsproleaguedetailsjson/" + self.devID + "/" + signature + \
            "/" + self.session_id + "/" + time

        return self._get_result(site)

    def get_friends(self, player):
        """
        Returns the Smite User names of each of the player’s friends.

        :param player: String
        :return: List
        """

        self._check()

        signature, time = self._create_signature("getfriends")

        site = self.url + "getfriendsjson/" + self.devID + "/" + signature + \
            "/" + self.session_id + "/" + time + "/" + player

        return self._get_result(site)

    def get_match_history(self, player):
        """
        Gets recent matches and high level match statistics for a particular player.


        :param player: String
        :return: List
        """

        self._check()

        signature, time = self._create_signature("getmatchhistory")

        site = self.url + "getmatchhistoryjson/" + self.devID + "/" + signature + \
            "/" + self.session_id + "/" + time + "/" + player

        return self._get_result(site)

    def get_god_ranks(self, player):
        """
        Returns all Gods and their various attributes.

        :param player: String
        :return: List
        """

        self._check()

        signature, time = self._create_signature("getgodranks")

        site = self.url + "getgodranksjson/" + self.devID + "/" + signature + \
            "/" + self.session_id + "/" + time + "/" + player

        return self._get_result(site)

    def get_god_recommended_items(self, god_id):
        """
        Returns the Recommended Items for a particular God

        :param god_id: String
        :return: List
        """

        self._check()

        signature, time = self._create_signature("getgodrecommendeditems")

        site = self.url + "getgodrecommendeditemsjson/" + self.devID + "/" + signature + \
            "/" + self.session_id + "/" + time + "/" + str(god_id) + "/1"

        return self._get_result(site)

    def get_items(self):
        """
        Returns all Items and their various attributes.

        :return: List
        """

        self._check()

        signature, time = self._create_signature("getitems")

        site = self.url + "getitemsjson/" + self.devID + "/" + signature + \
            "/" + self.session_id + "/" + time + "/1"

        return self._get_result(site)

    def get_match_details(self, match_id):
        """
        Returns the statistics for a particular completed match.

        :param match_id: String
        :return: List
        """

        self._check()

        signature, time = self._create_signature("getmatchdetails")

        site = self.url + "getmatchdetailsjson/" + self.devID + "/" + signature + \
            "/" + self.session_id + "/" + time + "/" + str(match_id)

        return self._get_result(site)

    def get_league_leaderboard(self, queue, tier, season):
        """
        Returns the top players for a particular league (as indicated by the queue/tier/season, as
         outlined by Smite API dev guide, parameters)

        :param queue: String
        :param tier: String
        :param season: String
        :return: List
        """

        self._check()

        signature, time = self._create_signature("getleagueleaderboard")

        site = self.url + "getleagueleaderboardjson/" + self.devID + "/" + signature + \
            "/" + self.session_id + "/" + time + "/" + str(queue) + "/" + str(tier) + "/" + str(season)

        return self._get_result(site)

    def get_league_seasons(self, queue):
        """
        Provides a list of seasons (including the single active season) for a match queue

        :param queue: String
        :return: List
        """

        self._check()

        signature, time = self._create_signature("getleagueseasons")

        site = self.url + "getleagueseasonsjson/" + self.devID + "/" + signature + \
            "/" + self.session_id + "/" + time + "/" + str(queue)

        return self._get_result(site)

    def get_player(self, player_name):
        """
        Returns league and other high level data for a particular player.

        :param player_name: String
        :return: List
        """

        self._check()

        signature, time = self._create_signature("getplayer")

        site = self.url + "getplayerjson/" + self.devID + "/" + signature + \
            "/" + self.session_id + "/" + time + "/" + player_name

        return self._get_result(site)

    def get_player_status(self, player_name):
        """
        Returns player status as follows:
        0 - Offline
        1 - In Lobby (basically anywhere except god selection or in game)
        2 - god Selection (player has accepted match and is selecting god before start of game)
        3 - In Game (match has started)
        4 - Online (player is logged in, but may be blocking broadcast of player state)

        :param player_name: String
        :return: List
        """

        self._check()

        signature, time = self._create_signature("getplayerstatus")

        site = self.url + "getplayerstatusjson/" + self.devID + "/" + signature + \
            "/" + self.session_id + "/" + time + "/" + player_name

        return self._get_result(site)

    def get_queue_stats(self, player_name, queue):
        """
        Returns match summary statistics for a (player, queue) combination grouped by gods played.

        :param player_name: String
        :param queue: String
        :return: List
        """

        self._check()

        signature, time = self._create_signature("getqueuestats")

        site = self.url + "getqueuestatsjson/" + self.devID + "/" + signature + \
            "/" + self.session_id + "/" + time + "/" + player_name + "/" + str(queue)

        return self._get_result(site)

    def search_teams(self, team_name):
        """
        Returns high level information for Team names containing the “team_name” string.

        :param team_name: String
        :return: List
        """

        self._check()

        signature, time = self._create_signature("searchteams")

        site = self.url + "searchteamsjson/" + self.devID + "/" + signature + \
            "/" + self.session_id + "/" + time + "/" + team_name

        return self._get_result(site)

    def get_team_match_history(self, clan_id):
        """
        Gets recent matches and high level match statistics for a particular clan/team.

        :param clan_id: String
        :return: List
        """

        self._check()

        signature, time = self._create_signature("getteammatchhistory")

        site = self.url + "getteammatchhistoryjson/" + self.devID + "/" + signature + \
            "/" + self.session_id + "/" + time + "/" + str(clan_id)

        return self._get_result(site)

    def get_team_players(self, clan_id):
        """
        Lists the players for a particular clan.

        :param clan_id: String
        :return: List
        """

        self._check()

        signature, time = self._create_signature("getteamplayers")

        site = self.url + "getteamplayersjson/" + self.devID + "/" + signature + "/" + \
            self.session_id + "/" + time + "/" + str(clan_id)

        return self._get_result(site)

    def get_top_matches(self):
        """
        Lists the 50 most watched / most recent recorded matches.

        :return: List
        """

        self._check()

        signature, time = self._create_signature("gettopmatches")

        site = self.url + "gettopmatchesjson/" + self.devID + "/" + signature + \
            "/" + self.session_id + "/" + time

        return self._get_result(site)

    def get_match_player_details(self, match_id):
        """
        Returns player information for a live match.

        :param match_id: String
        :return: List
        """

        self._check()

        signature, time = self._create_signature("getmatchplayerdetails")

        site = self.url + "getmatchplayerdetailsjson/" + self.devID + "/" + signature + \
            "/" + self.session_id + "/" + time + "/" + str(match_id)

        return self._get_result(site)

    def get_match_ids_by_queue(self, queue, date, hour):
        """
        Lists all Match IDs for a particular Match Queue; useful for API developers interested in constructing data by
        Queue. To limit the data returned, an {hour} parameter was added (valid values: 0 - 23). An {hour} parameter
        of -1 represents the entire day, but be warned that this may be more data than we can return for certain queues.
        Also, a returned “active_flag” means that there is no match information/stats for the corresponding match.
        Usually due to a match being in-progress, though there could be other reasons.


        :param queue: String
        :param date: String
        :param hour: String
        :return: List
        """

        self._check()

        signature, time = self._create_signature("getmatchidsbyqueue")

        site = self.url + "getmatchidsbyqueuejson/" + self.devID + "/" + signature + \
            "/" + self.session_id + "/" + time + "/" + str(queue) + "/" + str(date) + "/" + str(hour)

        return self._get_result(site)

    def get_team_details(self, clan_id):
        """
        Lists the number of players and other high level details for a particular clan.

        :param clan_id: String
        :return: List
        """

        self._check()

        signature, time = self._create_signature("getteamdetails")

        site = self.url + "getteamdetailsjson/" + self.devID + "/" + signature + \
            "/" + self.session_id + "/" + time + "/" + str(clan_id)

        return self._get_result(site)

    @staticmethod
    def _get_result(url):
        """
        Converts the returned data from the url and converts the JSON to a list

        :param url: String
        :return: List
        """

        result = requests.get(url)
        result = json.loads(result.text)
        return result


def _get_time():
    """
    Convert current time into UTC and required format for Smite API

    :return: String
    """

    time = str(datetime.utcnow())

    time = time.replace("-", "")
    time = time.replace(" ", "")
    time = time.replace(":", "")
    time = time.replace(".", "")

    time = time[:14]

    return time
