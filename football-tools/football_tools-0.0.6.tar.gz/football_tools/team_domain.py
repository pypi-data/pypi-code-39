from football_tools.storage import StorageRepository

class MatchLine():
    def __init__(self, line):
        self.league = line[0]
        self.date = line[1]
        self.home_team = line[2]
        self.away_team = line[3]
        self.full_time_home_goals = line[4]
        self.full_time_away_goals = line[5]
        self.full_time_winner = line[6]
        if len(line) > 7:
            self.half_time_home_goals = line[7]
            self.half_time_away_goals = line[8]
            self.half_time_winner = line[9]

class TeamDomain(StorageRepository):
    def __init__(self):
        pass
    
    def parse_match_line(self, line):
        return MatchLine(line)

    def get_all_teams(self):
        return list(super().storage.keys())

    def get_all_matches_by_team_name(self, team_name):
        return super().storage[team_name.lower()]['matches']

    def get_all_home_matches_by_team_name(self, team_name):
        home_matches = []
        matches = super().storage[team_name.lower()]['matches']
        for match in matches:
            if MatchLine(match).home_team.lower() == team_name.lower():
                home_matches.append(match)
        return home_matches

    def get_all_away_matches_by_team_name(self, team_name):
        away_matches = []
        matches = super().storage[team_name.lower()]['matches']
        for match in matches:
            if MatchLine(match).away_team.lower() == team_name.lower():
                away_matches.append(match)
        return away_matches

    def get_all_home_matches_winner_by_team_name(self, team_name):
        home_matches = []
        matches = super().storage[team_name.lower()]['matches']
        for match in matches:
            if MatchLine(match).home_team.lower() == team_name.lower() and MatchLine(match).full_time_winner == "H":
                home_matches.append(match)
        return home_matches

    def get_all_home_matches_lose_by_team_name(self, team_name):
        home_matches = []
        matches = super().storage[team_name.lower()]['matches']
        for match in matches:
            if MatchLine(match).home_team.lower() == team_name.lower() and MatchLine(match).full_time_winner == "A":
                home_matches.append(match)
        return home_matches
    
    def get_all_home_matches_draw_by_team_name(self, team_name):
        home_matches = []
        matches = super().storage[team_name.lower()]['matches']
        for match in matches:
            if MatchLine(match).home_team.lower() == team_name.lower() and MatchLine(match).full_time_winner == "D":
                home_matches.append(match)
        return home_matches

    def get_all_away_matches_winner_by_team_name(self, team_name):
        away_matches = []
        matches = super().storage[team_name.lower()]['matches']
        for match in matches:
            if MatchLine(match).away_team.lower() == team_name.lower() and MatchLine(match).full_time_winner == "A":
                away_matches.append(match)
        return away_matches

    def get_all_away_matches_lose_by_team_name(self, team_name):
        away_matches = []
        matches = super().storage[team_name.lower()]['matches']
        for match in matches:
            if MatchLine(match).away_team.lower() == team_name.lower() and MatchLine(match).full_time_winner == "H":
                away_matches.append(match)
        return away_matches

    def get_all_away_matches_draw_by_team_name(self, team_name):
        away_matches = []
        matches = super().storage[team_name.lower()]['matches']
        for match in matches:
            if MatchLine(match).away_team.lower() == team_name.lower() and MatchLine(match).full_time_winner == "D":
                away_matches.append(match)
        return away_matches

    def get_all_matches_winner_by_team_name(self, team_name):
        tmatches = []
        matches = super().storage[team_name.lower()]['matches']
        for match in matches:
            if (MatchLine(match).away_team.lower() == team_name.lower() and MatchLine(match).full_time_winner == "A") or (MatchLine(match).home_team.lower() == team_name.lower() and MatchLine(match).full_time_winner == "H"):
                tmatches.append(match)
        return tmatches

    def get_all_matches_lose_by_team_name(self, team_name):
        tmatches = []
        matches = super().storage[team_name.lower()]['matches']
        for match in matches:
            if (MatchLine(match).away_team.lower() == team_name.lower() and MatchLine(match).full_time_winner == "H") or (MatchLine(match).home_team.lower() == team_name.lower() and MatchLine(match).full_time_winner == "A"):
                tmatches.append(match)
        return tmatches

    def get_all_matches_draw_by_team_name(self, team_name):
        tmatches = []
        matches = super().storage[team_name.lower()]['matches']
        for match in matches:
            if (MatchLine(match).away_team.lower() == team_name.lower() and MatchLine(match).full_time_winner == "H") or (MatchLine(match).home_team.lower() == team_name.lower() and MatchLine(match).full_time_winner == "A"):
                tmatches.append(match)
        return tmatches

    