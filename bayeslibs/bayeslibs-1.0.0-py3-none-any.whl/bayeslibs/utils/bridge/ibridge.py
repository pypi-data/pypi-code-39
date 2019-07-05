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


def object_detect_bridge(req_type, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    return Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/object_detect'), request_json)


def distance_detect_bridge(req_type, pos=None, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    if pos:
        request_json['pos'] = pos
    return Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/distance_detect'), request_json)


def color_recog_bridge(req_type, colors='red', is_multi=False, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show,
        'is_multi': is_multi,
        'colors': colors
    }
    return Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/color_recog'), request_json)


def face_detect_bridge(req_type, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    return Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/face_detect'), request_json)


def face_recog_bridge(req_type, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    return Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/face_recog'), request_json)


def age_gender_recog_bridge(req_type, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    return Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/age_gender_recog'), request_json)


def emotion_recog_bridge(req_type, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    return Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/emotion_recog'), request_json)


def headpose_recog_bridge(req_type, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    return Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/headpose_recog'), request_json)


def beauty_recog_bridge(req_type, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    return Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/beauty_recog'), request_json)


def handpose_recog_bridge(req_type, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    return Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/handpose_recog'), request_json)


def skeleton_recog_bridge(req_type, is_show=True):
    request_json = {
        'uuid': APOLLO_CONFIG.get_appid(),
        'type': req_type,
        'is_show': is_show
    }
    return Http.request_json(APOLLO_CONFIG.get_robot_route_url('vision/skeleton_recog'), request_json)
