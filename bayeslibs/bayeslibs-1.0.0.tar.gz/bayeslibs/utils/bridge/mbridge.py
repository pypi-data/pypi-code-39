# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/5/30
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.config.setting import ApolloConfig
from bayeslibs.utils.comm.http import Http

APOLLO_CONFIG = ApolloConfig()


def map_bridge(req_type, data=None):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type
    }
    if data:
        request_json['data'] = data
    return Http.request_json(APOLLO_CONFIG.get_robot_route_url('map/save'), request_json)


def move_bridge(req_type, data=None):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type
    }
    if data:
        request_json['data'] = data
    return Http.request_json(APOLLO_CONFIG.get_robot_route_url('motion/move'), request_json)


def rotate_bridge(req_type, data=None):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type
    }
    if data:
        request_json['data'] = data
    return Http.request_json(APOLLO_CONFIG.get_robot_route_url('motion/rotate'), request_json)


def navigate_bridge(req_type, data=None):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type
    }
    if data:
        request_json['data'] = data
    return Http.request_json(APOLLO_CONFIG.get_robot_route_url('navigate'), request_json)
