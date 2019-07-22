# -*- coding: utf-8 -*-

"""Main module."""
import time
import requests
import logging
import responses
import prometheus_client
from .metrics import FPLMetrics


MONITOR = FPLMetrics()
LOGGER = logging.getLogger(__name__)


def prometheus_exporter(api_client):
    exporter = FPLExporter()
    prometheus_client.start_http_server(5000)
    while True:
        metrics = exporter.get_metrics(api_client).json()
        exporter.set_metric_values(metrics)
        time.sleep(240)


class FPLExporter:
    def get_metrics(self, api_client):
        "Return response object."

        start = time.time()
        api_response = api_client.get("bootstrap-static/")
        end = time.time()
        elapsed = end - start
        MONITOR.monitor_api_response_time.set(elapsed)

        return api_response

    def set_metric_values(self, metrics):

        start = time.time()

        MONITOR.players.set(metrics["total_players"])
        MONITOR.fpl_assets.set(len(metrics["elements"]))

        self.parse_teams(metrics["teams"])
        self.parse_assets(metrics["elements"])

        end = time.time()
        elapsed = end - start

        MONITOR.monitor_working_time.set(elapsed)
        return metrics

    def parse_teams(self, teams):
        for team in teams:
            key = team["short_name"]
            MONITOR.availability.state(self.team_availability(str(team["unavailable"])))
            MONITOR.strength_attack_home.labels(key).set(team["strength_attack_home"])
            MONITOR.strength_attack_away.labels(key).set(team["strength_attack_away"])
            MONITOR.strength_defence_home.labels(key).set(team["strength_defence_home"])
            MONITOR.strength_defence_away.labels(key).set(team["strength_defence_away"])
            MONITOR.strength_overall_home.labels(key).set(team["strength_overall_home"])
            MONITOR.strength_overall_away.labels(key).set(team["strength_overall_away"])
            # MONITOR.form.labels(key).set(team["form"])
            MONITOR.strength.labels(key).set(team["strength"])
            MONITOR.position.labels(key).set(team["position"])
            MONITOR.points.labels(key).set(team["points"])
            MONITOR.played.labels(key).set(team["played"])
            MONITOR.win.labels(key).set(team["win"])
            MONITOR.loss.labels(key).set(team["loss"])
            MONITOR.draw.labels(key).set(team["draw"])

    def team_availability(self, availability):
        router = {"True": "unavailable", "False": "available"}
        return router.get(availability, "unknown")

    def parse_assets(self, assets):
        for asset in assets:
            key = asset["web_name"]
            MONITOR.ict_index.labels(key).set(asset["ict_index"])
            MONITOR.influence.labels(key).set(asset["influence"])
            MONITOR.creativity.labels(key).set(asset["creativity"])
            MONITOR.threat.labels(key).set(asset["threat"])
            MONITOR.selected_by_percent.labels(key).set(
                float(asset["selected_by_percent"])
            )
            MONITOR.form.labels(key).set(asset["form"])
            MONITOR.bonus.labels(key).set(asset["bonus"])
            MONITOR.bps.labels(key).set(asset["bps"])
