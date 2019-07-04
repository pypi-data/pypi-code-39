#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time


url = "https://apiv2.dance4water.org/api"
dance_url = "https://sqlitev2.dance4water.org/resultsdb/"


def db_name(simulation_id):
    return '/mnt/s3/dynamind/' + str(simulation_id) + '_export_v2_1.sqlite'


def run_query(token, scenario_id, query):
    """
    Run a query on the scenario spatialite database. The database supports SQLite and Spatialite commands
    Only read access is supported! To find out which data are stored in the database read the dynamind_table_definitions

    :param token: Access token
    :param scenario_id: scenario id
    :param query: SQL query
    :type token: str
    :type scenario_id: int
    :type query str
    :return: query result
    :rtype: dict
    """

    simulation_id = get_database_id(token, scenario_id)

    data = {'db_name': db_name(simulation_id),
            'query': query}
    r = requests.post(dance_url, data=data)
    if r.status_code == 200:
        result = json.loads(r.json())
        return result
    raise Exception(f"Unable to run query {r.status_code}")


def add_node(token, node_data):
    headers = {"Authorization": "Bearer " + token}
    return requests.post(url + "/sm_node", headers=headers, json=node_data)


def add_model(token, name, src):
    headers = {"Authorization": "Bearer " + token}
    return requests.post(url + "/models", headers=headers, json={"name": name, "model_src": src})

def get_models(token):
    headers = {"Authorization": "Bearer " + token}
    return requests.get(url + "/models/", headers=headers)

def login(username, password):
    """
    Get access token

    :param username: registered user name (email address)
    :param password: top secret password
    :return: access token
    """
    counter = 0
    while True:
        r = requests.post(url + "/user/login/", json={'username': username,
                                                      'password': password})
        counter += 1
        if r.status_code == 200:
            return r.json()["access_token"]
        if counter > 4:
            raise Exception(f"Unable to login status {r.status_code}")

        else:
            time.sleep(2)

def get_database_id(token, scenario_id):
    """
    Returns database ID to run data analysis

    :param token: access token
    :param scenario_1_id: scenario id
    :return: data base id needed for query
    """
    r = get_simulations(token, scenario_id)

    sims = r.json()

    for s in sims["simulations"]:
        sim = json.loads(s)
        if sim["simulation_type"] == "PERFORMANCE_ASSESSMENT":
            return sim["id"]



def create_project(token):
    """
    Creates a new project

    :param token: Access token
    :type token: str
    :return: project id
    :rtype: int
    """

    headers = {"Authorization": "Bearer " + token}
    r = requests.post(url + "/projects", headers=headers)

    if r.status_code == 200:
        return r.json()["id"]

    raise Exception(f"Creation of project failed {r.status_code}")


def get_project(token, project):
    headers = {"Authorization": "Bearer " + token}
    return requests.get(url + "/projects/" + str(project), headers=headers)


def get_projects(token):
    headers = {"Authorization": "Bearer " + token}
    return requests.get(url + "/projects/", headers=headers)


def update_project(token, project, data):
    headers = {"Authorization": "Bearer " + token}
    return requests.put(url + "/projects/" + str(project), headers=headers, json=data)

def get_assessment_models(token):
    headers = {"Authorization": "Bearer " + token}
    return requests.get(url + "/assessment_models", headers=headers)


def get_assessment_model(token, model_name):
    """
    Returns assessment model id

    :param token: Access token
    :param model_name: Model Name. Currently supported are Land Surface Temperature and Target
    :type token: str
    :type model_name: str
    :return: model_id
    :rtype: int
    """
    headers = {"Authorization": "Bearer " + token}
    r = requests.get(url + "/assessment_models", headers=headers)

    if not r.status_code == 200:
        raise Exception(f"Could not get assessment model {r.status_code}")

    models = r.json()["assessment_models"]
    model_id = None

    for model in models:
        if model["name"] == model_name:
            model_id = model["id"]
            break

    if model_id is None:
        raise Exception(f"Could not find ' {model_name}")

    return model_id

def set_project_assessment_models(token, project, models):
    headers = {"Authorization": "Bearer " + token}
    return requests.put(url + "/projects/" + str(project) + "/models", headers=headers, json=models)


def create_scenario(token, project, parent, name="initialised model"):
    """
    Creates a new scenario. The provides the shell for the new scenarios. Scenario are derived from the base line
    or any other scenario in the project. To modify the environment workflow may be defined and executed.

    :param token: Access token
    :param project: project id
    :param parent: parent scenario id
    :param name: name of scenario
    :type str
    :type int
    :type int
    :type str
    :return: scenario id
    ":rtype: int
    """
    data = {"project_id": project, "name": name}
    if parent is not None:
        data["parent"] = parent

    headers = {"Authorization": "Bearer " + token}
    r = requests.post(url + "/scenario/", headers=headers, json=data)

    if r.status_code == 200:
        return r.json()["id"]

    raise Exception(f"Unable to create scenario {r.status_code}")


def set_scenario_workflow(token, scenario_id, node_data):
    """
    Set the workflow for a scenario. The workflow is defined by a series of nodes defined by the node_data
    The node_data have following structure

    .. code-block::

        [{
           name: node_id,
           area: geojson_id,
           parameters: {

            parameter.value = 1,
            paramter2.value = 2,

           }
        },
        ...
        ]

    The nodes in the workflow are executed as defined in the data structure

    :param token: Access token
    :param scenario_id: scenario id
    :param node_data: node data see above
    :type token: str
    :type scenario_id: int
    :type node_data: list

    """

    headers = {"Authorization": "Bearer " + token}
    return requests.post(url + "/scenario/" + str(scenario_id) + "/nodes", headers=headers, json=node_data)


def get_scenario_workflow_nodes(token):

    headers = {"Authorization": "Bearer " + token}
    return requests.get(url + "/sm_node/", headers=headers)


def upload_geojson(token, geojson, project_id):
    """
    Upload a geojson file and return id

    :param token: Assess token
    :param geojson: geojson file
    :param project_id: project the node will be assigned to
    :type token: str
    :type geojson: str
    :type project_id: str
    :return: geojson id
    :rtype: int
    """
    headers = {"Authorization": "Bearer " + token}

    if 'name' in geojson: del geojson['name']

    r = requests.post(url + "/geojson/", headers=headers,
                         json={"project_id": project_id, "geojson": geojson, "name": "casestudyarea"})

    if r.status_code == 200:
        return r.json()["id"]

    raise Exception(f"Unable to upload file {r.status_code}")


def get_region(token, region_name):
    """
    Returns region currently supported is Melbourne

    :param token: Assess token
    :param region:region id
    :return: region id
    """

    headers = {"Authorization": "Bearer " + token}
    r = requests.get(url + "/regions/", headers=headers)
    if not r.status_code == 200:
        raise Exception(f"Unable to get region {r.status_code}")
    regions = r.json()
    melbourne_region_id = None
    for region in regions:
        if region["name"].lower() == region_name:
            melbourne_region_id = region["id"]
            break

    if melbourne_region_id is None:
        raise Exception(f"Could not find ' {region_name}")

    return melbourne_region_id

def get_regions(token):
    headers = {"Authorization": "Bearer " + token}
    return requests.get(url + "/regions/", headers=headers)


def execute_scenario(token, scenario):
    headers = {"Authorization": "Bearer " + token}
    return requests.post(url + "/scenario/" + str(scenario) + "/execute", headers=headers)


def get_geojsons(token, project):
    headers = {"Authorization": "Bearer " + token}
    return requests.get(url + "/geojson/" + str(project), headers=headers)


def check_status(token, scenario):
    """
    Return status of current simulation.

    returns:

    .. code-block::

        {
           status: status code (int),
           status_text: status description
        }

        // CREATED = 1
        // BASE_IN_QUEUE = 2
        // BASE_RUNNING = 3
        // BASE_COMPLETE = 4
        // PA_IN_QUEUE = 5
        // PA_RUNNING = 6
        // PA_COMPLETE = 7
        // COMPLETE = 8

    :param token: Access token
    :param scenario: scenario id
    :type token: str
    :type scenario: int
    :return: scenario status
    :rtype: dict

    """
    headers = {"Authorization": "Bearer " + token}
    r= requests.get(url + "/scenario/" + str(scenario) + "/status", headers=headers)
    if r.status_code != 200:
        raise Exception(f"Unable to get status {r.status_code}")
    return r.json()


def get_scenario(token, scenario):
    headers = {"Authorization": "Bearer " + token}
    return requests.get(url + "/scenario/" + str(scenario), headers=headers)


def get_simulations(token, scenario):
    headers = {"Authorization": "Bearer " + token}
    return requests.get(url + "/scenario/" + str(scenario) + "/simulations", headers=headers)


def load_model(name, filename):
    """
    Uploads a new model to the server

    :param name: model name
    :param filename: dynamind file
    :type str
    :type str
    :return: model_id
    :rtype: int
    """
    token = login("admin@danceplatform.org", "password")

    with open(filename, 'r') as file:
        data = file.read().replace('\n', '')

    r = add_model(token, name, data)

    model_id = r.json()["model_id"]

    return model_id


def show_node_versions(token, node_id):
    headers = {"Authorization": "Bearer " + token}
    return requests.get(url + "/sm_node/" + str(node_id), headers=headers)


def add_description(filename, model_id = None):
    token = login("admin@danceplatform.org", "password")

    with open(filename) as json_file:
        node_data = json.load(json_file)

    if model_id is not None:
        node_data["models"][0]["id"] = model_id
    add_node(token, node_data)


def get_baseline(token, project_id):
    """
    Get a projects baseline scenario id

    :param token: Access token
    :param project_id: Project ID
    :type token: str
    :type project_id: int
    :return: baseline scenario id
    :rtype: int
    """
    r = get_project(token, project_id)
    scenarios = r.json()["scenarios"]
    scene = next(item for item in scenarios if item["parent"] is None)
    baseline_id = scene["id"]
    return baseline_id


def get_city_boundray(token, project_id):
    """
    Return a cities geojson boundary id

    :param token: Access token
    :param project_id: project ID
    :type token: str
    :type project_id: int
    :return: geojson boundary id
    :rtype: int
    """

    r = get_geojsons(token, project_id)
    geojsons = r.json()
    geojson_city_id = geojsons["geojsons"][0]["id"]
    return geojson_city_id


def show_nodes(token):
    """
    Prints list of available nodes

    :param token: Access token
    :type token: str
    """
    r = get_scenario_workflow_nodes(token)
    if not r.status_code == 200:
        raise Exception(f"Could not get scenario workflow nodes")

    smnodes = r.json()["scenario_maker_nodes"]
    for node in smnodes:
        print(node["id"], node["name"])


def show_scenarios(token, project_id):
    """
    Prints a list of the scenarios in a project

    :param token: Access token
    :param project_id: project id
    :type token: str
    :type project_id: int
    """
    r = get_project(token, project_id)
    if not r.status_code == 200:
        raise Exception(f"Could not get scenario workflow nodes {r.status_code}")

    scenarios = r.json()["scenarios"]
    for s in scenarios:
        print(s["id"], s["status"], s["name"])


def get_scenarios(token, project_id):
    """
    Get a list of scenarios in a project

    :param token: Access token
    :param project_id: project ID
    :type str
    :type int
    :return: returns a dict of all scenario
    :rtype: dict
    """
    r = get_project(token, project_id)
    if not r.status_code == 200:
        raise Exception(f"Could not get scenario workflow nodes {r.status_code}")

    scenarios = r.json()["scenarios"]
    return scenarios


def show_log(token, scenario_id):
    """
    Print scenario log file

    :param token: Access token
    :param scenario_id: scenario id
    :type token: str
    :type scenario_id: int
    """
    r = get_simulations(token, scenario_id)

    if not r.status_code == 200:
        raise Exception(f"Could not get scenario log {r.status_code}")

    sims = r.json()

    for s in sims["simulations"]:
        database_id = json.loads(s)["id"]
    for s in sims["simulation_intances"]:
        print(json.loads(s)["id"],  json.loads(s)["progress"], json.loads(s)["heartbeat"], json.loads(s)["log"])

    return database_id


def add_assessment_model(token, data):
    """
        Creates a new assessment model and a default version tagged as 0.0.1
        the data must be of the shape:

        .. code-block::

            {
               name: "some name",
               description: "some desc",

               //optionally add assessment model stage of development
               //1 = ALPHA
               //2 = BETA
               //3 = UNDER DEVELOPMENT
               //default is 3
               stage: 2
               //must specify one of:
               model_id: <model_id> //by default will use the active version of this model
               model_version_id: <model_version_id> //if present will use this model version id
            }

        returns:

        .. code-block::

            {
              assessment_model_id: <the id of the new assessment model>,
              assessment_model_version_id: <id of the new default version>
            }

    """

    headers = {"Authorization": "Bearer " + token}
    return requests.post(url + "/assessment_models", headers=headers, json=data)


