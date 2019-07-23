import requests
from . import driver
class Account(object):
    """Overwatch League teams and players each have their social media accounts for interacting with fans. Each Account object has an account ID, an account type, and an account URL."""
    def __init__(self, id, accountType=None, value=None, competitorId=None, isPublic=None, type=None, url=None):
        self.id = id
        if accountType:
            self.type = accountType
        else:
            self.type = type
        if value:
            self.url = value
        else:
            self.url = url
    
    def _getlatestpost():
        pass

class Blog(object):
    def __init__(self, blodId, created, updated, publish, title, author, \
                locale, keywords, summary, commentKey, status, thumbnail, \
                defaultCommunity, defaultUrl, commentsEnabled, pollAttached, \
                localizationPublish, siteCategory):
        """A Blog is where articles pertaining to Overwatch League are located. Each Blog covers topics including player news, match summaries, team updates, and more."""
        self.blogId = blogId
        self.created = created
        self.updated = updated
        self.publish = publish
        self.title = title
        self.author = author
        self.locale = locale
        self.keywords = keywords
        self.summary = summary,
        self.commentKey = commentKey,
        self.status = status,
        self.thumbnail = thumbnail,
        self.defaultCommunity = defaultCommunity
        self.defaultUrl = defaultUrl
        self.commentsEnabled = commentsEnabled
        self.pollAttached = pollAttached
        self.localizationPublish = localizationPublish
        self.siteCategory = siteCategory
    

class Bracket(object):
    pass

class Colors(object):
    def __init__(self, primary, secondary, tertiary):
        """Colors in int"""
        self.primary = int(primary["color"][1:], 16)
        self.secondary = int(secondary["color"][1:], 16)
        self.tertiary = int(tertiary["color"][1:], 16)

class Competitor(object):
    def __init__(self, id, availableLanguages, handle, name, homeLocation, \
                primaryColor, secondaryColor, game, attributes, attributesVersion, \
                abbreviatedName, addressCountry, logo, icon, players, secondaryPhoto, type):
        """Model for a competitor/team and associated information"""
        self.id = id
        self.availableLanguages = availableLanguages
        self.handle = handle
        self.name = name
        self.homeLocation = homeLocation
        self.primaryColor = primaryColor
        self.secondaryColor = secondaryColor
        self.game = game
        self.attributes = attributes
        self.attributesVersion = attributesVersion
        self.abbreviatedName = abbreviatedName
        self.addressCountry = addressCountry
        self.logo = logo
        self.icon = icon
        self.players = players
        self.secondaryPhoto = secondaryPhoto
        self.type = type
    pass


class Team(Competitor):
    def __init__(self, id, divisionId, handle, name, abbreviatedName, logo, \
                hasFallback, location, players, colors, accounts, website, \
                placement, advantage, records):
        """Model for a team and associated information"""
        self.id = id
        self.divisionId = divisionId
        self.handle = handle
        self.name = name
        self.abbreviatedName = abbreviatedName
        self.logo = logo
        self.hasFallback = hasFallback
        self.location = location
        self.players = players
        self.colors = Colors(colors["primary"], colors["secondary"], colors["tertiary"])
        self.accounts = []
        if accounts is not None:
            for a in accounts:
                self.accounts.append(Account(**a))
        self.website = website
        self.placement = placement
        self.advantage = advantage
        self.records = Records(**records)
    pass

class Game(object):
    pass

class GameMode(object):
    pass

class Match(object):
    def __init__(self, id, competitors, scores, round, ordinal, winnersNextMatch, winnerRound, \
                winnerOrdinal, bestOf, conclusionValue, conclusionStrategy, winner, home, \
                state, status, statusReason, attributes, games, clientHints, bracket, dateCreated, \
                flags, handle, competitorStatuses, timeZone, actualStartDate, actualEndDate, \
                startDate, endDate, showStartTime, showEndTime, rankings, meta):
        """An Overwatch League Match consists of 4 games taking place in four different maps and game modes. Matches are normally determined with a "Best of" conclusion strategy"""
        self.driver = driver.Driver()
        self.id = id
        self.competitors = []
        for c in competitors:
            self.competitors.append(self.driver.get_team_by_id(c["id"]))
        self.scores = scores
        self.round = round
        self.ordinal = ordinal
        self.winnersNextMatch = winnersNextMatch
        self.winnerRound = winnerRound
        self.winnerOrdinal = winnerOrdinal
        self.bestOf = bestOf
        self.conclusionValue = conclusionValue
        self.conclusionStrategy = conclusionStrategy
        self.winner = winner
        self.home = home
        self.state = state
        self.status = status
        self.statusReason = statusReason
        self.attributes = attributes
        self.games = games
        self.clientHints = clientHints
        self.bracket = bracket
        self.dateCreated = dateCreated
        self.flags = flags
        self.handle = handle
        self.competitorStatuses = competitorStatuses, timeZone
        self.actualStartDate = actualStartDate
        self.actualEndDate = actualEndDate
        self.startDate = startDate
        self.endDate = endDate
        self.showStartTime = showStartTime
        self.showEndTime = showEndTime
        self.rankings = rankings
        self.meta = meta
        pass
    pass

class LiveMatch(Match):
    pass

class Logo(object):
    pass

class NextMatch(Match):
    pass

class Player(object):
    def __init__(self, id, name, accounts, headshot, homeLocation=None, \
                availableLanguages=None, role=None, fullName=None, number=None, \
                game=None, attributes=None, attributesVersion=None, familyName=None, givenName=None, \
                nationality=None, type=None, teams=None, handle=None):
        """A Player is a member of a competing Overwatch League team"""
        self.id = id
        self.availableLanguages = availableLanguages
        self.handle = handle
        self.name = name
        self.homeLocation = homeLocation
        self.accounts = []
        if accounts is not None:
            for a in accounts:
                self.accounts.append(Account(**a))
        self.game = game
        self.attributes = attributes
        self.attributesVersion = attributesVersion
        self.familyName = familyName
        self.givenName = givenName
        self.nationality = nationality
        self.headshot = headshot
        self.teams = teams
        self.type = type
    
    def formatted_name(self):
        return("{}. {} (A.K.A {})".format(self.givenName[0], self.familyName, self.name))
    
    def get_team(self):
        d = driver.Driver()
        return  d.get_team_by_id(self.teams[0]["team"]["id"])


class Records(object):
    def __init__(self, matchWin, matchLoss, matchDraw, matchBye, \
                gameWin, gameLoss, gameTie, gamePointsFor, gamePointsAgainst, \
                comparisons):
        """Records maintain information about a Team's statistics"""
        self.matchWin = matchWin
        self.matchLoss = matchLoss
        self.matchDraw = matchDraw
        self.matchBye = matchBye
        self.gameWin = gameWin
        self.gameLoss = gameLoss
        self.gameTie = gameTie
        self.gamePointsFor = gamePointsFor
        self.gamePointsAgainst = gamePointsAgainst
        self.comparisons = comparisons
        

class VOD(object):
    pass
