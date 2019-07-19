from os import path 

user_home = path.expanduser('~')
jarvis_config_home = user_home + '/.jarvis'
openproject_config_file = jarvis_config_home + '/creds.cfg'

statuses = [
      {
        "status": 'new',
        "_type": "Status",
        "id": 1,
        "name": "New",
        "color": "#C3FAE8",
        "_links": {
          "self": {
            "href": "/api/v3/statuses/1",
          }
        }
      },
      {
        "status": 'work',
        "_type": "Status",
        "id": 7,
        "name": "In progress",
        "color": "#66D9E8",
        "_links": {
          "status": {
            "href": "/api/v3/statuses/7",
          }
        }
      },
      {
        "status": 'done',
        "_type": "Status",
        "id": 9,
        "name": "Developed",
        "color": "#12B886",
        "_links": {
          "status": {
            "href": "/api/v3/statuses/9",
          }
        }
      },
      {
        "status": 'testing',
        "_type": "Status",
        "id": 10,
        "name": "In testing",
        "color": "#0CA678",
        "_links": {
          "status": {
            "href": "/api/v3/statuses/10",
          }
        }
      },
      {
        "status": "pass",
        "_type": "Status",
        "id": 11,
        "name": "Tested",
        "color": "#087F5B",
        "_links": {
          "status": {
            "href": "/api/v3/statuses/11",
          }
        }
      },
      {
        "status": 'fail',
        "_type": "Status",
        "id": 12,
        "name": "Test failed",
        "color": "#C92A2A",
        "_links": {
          "status": {
            "href": "/api/v3/statuses/12",
          }
        }
      },
      {
        "status": 'close',
        "_type": "Status",
        "id": 13,
        "name": "Closed",
        "color": "#DEE2E6",
        "_links": {
          "status": {
            "href": "/api/v3/statuses/13",
          }
        }
      },
      {
        "status": 'hold',
        "_type": "Status",
        "id": 14,
        "name": "On hold",
        "color": "#FFC078",
        "_links": {
          "status": {
            "href": "/api/v3/statuses/14",
          }
        }
      }
]