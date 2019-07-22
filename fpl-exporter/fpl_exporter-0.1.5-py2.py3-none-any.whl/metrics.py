# -*- coding: utf-8 -*-

from prometheus_client import Gauge, Enum
import logging

LOGGER = logging.getLogger(__name__)


class FPLMetrics:

    monitor_working_time = Gauge(
        "prometheus_exporter_fpl_work_time", "Exporter working time."
    )
    monitor_api_response_time = Gauge(
        "prometheus_exporter_fpl_api_response_time", "Exporter FPL API response time."
    )
    players = Gauge("fpl_players_total", "Number of FPL players.")
    fpl_assets = Gauge(
        "fpl_assets_total", "Number of football players in Premier League."
    )

    # Teams
    availability = Enum(
        "fpl_team_availability",
        "Team availability in current gameweek.",
        ["team"],
        states=["unknown", "available", "unavailable"],
    )
    strength_attack_home = Gauge(
        "fpl_team_strength_attack_home",
        "Team offensive strength on home games.",
        ["team"],
    )
    strength_attack_away = Gauge(
        "fpl_team_strength_attack_away",
        "Team offensive strength on away games.",
        ["team"],
    )
    strength_defence_home = Gauge(
        "fpl_team_strength_defence_home",
        "Team defensive strength on home games.",
        ["team"],
    )
    strength_defence_away = Gauge(
        "fpl_team_strength_defence_away",
        "Team defensive strength on away games.",
        ["team"],
    )
    strength_overall_home = Gauge(
        "fpl_team_strength_overal_home",
        "Team overall strength on home games.",
        ["team"],
    )
    strength_overall_away = Gauge(
        "fpl_team_strength_overal_away",
        "Team overall strength on away games.",
        ["team"],
    )
    # form = Gauge(
    #    "fpl_team_form", "Team overal form.", ["team"]
    # )
    strength = Gauge("fpl_team_strength", "Team strength.", ["team"])
    #
    position = Gauge(
        "fpl_team_table_position", "Team position in Premier League table.", ["team"]
    )
    points = Gauge(
        "fpl_team_table_points",
        "Team points accumulated in Premier League table.",
        ["team"],
    )
    played = Gauge("fpl_team_games_played", "Games won.", ["team"])
    win = Gauge("fpl_team_games_won", "Games won.", ["team"])
    loss = Gauge("fpl_team_games_lost", "Games lost.", ["team"])
    draw = Gauge("fpl_team_games_drawn", "Games drawn.", ["team"])

    # Players
    ict_index = Gauge("fpl_asset_ict_index", "", ["asset"])
    influence = Gauge("fpl_asset_influence", "", ["asset"])
    creativity = Gauge("fpl_asset_creativity", "", ["asset"])
    threat = Gauge("fpl_asset_threat", "", ["asset"])
    selected_by_percent = Gauge("fpl_asset_selected_by_percent", "", ["asset"])
    form = Gauge("fpl_asset_form", "", ["asset"])
    bonus = Gauge("fpl_asset_bonus", "", ["asset"])
    bps = Gauge("fpl_asset_bps", "", ["asset"])

    # Players - unused
    transfers_in = Gauge("fpl_asset_transfers_in", "", ["asset"])
    transfers_out = Gauge("fpl_asset_transfers_out", "", ["asset"])
    # transfers_in_event = Gauge("fpl_asset_transfers_in_event", "", ["asset"])
    # transfers_out_event = Gauge("fpl_asset_transfers_out_event", "", ["asset"])
    assists = Gauge("fpl_asset_assists", "", ["asset"])
    goals_scored = Gauge("fpl_asset_goals_scored", "", ["asset"])
    goals_conceded = Gauge("fpl_asset_goals_conceded", "", ["asset"])
    saves = Gauge("fpl_asset_saves", "", ["asset"])
    penalties_missed = Gauge("fpl_asset_penalties_missed", "", ["asset"])
    penalties_saved = Gauge("fpl_asset_penalties_saved", "", ["asset"])
    # chance_of_playing_next_round = Gauge("fpl_asset_chance_of_playing_next_round", "", ["asset"])
    # chance_of_playing_this_round = Gauge("fpl_asset_chance_of_playing_this_round", "", ["asset"])
    clean_sheets = Gauge("fpl_asset_clean_sheets", "", ["asset"])
    cost_change_event = Gauge("fpl_asset_cost_change_event", "", ["asset"])
    cost_change_event_fall = Gauge("fpl_asset_cost_change_event_fall", "", ["asset"])
    cost_change_start = Gauge("fpl_asset_cost_change_start", "", ["asset"])
    cost_change_start_fall = Gauge("fpl_asset_cost_change_start_fall", "", ["asset"])
    minutes = Gauge("fpl_asset_minutes", "", ["asset"])
    total_points = Gauge("fpl_asset_total_points", "", ["asset"])
    # special = Gauge("fpl_asset_special", "", ["asset"])
    # squad_number = Gauge("fpl_asset_squad_number", "", ["asset"])
    # status = Gauge("fpl_asset_status", "", ["asset"])
    now_cost = Gauge("fpl_asset_now_cost", "", ["asset"])
    value_form = Gauge("fpl_asset_value_form", "", ["asset"])
    value_season = Gauge("fpl_asset_value_season", "", ["asset"])
    own_goals = Gauge("fpl_asset_own_goals", "", ["asset"])
    points_per_game = Gauge("fpl_asset_points_per_game", "", ["asset"])
    red_cards = Gauge("fpl_asset_red_cards", "", ["asset"])
    yellow_cards = Gauge("fpl_asset_yellow_cards", "", ["asset"])
    dreamteam_count = Gauge("fpl_asset_dreamteam_count", "", ["asset"])
    # in_dreamteam = Gauge("fpl_asset_in_dreamteam", "", ["asset"])
    # newa = Gauge("fpl_asset_newsnews", "", ["asset"])
    event_points = Gauge("fpl_asset_event_points", "", ["asset"])
