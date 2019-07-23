import requests
from OWLPy.objects import Player, Team, Match
from OWLPy.errors import *

class Driver(object):
    """An Object for controlling API functions"""
    def __init__(self):
        self.baseurl = "https://api.overwatchleague.com/"
    
    # Acquire Players
    def get_player_by_id(self, id): 
        r = requests.get("{}/player/{}".format(self.baseurl, id)).json()["data"]["player"]
        return Player(**r)

    def get_player_by_name(self, name): 
        r = requests.get("{}/players".format(self.baseurl)).json()["content"]
        for p in r:
            if p["name"] == name:
                return Player(**p)
        raise PlayerNotFound()


    # Acquire Teams
    def get_team_by_id(self, id):
        r = requests.get("{}/v2/teams/{}".format(self.baseurl, id)).json()["data"]
        return Team(**r)

    def get_team_by_name(self, name): 
        r = requests.get("{}/v2/teams".format(self.baseurl)).json()["data"]
        for t in r:
            if t["name"] == name:
                team = self.get_team_by_id(t["id"])
                return team
        raise TeamNotFound()

    
    # Acquire Players
    def get_match_by_id(self, id): 
        r = requests.get("{}/match/{}".format(self.baseurl, id)).json()
        return Match(**r)

    def get_match_by_name(self, name): 
        r = requests.get("{}/players".format(self.baseurl)).json()["content"]
        for m in r:
            if m["name"] == name:
                return Match(**m)
        raise MatchNotFound()

