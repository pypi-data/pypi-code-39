VEHICLE_POSITION_1 = """
{
  "lines": [
    {
      "lineId": "1",
      "vehiclePositions": [
        {
          "directionId": "8161",
          "distanceFromPoint": 1,
          "pointId": "8152"
        },
        {
          "directionId": "8161",
          "distanceFromPoint": 0,
          "pointId": "8102"
        },
        {
          "directionId": "8731",
          "distanceFromPoint": 0,
          "pointId": "8061"
        },
        {
          "directionId": "8161",
          "distanceFromPoint": 0,
          "pointId": "8272"
        },
        {
          "directionId": "8161",
          "distanceFromPoint": 0,
          "pointId": "8733"
        },
        {
          "directionId": "8731",
          "distanceFromPoint": 0,
          "pointId": "8161"
        },
        {
          "directionId": "8731",
          "distanceFromPoint": 1,
          "pointId": "8741"
        },
        {
          "directionId": "8731",
          "distanceFromPoint": 0,
          "pointId": "8121"
        },
        {
          "directionId": "8161",
          "distanceFromPoint": 0,
          "pointId": "8032"
        }
      ]
    }
  ]
}
"""

VEHICLE_POSITION_1_5 = """
{
  "lines": [
    {
      "lineId": "1",
      "vehiclePositions": [
        {
          "directionId": "8161",
          "distanceFromPoint": 1,
          "pointId": "8152"
        },
        {
          "directionId": "8161",
          "distanceFromPoint": 1,
          "pointId": "8102"
        },
        {
          "directionId": "8731",
          "distanceFromPoint": 0,
          "pointId": "8061"
        },
        {
          "directionId": "8161",
          "distanceFromPoint": 0,
          "pointId": "8272"
        },
        {
          "directionId": "8161",
          "distanceFromPoint": 0,
          "pointId": "8733"
        },
        {
          "directionId": "8731",
          "distanceFromPoint": 1,
          "pointId": "8161"
        },
        {
          "directionId": "8161",
          "distanceFromPoint": 0,
          "pointId": "8731"
        },
        {
          "directionId": "8731",
          "distanceFromPoint": 0,
          "pointId": "8111"
        },
        {
          "directionId": "8161",
          "distanceFromPoint": 1,
          "pointId": "8032"
        }
      ]
    },
    {
      "lineId": "5",
      "vehiclePositions": [
        {
          "directionId": "8642",
          "distanceFromPoint": 0,
          "pointId": "8281"
        },
        {
          "directionId": "8262",
          "distanceFromPoint": 0,
          "pointId": "8692"
        },
        {
          "directionId": "8262",
          "distanceFromPoint": 1,
          "pointId": "8242"
        },
        {
          "directionId": "8262",
          "distanceFromPoint": 0,
          "pointId": "8052"
        },
        {
          "directionId": "8642",
          "distanceFromPoint": 0,
          "pointId": "8651"
        },
        {
          "directionId": "8642",
          "distanceFromPoint": 0,
          "pointId": "8261"
        },
        {
          "directionId": "8262",
          "distanceFromPoint": 0,
          "pointId": "8022"
        },
        {
          "directionId": "8641",
          "distanceFromPoint": 0,
          "pointId": "8701"
        },
        {
          "directionId": "8641",
          "distanceFromPoint": 0,
          "pointId": "8262"
        },
        {
          "directionId": "8262",
          "distanceFromPoint": 1,
          "pointId": "8732"
        },
        {
          "directionId": "8641",
          "distanceFromPoint": 1,
          "pointId": "8071"
        },
        {
          "directionId": "8262",
          "distanceFromPoint": 0,
          "pointId": "8642"
        }
      ]
    }
  ]
}
"""

WAITING_TIME_8301 = """
{
  "points": [
    {
      "passingTimes": [
        {
          "destination": {
            "fr": "SIMONIS",
            "nl": "SIMONIS"
          },
          "expectedArrivalTime": "2019-06-05T14:21:00+02:00",
          "lineId": "2"
        },
        {
          "destination": {
            "fr": "ROI BAUDOUIN",
            "nl": "KONING BOUDEWIJN"
          },
          "expectedArrivalTime": "2019-06-05T14:17:00+02:00",
          "lineId": "6"
        },
        {
          "destination": {
            "fr": "SIMONIS",
            "nl": "SIMONIS"
          },
          "expectedArrivalTime": "2019-06-05T14:28:00+02:00",
          "lineId": "2"
        },
        {
          "destination": {
            "fr": "ROI BAUDOUIN",
            "nl": "KONING BOUDEWIJN"
          },
          "expectedArrivalTime": "2019-06-05T14:25:00+02:00",
          "lineId": "6"
        }
      ],
      "pointId": "8301"
    }
  ]
}
"""

WAITING_TIME_8301_8302 = """
{
  "points": [
    {
      "passingTimes": [
        {
          "destination": {
            "fr": "SIMONIS",
            "nl": "SIMONIS"
          },
          "expectedArrivalTime": "2019-06-05T14:20:00+02:00",
          "lineId": "2"
        },
        {
          "destination": {
            "fr": "ROI BAUDOUIN",
            "nl": "KONING BOUDEWIJN"
          },
          "expectedArrivalTime": "2019-06-05T14:17:00+02:00",
          "lineId": "6"
        },
        {
          "destination": {
            "fr": "SIMONIS",
            "nl": "SIMONIS"
          },
          "expectedArrivalTime": "2019-06-05T14:28:00+02:00",
          "lineId": "2"
        },
        {
          "destination": {
            "fr": "ROI BAUDOUIN",
            "nl": "KONING BOUDEWIJN"
          },
          "expectedArrivalTime": "2019-06-05T14:25:00+02:00",
          "lineId": "6"
        }
      ],
      "pointId": "8301"
    },
    {
      "passingTimes": [
        {
          "destination": {
            "fr": "ELISABETH",
            "nl": "ELISABETH"
          },
          "expectedArrivalTime": "2019-06-05T14:22:00+02:00",
          "lineId": "2"
        },
        {
          "destination": {
            "fr": "ELISABETH",
            "nl": "ELISABETH"
          },
          "expectedArrivalTime": "2019-06-05T14:20:00+02:00",
          "lineId": "6"
        },
        {
          "destination": {
            "fr": "ELISABETH",
            "nl": "ELISABETH"
          },
          "expectedArrivalTime": "2019-06-05T14:30:00+02:00",
          "lineId": "2"
        },
        {
          "destination": {
            "fr": "ELISABETH",
            "nl": "ELISABETH"
          },
          "expectedArrivalTime": "2019-06-05T14:26:00+02:00",
          "lineId": "6"
        }
      ],
      "pointId": "8302"
    }
  ]
}
"""

MESSAGE_BY_LINE_12 = """
{
  "messages": [
    {
      "content": [
        {
          "text": [
            {
              "en": "Works. STOP NOT OPERATED. Bus 12-21-79 at the stop Diamant of bus 29 Hof Ten Berg, av. du Diamant 199.",
              "fr": "Travaux. ARRET NON DESSERVI. Bus 12-21-79 à l'arrêt Diamant du bus 29 Hof Ten Berg, av. du Diamant 199.",
              "nl": "Werken. HALTE NIET BEDIEND. Bus 12-21-79 aan de halte Diamant van bus 29 Hof Ten Berg, Diamantlaan 199."
            }
          ],
          "type": "Description"
        }
      ],
      "lines": [
        {
          "id": "12"
        }
      ],
      "points": [
        {
          "id": "6448"
        }
      ],
      "priority": 5,
      "type": "LongText"
    }
  ]
}
"""  # noqa: E501


MESSAGE_BY_LINE_32 = """
{
  "messages": [
    {
      "content": [
        {
          "text": [
            {
              "en": "On 8/6 6.30AM-9.30PM, fair. Tram 32-55 replaced by T-bus betw. VERBOEKHOVEN and DA VINCI.Info:stib.brussels",
              "fr": "Le 8/6 6h30-21h30, braderie. Tram 32-55 remplacé par T-bus entre VERBOEKHOVEN et DA VINCI.Info:stib.brussels",
              "nl": "Op 8/6 6.30u-21.30u, braderie. Tram 32-55 vervangen door T-bus tss VERBOEKHOVEN en DA VINCI.Info:mivb.brussels"
            }
          ],
          "type": "Description"
        }
      ],
      "lines": [
        {
          "id": "32"
        }
      ],
      "points": [
        {
          "id": "5711F"
        },
        {
          "id": "5765F"
        },
        {
          "id": "2900F"
        },
        {
          "id": "5804G"
        },
        {
          "id": "5762"
        },
        {
          "id": "1642F"
        },
        {
          "id": "5361F"
        },
        {
          "id": "5039"
        },
        {
          "id": "606"
        },
        {
          "id": "626"
        },
        {
          "id": "5714"
        },
        {
          "id": "506"
        },
        {
          "id": "2902"
        },
        {
          "id": "2901"
        },
        {
          "id": "526"
        },
        {
          "id": "5710F"
        },
        {
          "id": "5803G"
        },
        {
          "id": "5872"
        },
        {
          "id": "5867F"
        },
        {
          "id": "5712F"
        },
        {
          "id": "2903F"
        },
        {
          "id": "1643F"
        },
        {
          "id": "5362F"
        },
        {
          "id": "5041F"
        },
        {
          "id": "5805"
        },
        {
          "id": "5766"
        },
        {
          "id": "5865"
        },
        {
          "id": "5866"
        },
        {
          "id": "516"
        },
        {
          "id": "5801"
        },
        {
          "id": "5868"
        },
        {
          "id": "5802"
        },
        {
          "id": "616"
        },
        {
          "id": "636"
        }
      ],
      "priority": 5,
      "type": "LongText"
    }
  ]
}
"""  # noqa: E501


MESSAGE_BY_LINE_12_17 = """
{
  "messages": [
    {
      "content": [
        {
          "text": [
            {
              "en": "Works. STOP NOT OPERATED. Bus 12-21-79 at the stop Diamant of bus 29 Hof Ten Berg, av. du Diamant 199.",
              "fr": "Travaux. ARRET NON DESSERVI. Bus 12-21-79 à l'arrêt Diamant du bus 29 Hof Ten Berg, av. du Diamant 199.",
              "nl": "Werken. HALTE NIET BEDIEND. Bus 12-21-79 aan de halte Diamant van bus 29 Hof Ten Berg, Diamantlaan 199."
            }
          ],
          "type": "Description"
        }
      ],
      "lines": [
        {
          "id": "12"
        }
      ],
      "points": [
        {
          "id": "6448"
        }
      ],
      "priority": 5,
      "type": "LongText"
    },
    {
      "content": [
        {
          "text": [
            {
              "en": "As from 25/3, works. STOP NOT OPERATED. Temporary stop moved +- 100m backwards, av. du Martin Pêcheur 23.",
              "fr": "Dès le 25/3, travaux. ARRET NON DESSERVI. Arrêt provisoire reculé de +-100m, av. du Martin Pêcheur 23.",
              "nl": "Vanaf 25/3, werken. HALTE NIET BEDIEND. Tijdelijke halte +-100m naar achter verplaatst, IJsvogellaan 23."
            }
          ],
          "type": "Description"
        }
      ],
      "lines": [
        {
          "id": "17"
        }
      ],
      "points": [
        {
          "id": "4294"
        }
      ],
      "priority": 5,
      "type": "LongText"
    }
  ]
}
"""  # noqa: E501

MESSAGE_BY_LINE_12_32 = """
{
  "messages": [
    {
      "content": [
        {
          "text": [
            {
              "en": "Works. STOP NOT OPERATED. Bus 12-21-79 at the stop Diamant of bus 29 Hof Ten Berg, av. du Diamant 199.",
              "fr": "Travaux. ARRET NON DESSERVI. Bus 12-21-79 à l'arrêt Diamant du bus 29 Hof Ten Berg, av. du Diamant 199.",
              "nl": "Werken. HALTE NIET BEDIEND. Bus 12-21-79 aan de halte Diamant van bus 29 Hof Ten Berg, Diamantlaan 199."
            }
          ],
          "type": "Description"
        }
      ],
      "lines": [
        {
          "id": "12"
        }
      ],
      "points": [
        {
          "id": "6448"
        }
      ],
      "priority": 5,
      "type": "LongText"
    },
    {
      "content": [
        {
          "text": [
            {
              "en": "On 8/6 6.30AM-9.30PM, fair. Tram 32-55 replaced by T-bus betw. VERBOEKHOVEN and DA VINCI.Info:stib.brussels",
              "fr": "Le 8/6 6h30-21h30, braderie. Tram 32-55 remplacé par T-bus entre VERBOEKHOVEN et DA VINCI.Info:stib.brussels",
              "nl": "Op 8/6 6.30u-21.30u, braderie. Tram 32-55 vervangen door T-bus tss VERBOEKHOVEN en DA VINCI.Info:mivb.brussels"
            }
          ],
          "type": "Description"
        }
      ],
      "lines": [
        {
          "id": "32"
        }
      ],
      "points": [
        {
          "id": "5711F"
        },
        {
          "id": "5765F"
        },
        {
          "id": "2900F"
        },
        {
          "id": "5804G"
        },
        {
          "id": "5762"
        },
        {
          "id": "1642F"
        },
        {
          "id": "5361F"
        },
        {
          "id": "5039"
        },
        {
          "id": "606"
        },
        {
          "id": "626"
        },
        {
          "id": "5714"
        },
        {
          "id": "506"
        },
        {
          "id": "2902"
        },
        {
          "id": "2901"
        },
        {
          "id": "526"
        },
        {
          "id": "5710F"
        },
        {
          "id": "5803G"
        },
        {
          "id": "5872"
        },
        {
          "id": "5867F"
        },
        {
          "id": "5712F"
        },
        {
          "id": "2903F"
        },
        {
          "id": "1643F"
        },
        {
          "id": "5362F"
        },
        {
          "id": "5041F"
        },
        {
          "id": "5805"
        },
        {
          "id": "5766"
        },
        {
          "id": "5865"
        },
        {
          "id": "5866"
        },
        {
          "id": "516"
        },
        {
          "id": "5801"
        },
        {
          "id": "5868"
        },
        {
          "id": "5802"
        },
        {
          "id": "616"
        },
        {
          "id": "636"
        }
      ],
      "priority": 5,
      "type": "LongText"
    }
  ]
}
"""  # noqa: E501

STOPS_BY_LINE_1 = """
{
  "lines": [
    {
      "destination": {
        "fr": "STOCKEL",
        "nl": "STOKKEL"
      },
      "direction": "Suburb",
      "lineId": "1",
      "points": [
        {
          "id": "8733",
          "order": 1
        },
        {
          "id": "8742",
          "order": 2
        },
        {
          "id": "8292",
          "order": 3
        },
        {
          "id": "8282",
          "order": 4
        },
        {
          "id": "8272",
          "order": 5
        },
        {
          "id": "8012",
          "order": 6
        },
        {
          "id": "8022",
          "order": 7
        },
        {
          "id": "8032",
          "order": 8
        },
        {
          "id": "8042",
          "order": 9
        },
        {
          "id": "8052",
          "order": 10
        },
        {
          "id": "8062",
          "order": 11
        },
        {
          "id": "8072",
          "order": 12
        },
        {
          "id": "8082",
          "order": 13
        },
        {
          "id": "8092",
          "order": 14
        },
        {
          "id": "8102",
          "order": 15
        },
        {
          "id": "8112",
          "order": 16
        },
        {
          "id": "8122",
          "order": 17
        },
        {
          "id": "8132",
          "order": 18
        },
        {
          "id": "8142",
          "order": 19
        },
        {
          "id": "8152",
          "order": 20
        },
        {
          "id": "8161",
          "order": 21
        }
      ]
    },
    {
      "destination": {
        "fr": "GARE DE L'OUEST",
        "nl": "WESTSTATION"
      },
      "direction": "City",
      "lineId": "1",
      "points": [
        {
          "id": "8161",
          "order": 1
        },
        {
          "id": "8162",
          "order": 2
        },
        {
          "id": "8151",
          "order": 3
        },
        {
          "id": "8141",
          "order": 4
        },
        {
          "id": "8131",
          "order": 5
        },
        {
          "id": "8121",
          "order": 6
        },
        {
          "id": "8111",
          "order": 7
        },
        {
          "id": "8101",
          "order": 8
        },
        {
          "id": "8091",
          "order": 9
        },
        {
          "id": "8081",
          "order": 10
        },
        {
          "id": "8071",
          "order": 11
        },
        {
          "id": "8061",
          "order": 12
        },
        {
          "id": "8051",
          "order": 13
        },
        {
          "id": "8041",
          "order": 14
        },
        {
          "id": "8031",
          "order": 15
        },
        {
          "id": "8021",
          "order": 16
        },
        {
          "id": "8011",
          "order": 17
        },
        {
          "id": "8271",
          "order": 18
        },
        {
          "id": "8281",
          "order": 19
        },
        {
          "id": "8291",
          "order": 20
        },
        {
          "id": "8741",
          "order": 21
        },
        {
          "id": "8731",
          "order": 22
        }
      ]
    }
  ]
}
"""

STOPS_BY_LINE_1_5 = """
{
  "lines": [
    {
      "destination": {
        "fr": "STOCKEL",
        "nl": "STOKKEL"
      },
      "direction": "Suburb",
      "lineId": "1",
      "points": [
        {
          "id": "8733",
          "order": 1
        },
        {
          "id": "8742",
          "order": 2
        },
        {
          "id": "8292",
          "order": 3
        },
        {
          "id": "8282",
          "order": 4
        },
        {
          "id": "8272",
          "order": 5
        },
        {
          "id": "8012",
          "order": 6
        },
        {
          "id": "8022",
          "order": 7
        },
        {
          "id": "8032",
          "order": 8
        },
        {
          "id": "8042",
          "order": 9
        },
        {
          "id": "8052",
          "order": 10
        },
        {
          "id": "8062",
          "order": 11
        },
        {
          "id": "8072",
          "order": 12
        },
        {
          "id": "8082",
          "order": 13
        },
        {
          "id": "8092",
          "order": 14
        },
        {
          "id": "8102",
          "order": 15
        },
        {
          "id": "8112",
          "order": 16
        },
        {
          "id": "8122",
          "order": 17
        },
        {
          "id": "8132",
          "order": 18
        },
        {
          "id": "8142",
          "order": 19
        },
        {
          "id": "8152",
          "order": 20
        },
        {
          "id": "8161",
          "order": 21
        }
      ]
    },
    {
      "destination": {
        "fr": "GARE DE L'OUEST",
        "nl": "WESTSTATION"
      },
      "direction": "City",
      "lineId": "1",
      "points": [
        {
          "id": "8161",
          "order": 1
        },
        {
          "id": "8162",
          "order": 2
        },
        {
          "id": "8151",
          "order": 3
        },
        {
          "id": "8141",
          "order": 4
        },
        {
          "id": "8131",
          "order": 5
        },
        {
          "id": "8121",
          "order": 6
        },
        {
          "id": "8111",
          "order": 7
        },
        {
          "id": "8101",
          "order": 8
        },
        {
          "id": "8091",
          "order": 9
        },
        {
          "id": "8081",
          "order": 10
        },
        {
          "id": "8071",
          "order": 11
        },
        {
          "id": "8061",
          "order": 12
        },
        {
          "id": "8051",
          "order": 13
        },
        {
          "id": "8041",
          "order": 14
        },
        {
          "id": "8031",
          "order": 15
        },
        {
          "id": "8021",
          "order": 16
        },
        {
          "id": "8011",
          "order": 17
        },
        {
          "id": "8271",
          "order": 18
        },
        {
          "id": "8281",
          "order": 19
        },
        {
          "id": "8291",
          "order": 20
        },
        {
          "id": "8741",
          "order": 21
        },
        {
          "id": "8731",
          "order": 22
        }
      ]
    },
    {
      "destination": {
        "fr": "HERRMANN-DEBROUX",
        "nl": "HERRMANN-DEBROUX"
      },
      "direction": "Suburb",
      "lineId": "5",
      "points": [
        {
          "id": "8642",
          "order": 1
        },
        {
          "id": "8641",
          "order": 2
        },
        {
          "id": "8652",
          "order": 3
        },
        {
          "id": "8662",
          "order": 4
        },
        {
          "id": "8672",
          "order": 5
        },
        {
          "id": "8682",
          "order": 6
        },
        {
          "id": "8692",
          "order": 7
        },
        {
          "id": "8702",
          "order": 8
        },
        {
          "id": "8712",
          "order": 9
        },
        {
          "id": "8722",
          "order": 10
        },
        {
          "id": "8732",
          "order": 11
        },
        {
          "id": "8742",
          "order": 12
        },
        {
          "id": "8292",
          "order": 13
        },
        {
          "id": "8282",
          "order": 14
        },
        {
          "id": "8272",
          "order": 15
        },
        {
          "id": "8012",
          "order": 16
        },
        {
          "id": "8022",
          "order": 17
        },
        {
          "id": "8032",
          "order": 18
        },
        {
          "id": "8042",
          "order": 19
        },
        {
          "id": "8052",
          "order": 20
        },
        {
          "id": "8062",
          "order": 21
        },
        {
          "id": "8072",
          "order": 22
        },
        {
          "id": "8202",
          "order": 23
        },
        {
          "id": "8212",
          "order": 24
        },
        {
          "id": "8222",
          "order": 25
        },
        {
          "id": "8232",
          "order": 26
        },
        {
          "id": "8242",
          "order": 27
        },
        {
          "id": "8252",
          "order": 28
        },
        {
          "id": "8262",
          "order": 29
        }
      ]
    },
    {
      "destination": {
        "fr": "ERASME",
        "nl": "ERASMUS"
      },
      "direction": "City",
      "lineId": "5",
      "points": [
        {
          "id": "8261",
          "order": 1
        },
        {
          "id": "8262",
          "order": 2
        },
        {
          "id": "8251",
          "order": 3
        },
        {
          "id": "8241",
          "order": 4
        },
        {
          "id": "8231",
          "order": 5
        },
        {
          "id": "8221",
          "order": 6
        },
        {
          "id": "8211",
          "order": 7
        },
        {
          "id": "8201",
          "order": 8
        },
        {
          "id": "8071",
          "order": 9
        },
        {
          "id": "8061",
          "order": 10
        },
        {
          "id": "8051",
          "order": 11
        },
        {
          "id": "8041",
          "order": 12
        },
        {
          "id": "8031",
          "order": 13
        },
        {
          "id": "8021",
          "order": 14
        },
        {
          "id": "8011",
          "order": 15
        },
        {
          "id": "8271",
          "order": 16
        },
        {
          "id": "8281",
          "order": 17
        },
        {
          "id": "8291",
          "order": 18
        },
        {
          "id": "8741",
          "order": 19
        },
        {
          "id": "8731",
          "order": 20
        },
        {
          "id": "8721",
          "order": 21
        },
        {
          "id": "8711",
          "order": 22
        },
        {
          "id": "8701",
          "order": 23
        },
        {
          "id": "8691",
          "order": 24
        },
        {
          "id": "8681",
          "order": 25
        },
        {
          "id": "8671",
          "order": 26
        },
        {
          "id": "8661",
          "order": 27
        },
        {
          "id": "8651",
          "order": 28
        },
        {
          "id": "8641",
          "order": 29
        }
      ]
    }
  ]
}
"""

POINT_DETAIL_8301 = """
{
  "points": [
    {
      "gpsCoordinates": {
        "latitude": 50.840813,
        "longitude": 4.366354
      },
      "id": "8301",
      "name": {
        "fr": "TRONE",
        "nl": "TROON"
      }
    }
  ]
}
"""
POINT_DETAIL_6448 = """
{
  "points": [
    {
      "gpsCoordinates": {
        "latitude": 50.84953,
        "longitude": 4.402407
      },
      "id": "6448",
      "name": {
        "fr": "DIAMANT",
        "nl": "DIAMANT"
      }
    }
  ]
}
"""
POINT_DETAIL_28 = """
{
  "points": [
    {
      "gpsCoordinates": {
        "latitude": 50.816285,
        "longitude": 4.405107
      },
      "id": "28",
      "name": {
        "fr": "DEPOT DELTA",
        "nl": "REMISE DELTA"
      }
    }
  ]
}
"""

POINT_DETAIL_8301_0470F = """
{
  "points": [
    {
      "gpsCoordinates": {
        "latitude": 50.840813,
        "longitude": 4.366354
      },
      "id": "8301",
      "name": {
        "fr": "TRONE",
        "nl": "TROON"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.863666,
        "longitude": 4.329612
      },
      "id": "470F",
      "name": {
        "fr": "SIMONIS",
        "nl": "SIMONIS"
      }
    }
  ]
}
"""

POINT_DETAIL_10_ARGS = """
{
  "points": [
    {
      "gpsCoordinates": {
        "latitude": 50.830699,
        "longitude": 4.333
      },
      "id": "1",
      "name": {
        "fr": "DEPOT AVENUE DU ROI",
        "nl": "REMISE KONINGSLAAN"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.848279,
        "longitude": 4.323813
      },
      "id": "2",
      "name": {
        "fr": "DEPOT MOLENBEEK TRAM",
        "nl": "REMISE MOLENBEEK TRAM"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.885107,
        "longitude": 4.41319
      },
      "id": "3",
      "name": {
        "fr": "DEPOT HAREN TRAM",
        "nl": "REMISE HAREN TRAM"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.819887,
        "longitude": 4.378374
      },
      "id": "4",
      "name": {
        "fr": "DEPOT IXELLES",
        "nl": "REMISE ELSENE"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.848313,
        "longitude": 4.32195
      },
      "id": "5",
      "name": {
        "fr": "DEPOT MOLENBEEK",
        "nl": "REMISE MOLENBEEK"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.865231,
        "longitude": 4.373923
      },
      "id": "6",
      "name": {
        "fr": "DEPOT SCHAERBEEK",
        "nl": "REMISE SCHAARBEEK"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.831547,
        "longitude": 4.434076
      },
      "id": "7",
      "name": {
        "fr": "DEPOT WOLUWE",
        "nl": "REMISE WOLUWE"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.883723,
        "longitude": 4.412749
      },
      "id": "8",
      "name": {
        "fr": "DEPOT HAREN",
        "nl": "REMISE HAREN"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.816286,
        "longitude": 4.405107
      },
      "id": "9",
      "name": {
        "fr": "DEPOT DELTA",
        "nl": "REMISE DELTA"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.798578,
        "longitude": 4.314329
      },
      "id": "15",
      "name": {
        "fr": "DEPOT MARCONI",
        "nl": "REMISE MARCONI"
      }
    }
  ]
}
"""

POINT_DETAIL_10_ARGS_5711F_TO_626 = """
{
  "points": [
    {
      "gpsCoordinates": {
        "latitude": 50.869258,
        "longitude": 4.370997
      },
      "id": "5711F",
      "name": {
        "fr": "PAVILLON",
        "nl": "PAVILJOEN"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.869555,
        "longitude": 4.371338
      },
      "id": "5765F",
      "name": {
        "fr": "PAVILLON",
        "nl": "PAVILJOEN"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.879051,
        "longitude": 4.403892
      },
      "id": "2900F",
      "name": {
        "fr": "FONSON",
        "nl": "FONSON"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.871653,
        "longitude": 4.384367
      },
      "id": "5804G",
      "name": {
        "fr": "FOYER SCHAERBEEK.",
        "nl": "SCHAARBEEK. HAARD"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.865689,
        "longitude": 4.364534
      },
      "id": "5762",
      "name": {
        "fr": "THOMAS",
        "nl": "THOMAS"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.865384,
        "longitude": 4.367758
      },
      "id": "1642F",
      "name": {
        "fr": "LIEDTS",
        "nl": "LIEDTS"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.878456,
        "longitude": 4.409817
      },
      "id": "5361F",
      "name": {
        "fr": "BORDET STATION",
        "nl": "BORDET STATION"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.876747,
        "longitude": 4.412529
      },
      "id": "5039",
      "name": {
        "fr": "DA VINCI",
        "nl": "DA VINCI"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.848086,
        "longitude": 4.349455
      },
      "id": "606",
      "name": {
        "fr": "BOURSE",
        "nl": "BEURS"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.840399,
        "longitude": 4.341408
      },
      "id": "626",
      "name": {
        "fr": "LEMONNIER",
        "nl": "LEMONNIER"
      }
    }
  ]
}
"""

POINT_DETAIL_10_ARGS_5714_TO_5712F = """
{
  "points": [
    {
      "gpsCoordinates": {
        "latitude": 50.865348,
        "longitude": 4.362872
      },
      "id": "5714",
      "name": {
        "fr": "THOMAS",
        "nl": "THOMAS"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.851746,
        "longitude": 4.353415
      },
      "id": "506",
      "name": {
        "fr": "DE BROUCKERE",
        "nl": "DE BROUCKERE"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.880012,
        "longitude": 4.407132
      },
      "id": "2902",
      "name": {
        "fr": "VAN CUTSEM",
        "nl": "VAN CUTSEM"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.880138,
        "longitude": 4.407488
      },
      "id": "2901",
      "name": {
        "fr": "VAN CUTSEM",
        "nl": "VAN CUTSEM"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.860718,
        "longitude": 4.3605
      },
      "id": "526",
      "name": {
        "fr": "GARE DU NORD",
        "nl": "NOORDSTATION"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.871388,
        "longitude": 4.375288
      },
      "id": "5710F",
      "name": {
        "fr": "VERBOEKHOVEN",
        "nl": "VERBOEKHOVEN"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.873428,
        "longitude": 4.386924
      },
      "id": "5803G",
      "name": {
        "fr": "HELMET",
        "nl": "HELMET"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.876949,
        "longitude": 4.400835
      },
      "id": "5872",
      "name": {
        "fr": "PAIX",
        "nl": "VREDE"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.874138,
        "longitude": 4.38772
      },
      "id": "5867F",
      "name": {
        "fr": "HELMET",
        "nl": "HELMET"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.866633,
        "longitude": 4.368738
      },
      "id": "5712F",
      "name": {
        "fr": "RUBENS",
        "nl": "RUBENS"
      }
    }
  ]
}
"""

POINT_DETAIL_10_ARGS_2903F_TO_5801 = """
{
  "points": [
    {
      "gpsCoordinates": {
        "latitude": 50.878817,
        "longitude": 4.403664
      },
      "id": "2903F",
      "name": {
        "fr": "FONSON",
        "nl": "FONSON"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.864152,
        "longitude": 4.366338
      },
      "id": "1643F",
      "name": {
        "fr": "LIEDTS",
        "nl": "LIEDTS"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.878141,
        "longitude": 4.409916
      },
      "id": "5362F",
      "name": {
        "fr": "BORDET STATION",
        "nl": "BORDET STATION"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.876787,
        "longitude": 4.411827
      },
      "id": "5041F",
      "name": {
        "fr": "DA VINCI",
        "nl": "DA VINCI"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.870156,
        "longitude": 4.382107
      },
      "id": "5805",
      "name": {
        "fr": "WAELHEM",
        "nl": "WAELHEM"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.871128,
        "longitude": 4.376282
      },
      "id": "5766",
      "name": {
        "fr": "VERBOEKHOVEN",
        "nl": "VERBOEKHOVEN"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.870057,
        "longitude": 4.381496
      },
      "id": "5865",
      "name": {
        "fr": "WAELHEM",
        "nl": "WAELHEM"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.871927,
        "longitude": 4.384977
      },
      "id": "5866",
      "name": {
        "fr": "FOYER SCHAERBEEK.",
        "nl": "SCHAARBEEK. HAARD"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.855933,
        "longitude": 4.358494
      },
      "id": "516",
      "name": {
        "fr": "ROGIER",
        "nl": "ROGIER"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.876904,
        "longitude": 4.400878
      },
      "id": "5801",
      "name": {
        "fr": "PAIX",
        "nl": "VREDE"
      }
    }
  ]
}
"""

POINT_DETAIL_4_ARGS_5868_TO_636 = """
{
  "points": [
    {
      "gpsCoordinates": {
        "latitude": 50.875809,
        "longitude": 4.392352
      },
      "id": "5868",
      "name": {
        "fr": "TILLEUL",
        "nl": "LINDE"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.875935,
        "longitude": 4.392836
      },
      "id": "5802",
      "name": {
        "fr": "TILLEUL",
        "nl": "LINDE"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.84449,
        "longitude": 4.345736
      },
      "id": "616",
      "name": {
        "fr": "ANNEESSENS",
        "nl": "ANNEESSENS"
      }
    },
    {
      "gpsCoordinates": {
        "latitude": 50.836811,
        "longitude": 4.337407
      },
      "id": "636",
      "name": {
        "fr": "GARE DU MIDI",
        "nl": "ZUIDSTATION"
      }
    }
  ]
}
"""

HEADER_FIELD = "Authorization"
HEADER_VALUE = "Bearer 2133c416f69f5acaa67351501153d892"


class Response:
    def __init__(self, request, headers):
        if not (HEADER_FIELD in headers and headers[HEADER_FIELD] == HEADER_VALUE):
            self.text = ""
            self.status = 401
        elif request not in REQUESTS.keys():
            self.text = ""
            self.status = 403
        elif REQUESTS[request] == 404:
            self.text = "Not Found"
            self.status = 404
        else:
            self.text = REQUESTS[request]
            self.status = 200


VEHICLE_POSITION_1_URL = "/OperationMonitoring/4.0/VehiclePositionByLine/1"
VEHICLE_POSITION_1_5_URL = "/OperationMonitoring/4.0/VehiclePositionByLine/1,5"
WAITING_TIME_8301_URL = "/OperationMonitoring/4.0/PassingTimeByPoint/8301"
WAITING_TIME_8301_8302_URL = "/OperationMonitoring/4.0/PassingTimeByPoint/8301,8302"
MESSAGE_BY_LINE_12_URL = "/OperationMonitoring/4.0/MessageByLine/12"
MESSAGE_BY_LINE_32_URL = "/OperationMonitoring/4.0/MessageByLine/32"
MESSAGE_BY_LINE_12_32_URL = "/OperationMonitoring/4.0/MessageByLine/12,32"
MESSAGE_BY_LINE_12_17_URL = "/OperationMonitoring/4.0/MessageByLine/12,17"
STOPS_BY_LINE_1_URL = "/NetworkDescription/1.0/PointByLine/1"
STOPS_BY_LINE_1_5_URL = "/NetworkDescription/1.0/PointByLine/1,5"
POINT_DETAIL_8301_URL = "/NetworkDescription/1.0/PointDetail/8301"
POINT_DETAIL_6448_URL = "/NetworkDescription/1.0/PointDetail/6448"
POINT_DETAIL_28_URL = "/NetworkDescription/1.0/PointDetail/28"
POINT_DETAIL_8301_0470F_URL = "/NetworkDescription/1.0/PointDetail/8301,0470F"
POINT_DETAIL_10_ARGS_URL = "/NetworkDescription/1.0/PointDetail/1,2,3,4,5,6,7,8,9,15"
POINT_DETAIL_10_ARGS_5711F_TO_626_URL = (
    "/NetworkDescription/1.0/PointDetail/"
    "5711F,5765F,2900F,5804G,5762,1642F,5361F,5039,606,626"
)
POINT_DETAIL_10_ARGS_5714_TO_5712F_URL = (
    "/NetworkDescription/1.0/PointDetail/"
    "5714,506,2902,2901,526,5710F,5803G,5872,5867F,5712F"
)
POINT_DETAIL_10_ARGS_2903F_TO_5801_URL = (
    "/NetworkDescription/1.0/PointDetail/"
    "2903F,1643F,5362F,5041F,5805,5766,5865,5866,516,5801"
)
POINT_DETAIL_4_ARGS_5868_TO_636_URL = (
    "/NetworkDescription/1.0/PointDetail/5868,5802,616,636"
)
SERVER_WRONG_DATA = "/NetworkDescription/1.0/PointDetail/123456"
SERVER_404_ERROR = "/NetworkDescription/1.0/PointDetail/1234567"

REQUESTS = {
    VEHICLE_POSITION_1_URL: VEHICLE_POSITION_1,
    VEHICLE_POSITION_1_5_URL: VEHICLE_POSITION_1_5,
    WAITING_TIME_8301_URL: WAITING_TIME_8301,
    WAITING_TIME_8301_8302_URL: WAITING_TIME_8301_8302,
    MESSAGE_BY_LINE_12_URL: MESSAGE_BY_LINE_12,
    MESSAGE_BY_LINE_32_URL: MESSAGE_BY_LINE_32,
    MESSAGE_BY_LINE_12_32_URL: MESSAGE_BY_LINE_12_32,
    MESSAGE_BY_LINE_12_17_URL: MESSAGE_BY_LINE_12_17,
    STOPS_BY_LINE_1_URL: STOPS_BY_LINE_1,
    STOPS_BY_LINE_1_5_URL: STOPS_BY_LINE_1_5,
    POINT_DETAIL_8301_URL: POINT_DETAIL_8301,
    POINT_DETAIL_6448_URL: POINT_DETAIL_6448,
    POINT_DETAIL_28_URL: POINT_DETAIL_28,
    POINT_DETAIL_8301_0470F_URL: POINT_DETAIL_8301_0470F,
    POINT_DETAIL_10_ARGS_URL: POINT_DETAIL_10_ARGS,
    POINT_DETAIL_10_ARGS_5711F_TO_626_URL: POINT_DETAIL_10_ARGS_5711F_TO_626,
    POINT_DETAIL_10_ARGS_5714_TO_5712F_URL: POINT_DETAIL_10_ARGS_5714_TO_5712F,
    POINT_DETAIL_10_ARGS_2903F_TO_5801_URL: POINT_DETAIL_10_ARGS_2903F_TO_5801,
    POINT_DETAIL_4_ARGS_5868_TO_636_URL: POINT_DETAIL_4_ARGS_5868_TO_636,
    SERVER_WRONG_DATA: "some wrong data",
    SERVER_404_ERROR: 404,
}
