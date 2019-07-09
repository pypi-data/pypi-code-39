from pprint import pprint
from sports_client_factory import SportsClientFactory
from datetime import date
# import json

subs_key_nba = '38894df74dde436f9e749089aaa28106'

factory = SportsClientFactory()
sr = factory.get_api_client('nba')
# print("\n Testing get_pre_game_odds_by_date \n")
# data = sr.get_pre_game_odds_by_date()
# pprint(data)

# print("\n Testing get_pre_game_odds \n")
ddate = date(2019, 1, 31)
end_date = date(2019, 1, 31)
# data = sr.get_pre_game_odds(start_date, end_date)
# data = sr.get_pre_game_odds('2019-05-15', '2019-05-25')
print("\n Testing get injury news \n")
# data = sr.get_player_game_stats_by_player(ddate, 20001984)
# data = sr.get_injuries_report(ddate, end_date)
data = sr.get_injuries_news_by_date(ddate)
# data = sr.get_injuries_report()
# data = sr.get_pre_game_odds_by_date()
# data = sr.get_player_detail(20000439)

pprint(data)
