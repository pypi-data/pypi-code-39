#   Written by ThousandEyes Professional Services.
#   Email services@thousandeyes.com
#   License is covered under the existing MSA agreement between customer and ThousandEyes
import logging
import re
import csv
import json
import os
import time
from datetime import datetime
from te_net import Network, HTTPResponseError


TEST_TYPE_DICT = {
    "agent-to-server": ["net/metrics"],
    "agent-to-agent": ["net/metrics"],
    "http-server": ["web/http-server", "net/metrics"],
    "page-load": ["web/page-load", "web/http-server", "net/metrics"],
}

NET_METRICS_DICT = {"loss": 0, "avgLatency": 0, "jitter": 0}

HTTP_METRICS_DICT = {
    "responseCode": 0,
    "dnsTime": 0,
    "connectTime": 0,
    "sslTime": 0,
    "waitTime": 0,
    "receiveTime": 0,
    "responseTime": 0,
    "totalTime": 0,
    "throughput": 0,
}

PAGE_LOAD_METRICS_DICT = {"domLoadTime": 0, "pageLoadTime": 0}

LAYER_METRIC = {
    "web/page-load": ["domLoadTime", "pageLoadTime"],
    "web/http-server": [
        "responseCode",
        "dnsTime",
        "connectTime",
        "sslTime",
        "waitTime",
        "receiveTime",
        "responseTime",
        "totalTime",
        "throughput",
    ],
    "net/metrics": ["loss", "avgLatency", "jitter"],
}


def get_accounts_info() -> dict:
    """
    Retrieve Organization's Account Groups.

    :return:dictionary containing Account's Name to ID mapping.
    :rtype: dict
    Return dictionary format {"aid_name1": aid1, aid_name2: aid2, ...}
    """
    name_to_aid_dict = dict()
    logging.info(f"{get_accounts_info.__name__}:: Getting account group names and IDs")
    try:
        aids = network.get("/account-groups")
    except HTTPResponseError as err:
        logging.error(
            f"{get_accounts_info.__name__}:: Unable to retrieve Account Groups data: {err}"
        )
    except Exception as err:
        logging.error(f"{get_accounts_info.__name__}:: General exceptions: {err}")
    if aids:
        account_groups = aids.get("accountGroups")
        if account_groups:
            for aid in account_groups:
                account_group_name = aid.get("accountGroupName")
                account_group_id = aid.get("aid")
                if account_group_name and account_group_id:
                    name_to_aid_dict[account_group_name] = account_group_id
            return name_to_aid_dict


def get_basic_test_info(aid: int = 0, aid_name: str = None) -> dict:
    """
    Retrieve a dict of tests associated with an Account Group.
    Exclude the disabled and the savedEvents from the returned dict.

    :param aid: Account Group ID
    :param aid_name: Account Group Name
    :type aid: int
    :type aid_name: str
    :return: dictionary containing each test's ID as key and list of name, test type and aid as corresponding value.
    :rtype:dict
    Return dictionary format {test1_id: ["test1_name", "test1_type", test1_aid], ...}
    """
    test_meta_dict = dict()
    logging.info(
        f"{get_basic_test_info.__name__}:: Getting basic test info for tests in aid {aid_name}({aid})"
    )
    try:
        if aid > 0:
            basic_test_info = network.get("/tests", options={"aid": aid})
        else:
            basic_test_info = network.get("/tests")
        if basic_test_info:
            basic_tests = basic_test_info.get("test")
            if basic_tests:
                for test in basic_tests:
                    if test.get("enabled") and not test.get("savedEvent"):
                        test_meta_dict[test.get("testId")] = [
                            test.get("testName"),
                            test.get("type"),
                            aid,
                        ]
                return test_meta_dict
    except HTTPResponseError as err:
        logging.error(
            f"{get_basic_test_info.__name__}:: Unable to retrieve basic test info for {test.get('testName')}({test}): {err}"
        )
    except Exception as err:
        logging.error(f"{get_basic_test_info.__name__}:: General exceptions: {err}")


def get_layered_test_info(
    test_id: int, test_name: str, test_type: str, time_range: str = None, aid: int = 0
) -> dict:
    """
    Get detailed information for each test using layers corresponding to each test type as specified in TEST_TYPE_DICT.

    :param test_id: unique test ID integer.
    :param test_name: unique test name string.
    :param test_type: test type. Test types supported by this script are specified in the TEST_TYPE_DICT.
    :param time_range: time window for data retrieval. This value should abide by regex [0-9]+[smhdw]?
    :param aid: Account Group ID integer.
    :return: dictionary containing test layer name as key and corresponding list of data results retrieved per layer.
    :rtype: dict
    Return dictionary format {'web/http-server' : [page1_dict_data, page2_dict_data], 'net/metrics' : [page1_dict_data, page2_dict_data], ...}
    """
    detailed_test_info = dict()
    time_range = _time_range_validator(time_range)
    if test_type in TEST_TYPE_DICT:
        for layer in TEST_TYPE_DICT.get(test_type):
            logging.info(
                f"{get_layered_test_info.__name__}:: Getting detailed test info for test {test_name}({test_id}) layer {layer}"
            )
            try:
                if aid > 0:
                    layer_dict = network.get(
                        layer + "/" + str(test_id),
                        options={"window": time_range, "aid": aid},
                    )
                else:
                    layer_dict = network.get(
                        layer + "/" + str(test_id), options={"window": time_range}
                    )
                if layer_dict:
                    detailed_test_info[layer] = [layer_dict]
                    if layer_dict.get("pages") and layer_dict.get("pages").get("next"):
                        while layer_dict.get("pages").get("next"):
                            new_page_url = layer_dict.get("pages").get("next")
                            logging.info(
                                f"{get_layered_test_info.__name__}:: "
                                f"Pagination is required. "
                                f"Retrieving more info for {test_name}({test_id}) layer {layer}"
                            )
                            try:
                                layer_dict = network.get(new_page_url.split("v6/")[1])
                                if layer_dict and detailed_test_info.get(layer):
                                    detailed_test_info.get(layer).append(layer_dict)
                            except HTTPResponseError as err:
                                logging.error(
                                    f"{get_layered_test_info.__name__}:: "
                                    f"Unable to retrieve additional pages from {new_page_url} "
                                    f"{test_name}({test_id}) at layer {layer}: {err}"
                                )
            except HTTPResponseError as err:
                logging.error(
                    f"{get_layered_test_info.__name__}:: "
                    f"Unable to retrieve detailed test info for "
                    f"{test_name}({test_id}) at layer {layer}: {err}"
                )
            except Exception as err:
                logging.error(
                    f"{get_layered_test_info.__name__}:: General exceptions: {err}"
                )
    return detailed_test_info


def process_layered_test_info(
    test_id: int, test_name: str, test_type: str, time_range: str = "1h", aid: int = 0
) -> dict:
    """
    Process test data retrieved through API in format applicable to the specification.
    Function will use helper functions to flatten data from multiple layers and pages into a single dictionary.

    :param test_id: unique test ID integer.
    :param test_name: unique test name string.
    :param test_type: test type. Test types supported by this script are specified in the TEST_TYPE_DICT.
    :param time_range: time window for data retrieval. This value should abide by regex [0-9]+[smhdw]?
    :param aid: Account Group ID integer.
    :return: return test data dictionary in format that will later be used for writing.
    :rtype: dict
    Return dictionary format:
    {test_aid :
        |_{test_id:
            |_[test_name, {agent_id:
                |_[agent_name, {round_id:
                    |_{test_layer:
                        |_{metric_data}}}]}]}}
    """
    aid_test_agent_time_metric_dict = {aid: {test_id: [test_name, {}]}}
    time_range = _time_range_validator(time_range)
    try:
        unprocessed_result = get_layered_test_info(
            test_id, test_name, test_type, time_range, aid
        )
        if unprocessed_result:
            agent_metric_dict = _process_helper(unprocessed_result, test_type)
            if agent_metric_dict and aid_test_agent_time_metric_dict.get(aid):
                aid_test_agent_time_metric_dict.get(aid).get(test_id)[
                    1
                ] = agent_metric_dict
        return aid_test_agent_time_metric_dict
    except HTTPResponseError as err:
        logging.error(
            f"{process_layered_test_info.__name__:: }"
            f"Unable to retrieve detailed test info for "
            f"{test_name}({test_id}) at layer: {err}"
        )
    except Exception as err:
        logging.error(
            f"{process_layered_test_info.__name__}:: General exceptions: {err}"
        )


def _process_helper(data_dict: dict, test_type: str) -> dict:
    """
    Function that will be used by the main processing function to restructure API returned dictionaries.

    :param data_dict: dictionary that will be passed into function containing layer to paged API data list.
    Format of data_dict {'web/http-server' : [page1_dict_data, page2_dict_data], 'net/metrics' : [page1_dict_data, page2_dict_data], ...}
    :param test_type: test type. Test types supported by this script are specified in the TEST_TYPE_DICT.
    :return: dictionary with Agent ID as keys and all the corresponding rounds' data as its values.
    :rtype:dict
    Return dictionary format:
    {agent_id:
        |_[agent_name, {round_id:
            |_{test_layer:
                |_{metric_data}}}]}]}}
    """
    agent_metric_dict = dict()

    def inner_helper_function(data_array: list, metric_dict: dict):
        """
        Inner function to simplify repetitive metric processing.

        :param data_array: Subset of API returned data containing agent ID, round ID and corresponding metric in each entry.
        :param metric_dict: depending on the processed layer, corresponding set of metric that will need to be retrieved.
        :return: None
        """
        for data_point in data_array:
            pl_metric = dict()
            agent_id = data_point.get("agentId")
            round_id = data_point.get("roundId")
            for metric in metric_dict:
                pl_metric[metric] = data_point.get(metric)
            if agent_id and agent_id in agent_metric_dict:
                # This round_id is already present - we need to update its content with this layer's metrics
                agent_round_dict = agent_metric_dict.get(agent_id)[1]
                if round_id and agent_round_dict and round_id in agent_round_dict:
                    if agent_round_dict.get(round_id):
                        agent_round_dict.get(round_id).update({layer: pl_metric})
                # This is the fist time we see this round - set its content
                elif round_id and agent_round_dict:
                    agent_round_dict[round_id] = {layer: pl_metric}
            # Otherwise we are seeing this agent for the first time
            elif agent_id and round_id and data_point.get("agentName"):
                agent_metric_dict[agent_id] = [
                    data_point.get("agentName"),
                    {round_id: {layer: pl_metric}},
                ]

    for layer in TEST_TYPE_DICT.get(test_type):
        raw_data_array = data_dict.get(layer)
        if raw_data_array:
            if layer == "web/page-load":
                for layer_pages in raw_data_array:
                    data = layer_pages.get("web").get("pageLoad")
                    if data:
                        inner_helper_function(data, PAGE_LOAD_METRICS_DICT)
            elif layer == "web/http-server":
                for layer_pages in raw_data_array:
                    data = layer_pages.get("web").get("httpServer")
                    if data:
                        inner_helper_function(data, HTTP_METRICS_DICT)
            elif layer == "net/metrics":
                for layer_pages in raw_data_array:
                    data = layer_pages.get("net").get("metrics")
                    if data:
                        inner_helper_function(data, NET_METRICS_DICT)
    return agent_metric_dict


def write_test_info(
    test_id: int,
    test_name: str,
    test_type: str,
    time_range: str = "1h",
    aid: int = 0,
    report_dir: str = ".",
    file_format: str = ".csv",
):
    """
    Function that will write test data into config file provided folder.

    :param test_id: unique test ID integer.
    :param test_name: unique test name string.
    :param test_type: test type. Test types supported by this script are specified in the TEST_TYPE_DICT.
    :param time_range: time window for data retrieval. This value should abide by regex [0-9]+[smhdw]?
    :param aid: Account Group ID integer.
    :param report_dir: Directory where reports will be written to.
    :param file_format: String specifying required file format. Default is set to csv.
    :return: None
    """
    write_data = list()
    header = ["agent name", "agent id", "test name", "test id", "timestamp"]
    file_time_stamp = (
        datetime.isoformat(datetime.utcnow()).split(".")[0].replace(":", "-")
    )
    test_file_name = test_name
    for sym in " :/":
        test_file_name = test_file_name.replace(sym, "_")
    file_name = os.path.join(
        report_dir,
        test_file_name + "_" + file_time_stamp + "_" + time_range + file_format,
    )
    metric_header = list()
    agent_time_data = dict()

    def inner_write_helper(data, test_type):
        """
        Inner helper function will process per layer data and extract relevant layer metric from it.

        This metrics wil be appended to the csv row entry.
        Changes to metric data format representations may be applied here.
        :param data: dictionary containing per layer paginated data.
        Format of data_dict {'web/http-server' : [page1_dict_data, page2_dict_data], 'net/metrics' : [page1_dict_data, page2_dict_data], ...}
        :param test_type: supported test type.
        :return: None
        """
        if test_type in TEST_TYPE_DICT:
            metric_data = []
            layers = TEST_TYPE_DICT.get(test_type)
            if layers:
                for layer in layers:
                    for layer_metric in LAYER_METRIC.get(layer):
                        if data.get(layer):
                            metric_result = data.get(layer).get(layer_metric)
                            metric_data.append(metric_result)
                            if layer_metric not in metric_header:
                                metric_header.append(layer_metric)
                        else:
                            metric_data.append("N/A")
                data_row.extend(metric_data)

    aid_test_agent_time_data = process_layered_test_info(
        test_id, test_name, test_type, time_range, aid
    )
    if (
        aid_test_agent_time_data
        and aid_test_agent_time_data.get(aid)
        and aid_test_agent_time_data.get(aid).get(test_id)[1]
    ):
        agent_time_data = aid_test_agent_time_data.get(aid).get(test_id)[1]
        if agent_time_data:
            for agent_id in agent_time_data:
                if agent_time_data.get(agent_id)[1]:
                    for round_id in agent_time_data.get(agent_id)[1]:
                        data_row = list()
                        data_row.extend(
                            [
                                agent_time_data.get(agent_id)[0],
                                agent_id,
                                test_name,
                                test_id,
                                _epoch_to_datetime(round_id),
                            ]
                        )
                        round_data = agent_time_data.get(agent_id)[1].get(round_id)
                        if round_data and test_type in TEST_TYPE_DICT:
                            inner_write_helper(round_data, test_type)
                        else:
                            logging.info(
                                f"{write_test_info.__name__}:: Unable to process this {test_type}"
                            )
                        write_data.append(data_row)
            header.extend(metric_header)
            write_data.sort(key=lambda x: (x[0], x[4]))
            with open(file_name, "w", newline="") as wf:
                logging.info(
                    f"{write_test_info.__name__}:: Writing test {test_name}({test_id}) data into {file_name}"
                )
                csv_writer = csv.writer(wf)
                csv_writer.writerow(header)
                csv_writer.writerows(write_data)


def get_write_aid_tests(
    aid: int, aid_name: str, time_range: str, report_dir: str, file_format: str
):
    """
    Function that will fetch and write all the test info for a specific Account Group.

    :param aid: Account Group ID
    :param aid_name: Account Group Name
    :param time_range: time window for data retrieval. This value should abide by regex [0-9]+[smhdw]?
    :param report_dir: directory where report data will be stored.
    :return: None
    """
    counter = 0
    basic_info_dict = get_basic_test_info(aid, aid_name)
    if basic_info_dict:
        total = len(basic_info_dict)
        logging.info(
            f"{get_write_aid_tests.__name__}:: Retrieved basic info for {aid_name}({aid}): {total} tests."
        )
        logging.info(
            f"{get_write_aid_tests.__name__}:: Data file will be written in {report_dir} folder"
        )
        for test in basic_info_dict:
            # Each test entry should have test_name, test_type and aid
            if len(basic_info_dict.get(test)) == 3:
                test_id, test_name, test_type, time_range, aid = (
                    test,
                    basic_info_dict.get(test)[0],
                    basic_info_dict.get(test)[1],
                    time_range,
                    basic_info_dict.get(test)[2],
                )
                logging.debug(
                    f"{get_write_aid_tests.__name__}:: Initiating work with {test_name}({test_id})"
                )
                if test_type in TEST_TYPE_DICT:
                    counter += 1
                    logging.info(
                        f"{get_write_aid_tests.__name__}:: {aid_name}: Received info for {counter}/{total} {test_name}({test_id})"
                    )
                    write_test_info(
                        test_id,
                        test_name,
                        test_type,
                        time_range,
                        aid,
                        report_dir,
                        file_format,
                    )
                    logging.info(
                        f"{get_write_aid_tests.__name__}:: {aid_name}: Info for {counter}/{total} {test_name}({test_id}) has been written"
                    )
                else:
                    logging.error(
                        f"{get_write_aid_tests.__name__}:: {aid_name}: Unsupported test {counter}/{total} {test_name}({test_id})"
                    )
                    counter += 1
                    continue


def _epoch_to_datetime(epoch: int) -> str:
    """
    Function to convert roundId values to datetime format time stamps.

    :param epoch: roundId integer
    :return: datetime formatted string
    """
    return datetime.isoformat(datetime.utcfromtimestamp(epoch))


def _time_range_validator(time_range: str) -> str:
    """
    Function to validate passed in time_range parameter.
    In case if parameter is not validated, an exception will be thrown.

    :param time_range: time window for data retrieval. This value should abide by regex [0-9]+[smhdw]?
    :return: validated time range string.
    """
    time_range_pattern = re.compile(r"([0-9]+)([smhdw]?)")
    match = re.match(time_range_pattern, time_range)
    if match.group(1) and match.group(2):
        return time_range
    elif match.group(1):
        return match.group(1)
    else:
        raise Exception("Check your time range configuration.")


if __name__ == "__main__":
    with open("config.json") as cf:
        config = json.load(cf)
    # Setting variables from the config file
    log_file = config.get("log").get("file")
    log_level = config.get("log").get("level")
    username = config.get("credentials").get("username")
    password = config.get("credentials").get("basicAuthToken")
    report_dir = config.get("options").get("dataDir")
    report_timespan = config.get("options").get("timeRange")
    aids_to_report = config.get("credentials").get("accountGroups")
    file_format = config.get("options").get("fileFormat")

    proxy_type = config.get("network").get("proxy_type")
    proxy_address = config.get("network").get("proxy_address")
    proxy_password = config.get("network").get("proxy_password")
    proxy_username = config.get("network").get("proxy_username")

    if username and password and proxy_address and proxy_username and proxy_password:
        network = Network(
            username=username,
            authToken=password,
            proxy_type=proxy_type,
            proxy_address=proxy_address,
            proxy_username=proxy_username,
            proxy_password=proxy_password,
        )
    elif username and password and proxy_address:
        network = Network(
            username=username,
            authToken=password,
            proxy_type=proxy_type,
            proxy_address=proxy_address,
        )
    elif username and password:
        network = Network(username=username, authToken=password)
    else:
        logging.error("Please provide relevant credentials in the configuration file.")

    if log_file and log_level:
        logging.basicConfig(
            filename=log_file,
            level=log_level,
            format="%(asctime)s %(levelname)s %(message)s",
        )
    else:
        logging.basicConfig(
            filename="./te_reports.log",
            level="INFO",
            format="%(asctime)s %(levelname)s %(message)s",
        )

    if report_dir and not os.path.exists(report_dir):
        os.mkdir(report_dir)
    elif report_dir:
        pass
    elif not os.path.exists("./te_reports"):
        os.mkdir("./te_reports")
        report_dir = "./te_reports"

    if not report_timespan:
        report_timespan = "1h"

    name_to_aid_dict = get_accounts_info()
    start_time = time.perf_counter()
    print(
        "Starting retrieval script. This can take awhile. Please check log messages for progress."
    )
    if aids_to_report:
        for aid_to_report in aids_to_report:
            if aid_to_report in name_to_aid_dict:
                aid = name_to_aid_dict.get(aid_to_report)
                if file_format and aid:
                    get_write_aid_tests(
                        aid, aid_to_report, report_timespan, report_dir, file_format
                    )
                elif aid:
                    get_write_aid_tests(
                        aid, aid_to_report, report_timespan, report_dir, ".csv"
                    )

    else:
        for name_aid in name_to_aid_dict:
            if name_to_aid_dict.get(name_aid):
                get_write_aid_tests(
                    name_to_aid_dict.get(name_aid),
                    name_aid,
                    report_timespan,
                    report_dir,
                )

    print(f"Execution took: {time.perf_counter()-start_time} seconds")
