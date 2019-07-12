from datetime import datetime
import logging
import requests
from sys import stdout
from .hero import Hero
from .match import Match

logger = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
logger.addHandler(out_hdlr)
logger.setLevel(logging.INFO)


class Player():
    """ Match data from the OpenDota players endpoint.
    Sends request to API endpoint only when data is needed.

    API reference: https://docs.opendota.com/#tag/players

    Args:
        account_id (int): The account ID
    """
    def __init__(self, account_id):
        self._id = int(account_id)
        self._loaded = False
        
        # Populate fields with None
        self._avatar           = None
        self._avatarmedium     = None
        self._avatarfull       = None
        self._cheese           = None
        self._competitive_rank = None
        self._is_contributor   = None
        self._last_login       = None
        self._loccountrycode   = None
        self._mmr_estimate     = None
        self._name             = None
        self._personaname      = None
        self._plus             = None
        self._profileurl       = None
        self._rank_tier        = None
        self._tracked_until    = None
        self._steamid          = None

        self._wins = None
        self._losses = None

        # Other endpoints
        self._heroes = None
        self._heroes_args = None
        self._recent_matches = None
        self._matches = None
        self._matches_args = None
        self._wl = None
        self._wl_args = None

    def __str__(self):
        """ Print all attributes if the player is printed """
        return (f"id: {self.id}\n"
                f"avatar: {self.avatar}\n"
                f"avatarmedium: {self.avatarmedium}\n"
                f"avatarfull: {self.avatarfull}\n"
                f"cheese: {self.cheese}\n"
                f"competitive_rank: {self.competitive_rank}\n"
                f"is_contributor: {self.is_contributor}\n"
                f"last_login: {self.last_login}\n"
                f"loccountrycode: {self.loccountrycode}\n"
                f"mmr_estimate: {self.mmr_estimate}\n"
                f"name: {self.name}\n"
                f"personaname: {self.personaname}\n"
                f"plus: {self.plus}\n"
                f"profileurl: {self.profileurl}\n"
                f"rank_tier: {self.rank_tier}\n"
                f"tracked_until: {self.tracked_until}\n"
                f"steamid: {self.steamid}")
    
    def _load(self):
        """ Loads data from the /api/players endpoint. """
        if not self._loaded:
            logger.info("Loading player data for account id: %s", self._id)
            url = f"https://api.opendota.com/api/players/{self._id}"
            self.data = requests.get(url).json()
            self.profile = self.data.get('profile', {})
            self._avatar           = self.profile.get('avatar')
            self._avatarmedium     = self.profile.get('avatarmedium')
            self._avatarfull       = self.profile.get('avatarfull')
            self._cheese           = self.profile.get('cheese')
            self._competitive_rank = self.profile.get('competitive_rank')
            self._is_contributor   = self.profile.get('is_contributor')
            self._last_login       = self.profile.get('last_login')
            self._loccountrycode   = self.profile.get('loccountrycode')
            self._mmr_estimate     = self.data.get('mmr_estimate', {}).get('estimate')
            self._name             = self.profile.get('name')
            self._personaname      = self.profile.get('personaname')
            self._plus             = self.profile.get('plus')
            self._profileurl       = self.profile.get('profileurl')
            self._rank_tier        = self.profile.get('rank_tier')
            self._tracked_until    = self.data.get('tracked_until')
            self._steamid          = self.profile.get('steamid')

            # Convert last_login to datetime
            if self._last_login:
                self._last_login = datetime.strptime(
                    self._last_login, "%Y-%m-%dT%H:%M:%S.%fZ")

            # Convert tracked_until to datetime
            if self._tracked_until:
                self._tracked_until = datetime.fromtimestamp(int(self._tracked_until))

            self._loaded = True

    def _get(self, key):
        """ Loads data if missing before getting an attribute """
        try:
            val = getattr(self, f"_{key}")
            if val is not None:
                return val
            else:
                self._load()
                return getattr(self, f"_{key}")
        except AttributeError:
            return None

    @property
    def id(self):
        """ Account ID """
        return self._id

    @property
    def account_id(self):
        """ Account ID """
        return self._id

    @property
    def avatar(self):
        """ URL of the user's avatar (32x32) """
        return self._get("avatar")

    @property
    def avatarmedium(self):
        """ URL of the user's avatar (64x64) """
        return self._get("avatarmedium")

    @property
    def avatarfull(self):
        """ URL of the user's avatar (184x184) """
        return self._get("avatarfull")

    @property
    def cheese(self):
        """ Cheese """
        return self._get("cheese")

    @property
    def competitive_rank(self):
        """ Competitive rank """
        return self._get("competitive_rank")

    @property
    def is_contributor(self):
        """ True if the player is an OpenDota contributor """
        return self._get("is_contributor")

    @property
    def last_login(self):
        """ Last time the player logged in, as a datetime """
        return self._get("last_login")

    @property
    def loccountrycode(self):
        """ Country code string """
        return self._get("loccountrycode")

    @property
    def mmr_estimate(self):
        """ Player's estimated MMR """
        return self._get("mmr_estimate")

    @property
    def name(self):
        """ Player's name """
        return self._get("name")

    @property
    def personaname(self):
        """ Persona name """
        return self._get("personaname")

    @property
    def plus(self):
        """ Plus """
        return self._get("plus")

    @property
    def profileurl(self):
        """ Profile URL """
        return self._get("profileurl")

    @property
    def rank_tier(self):
        """ Rank tier """
        return self._get("rank_tier")

    @property
    def tracked_until(self):
        """ Tracked until """
        return self._get("tracked_until")

    @property
    def steamid(self):
        """ Steam ID """
        return self._get("steamid")

    @property
    def url(self):
        """ URL to the player on opendota.com """
        return f"https://www.opendota.com/players/{self._id}"

    @property
    def recent_matches(self):
        """ Gets the player's recent matches played

        https://docs.opendota.com/#tag/players%2Fpaths%2F~1players~1%7Baccount_id%7D~1recentMatches%2Fget

        Returns a list of Match objects with the following attributes set:  
            (bool) match.radiant_win  
            (int) match.duration  
            (int) match.game_mode  
            (int) match.cluster  
            (int) match.lobby_type  
            (int) match.skill  
            (int) match.start_time  
            (int) match.version  

        Along with the following player specific attributes:  
            (int) match.assists  
            (int) match.deaths  
            (int) match.hero_id  
            (bool) match.is_roaming  
            (int) match.kills  
            (int) match.lane  
            (int) match.lane_role  
            (int) match.leaver_status  
            (int) match.player_slot  
            (int) match.party_size
        """
        if not self._recent_matches:
            url = f"https://api.opendota.com/api/players/{self.id}/recentMatches"
            logger.info("Loading recent matches for %s from url : %s",
                        self.personaname, url)
            data = requests.get(url).json()
            self._recent_matches = []
            for item in data:
                # Add user data to match object
                match = Match(item.get('match_id'))

                # Player specific attributes
                match.assists       = item.get("assists")
                match.deaths        = item.get("deaths")
                match.hero_id       = item.get("hero_id")
                match.is_roaming    = item.get("is_roaming")
                match.kills         = item.get("kills")
                match.lane          = item.get("lane")
                match.lane_role     = item.get("lane_role")
                match.leaver_status = item.get("leaver_status")
                match.player_slot   = item.get("player_slot")
                match.party_size    = item.get("party_size")

                # Private attributes (properties)
                match._radiant_win = item.get("radiant_win")
                match._duration    = item.get("duration")
                match._game_mode   = item.get("game_mode")
                match._cluster     = item.get("cluster")
                match._lobby_type  = item.get("lobby_type")
                match._skill       = item.get("skill")
                match._start_time  = item.get("start_time")
                match._version     = item.get("version")

                self._recent_matches.append(match)

        return self._recent_matches

    def wl(self, **kwargs):
        """ Gets the player's Win/Loss count

        Keyword Args:  
            (int) limit: Number of matches to limit to  
            (int) offset: Number of matches to offset start by  
            (int) win: Whether the player won  
            (int) patch: Patch ID  
            (int) game_mode: Game Mode ID  
            (int) lobby_type: Lobby type ID  
            (int) region: Region ID  
            (int) date: Days previous  
            (int) lane_role: Lane Role ID  
            (int) hero_id: Hero ID  
            (int) is_radiant: Whether the player was radiant  
            ([int]) included_account_id: Account IDs in the match  
            ([int]) excluded_account_id: Account IDs not in the match  
            ([int]) with_hero_id: Hero IDs on the player's team  
            ([int]) against_hero_id: Hero IDs against the player's team  
            (int) significant: Whether the match was significant.  
             -- Defaults to 1, set to 0 for non-standard modes/matches  
            (int) having: The minimum number of games played  
            (str) sort: The field to return matches sorted (descending)  

        Returns a dict with two keys:  
            (int) win: Number of wins  
            (int) lose Number of losses
        """
        if not self._wl and kwargs is not self._wl_args:
            self._wl_args = kwargs
            logger.info("Loading win-loss for %s", self.personaname)
            url = f"https://api.opendota.com/api/players/{self.id}/wl?"
            for key in ('limit', 'offset', 'win', 'patch', 'game_mode', 'lobby_type', 'region', 'date', 'lane_role', 'hero_id', 'is_radiant', 'included_account_id', 'excluded_account_id', 'with_hero_id', 'against_hero_id', 'significant', 'having', 'sort'):
                if key in kwargs:
                    url += f"{key}={kwargs[key]}&"
            logger.info("url : %s", url)
            self._wl = requests.get(url).json()
        return self._wl

    def heroes(self, **kwargs):
        """ Gets the player's most played heroes

        Keyword Args:  
            (int) limit: Number of matches to limit to  
            (int) offset: Number of matches to offset start by  
            (int) win: Whether the player won  
            (int) patch: Patch ID  
            (int) game_mode: Game Mode ID  
            (int) lobby_type: Lobby type ID  
            (int) region: Region ID  
            (int) date: Days previous  
            (int) lane_role: Lane Role ID  
            (int) hero_id: Hero ID  
            (int) is_radiant: Whether the player was radiant  
            ([int]) included_account_id: Account IDs in the match  
            ([int]) excluded_account_id: Account IDs not in the match  
            ([int]) with_hero_id: Hero IDs on the player's team  
            ([int]) against_hero_id: Hero IDs against the player's team  
            (int) significant: Whether the match was significant.  
              -- Defaults to 1, set to 0 for non-standard modes/matches  
            (int) having: The minimum number of games played  
            (str) sort: The field to return matches sorted (descending)  

        Returns a list of Hero objects with the following attributes set:  
            (int) hero.last_played
            (int) hero.games
            (int) hero.win
            (int) hero.with_games
            (int) hero.with_win
            (int) hero.against_games
            (int) hero.against_win
        """
        if not self._heroes and kwargs is not self._heroes_args:
            self._heroes_args = kwargs
            logger.info("Loading top heroes for %s", self.personaname)
            url = f"https://api.opendota.com/api/players/{self.id}/heroes?"
            for key in ('limit', 'offset', 'win', 'patch', 'game_mode', 'lobby_type', 'region', 'date', 'lane_role', 'hero_id', 'is_radiant', 'included_account_id', 'excluded_account_id', 'with_hero_id', 'against_hero_id', 'significant', 'having', 'sort'):
                if key in kwargs:
                    url += f"{key}={kwargs[key]}&"
            logger.info("url : %s", url)
            data = requests.get(url).json()
            self._heroes = []
            for item in data:
                hero = Hero(item.get('hero_id'))

                # Add user info to Hero object
                hero.last_played = item.get('last_played')
                hero.games = item.get('games')
                hero.win = item.get('win')
                hero.with_games = item.get('with_games')
                hero.with_win = item.get('with_win')
                hero.against_games = item.get('against_games')
                hero.against_win = item.get('against_win')

                self._heroes.append(hero)

        return self._heroes

    def refresh(self):
        """ Sends a POST to the OpenDota refresh player api endpoint.
        
        Returns:
            requests.Response: The POST response.
        """
        logger.info(f"Refreshing player data for %s", self._id)
        url = f"https://api.opendota.com/api/players/{self._id}/refresh"
        response = requests.post(url)
        return response

    def matches(self, **kwargs):
        """ Gets the player's matches

        https://docs.opendota.com/#tag/players%2Fpaths%2F~1players~1%7Baccount_id%7D~1matches%2Fget

        Keyword Args convert to query parameters:  
            (int) limit:  Number of matches to limit to  
            (int) offset:  Number of matches to offset start by  
            (int) win:  Whether the player won  
            (int) patch:  Patch ID  
            (int) game_mode:  Game Mode ID  
            (int) lobby_type:  Lobby type ID  
            (int) region:  Region ID  
            (int) date:  Days previous  
            (int) lane_role:  Lane Role ID  
            (int) hero_id:  Hero ID  
            (int) is_radiant:  Whether the player was radiant  
            ([int]) included_account_id: Account IDs in the match  
            ([int]) excluded_account_id: Account IDs not in the match  
            ([int]) with_hero_id: Hero IDs on the player's team  
            ([int]) against_hero_id: Hero IDs against the player's team  
            (int) significant:  Whether the match was significant.  
             -- Defaults to 1, set to 0 for non-standard modes/matches  
            (int) having:  The minimum number of games played  
            (str) sort:  The field to return matches sorted (descending)  
            ([str]) project: Fields to project  

        Returns a list of Match objects with the following attributes set:  
            (bool) match.radiant_win  
            (int) match.duration  
            (int) match.game_mode  
            (int) match.lobby_type  
            (int) match.skill  
            (int) match.start_time  
            (int) match.version  
            
        Along with the following player specific attributes:
            (int) match.player_slot  
            (int) match.hero_id  
            (int) match.kills  
            (int) match.deaths  
            (int) match.assists  
            (int) match.party_size  
            (int) match.leaver_status

        """
        if not self._matches and kwargs is not self._matches_args:
            self._matches_args = kwargs
            url = f"https://api.opendota.com/api/players/{self.id}/matches?"

            # Valid query parameters
            params = ['limit', 'offset', 'win', 'patch', 'game_mode', 'lobby_type',
                    'region', 'date', 'lane_role', 'hero_id', 'is_radiant',
                    'included_account_id', 'excluded_account_id', 'with_hero_id',
                    'against_hero_id', 'significant', 'having', 'sort', 'project']

            # Add it to the url if passed as a keyword argument
            for param in params:
                if param in kwargs:
                    url += f"{param}={kwargs[param]}&"

            logger.info("Loading matches for %s from url : %s",
                        self.personaname, url)
            data = requests.get(url).json()
            self._matches = []
            for item in data:
                # Add user data to match object
                match = Match(item.get('match_id'))

                # Player specific attributes
                match.player_slot   = item.get("player_slot")
                match.hero_id       = item.get("hero_id")
                match.kills         = item.get("kills")
                match.deaths        = item.get("deaths")
                match.assists       = item.get("assists")
                match.party_size    = item.get("party_size")
                match.leaver_status = item.get("leaver_status")

                # Private attributes (properties)
                match._radiant_win = item.get("radiant_win")
                match._duration    = item.get("duration")
                match._game_mode   = item.get("game_mode")
                match._lobby_type  = item.get("lobby_type")
                match._skill       = item.get("skill")
                match._start_time  = item.get("start_time")
                match._version     = item.get("version")

                self._matches.append(match)
        return self._matches
