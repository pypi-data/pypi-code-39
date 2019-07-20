from football_tools.team_domain import TeamDomain

class Statistics(TeamDomain):
    def count_total_matches_by_team(self, team):
        return len(super().get_all_matches_by_team_name(team))

    def count_total_matches_winner_by_team(self, team):
        return len(super().get_all_matches_winner_by_team_name(team))
    
    def count_total_matches_lose_by_team(self, team):
        return len(super().get_all_matches_lose_by_team_name(team))

    def count_total_matches_draw_by_team(self, team):
        return len(super().get_all_matches_draw_by_team_name(team))

    def percentage_of_matches_winner_by_team(self):
        return (self.total_matches_winner * 100) / self.total_matches

    def percentage_of_matches_lose_by_team(self):
        return (self.total_matches_lose * 100) / self.total_matches 

    def percentage_of_matches_draw_by_team(self):
        return (self.total_matches_draw * 100) / self.total_matches 

    def __init__(self, team):
        self.team_name = self.storage[team.lower()]['team_name']
        self.total_matches_winner = self.count_total_matches_winner_by_team(team)
        self.total_matches_lose = self.count_total_matches_lose_by_team(team)
        self.total_matches_draw = self.count_total_matches_draw_by_team(team)
        self.total_matches = self.count_total_matches_by_team(team)
        self.percentage_of_matches_winner = self.percentage_of_matches_winner_by_team()
        self.percentage_of_matches_lose = self.percentage_of_matches_lose_by_team()
        self.percentage_of_matches_draw = self.percentage_of_matches_draw_by_team()
        
