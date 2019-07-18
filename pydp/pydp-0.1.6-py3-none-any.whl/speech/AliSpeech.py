#!/usr/bin/env python
# -*- coding: utf-8 -*-

import http.client
import urllib.parse
import json
from dp import utils, audio
import logging


def processGETRequest(appKey, token, voice, text, format, sampleRate):
    host = 'nls-gateway.cn-shanghai.aliyuncs.com'
    url = 'https://' + host + '/stream/v1/tts'
    # 设置URL请求参数
    url = url + '?appkey=' + appKey
    url = url + '&token=' + token
    url = url + '&text=' + text
    url = url + '&format=' + format
    url = url + '&sample_rate=' + str(sampleRate)
    url = url + '&voice=' + voice
    logging.debug(url)
    conn = http.client.HTTPSConnection(host)
    conn.request(method='GET', url=url)
    # 处理服务端返回的响应
    response = conn.getresponse()
    logging.debug('Response status and response reason:')
    logging.debug(response.status, response.reason)
    contentType = response.getheader('Content-Type')
    logging.debug(contentType)
    body = response.read()
    if 'audio/mpeg' == contentType:
        logging.debug('The GET request succeed!')
        tmpfile = utils.write_temp_file(body, '.mp3')
        conn.close()
        return tmpfile
    else:
        logging.debug('The GET request failed: ' + str(body))
        conn.close()
        return None


def processPOSTRequest(appKey, token, voice, text, format, sampleRate):
    host = 'nls-gateway.cn-shanghai.aliyuncs.com'
    url = 'https://' + host + '/stream/v1/tts'
    # 设置HTTPS Headers
    httpHeaders = {
        'Content-Type': 'application/json'
    }
    # 设置HTTPS Body
    body = {'appkey': appKey, 'token': token, 'text': text, 'format': format, 'sample_rate': sampleRate, 'voice': voice}
    body = json.dumps(body)
    logging.debug('The POST request body content: ' + body)
    # Python 2.x 请使用httplib
    # conn = httplib.HTTPSConnection(host)
    # Python 3.x 请使用http.client
    conn = http.client.HTTPSConnection(host)
    conn.request(method='POST', url=url, body=body, headers=httpHeaders)
    # 处理服务端返回的响应
    response = conn.getresponse()
    logging.debug('Response status and response reason:')
    logging.debug(response.status, response.reason)
    contentType = response.getheader('Content-Type')
    logging.debug(contentType)
    body = response.read()
    if 'audio/mpeg' == contentType:
        logging.debug('The POST request succeed!')
        tmpfile = utils.write_temp_file(body, '.mp3')
        conn.close()
        return tmpfile
    else:
        logging.critical('The POST request failed: ' + str(body))
        conn.close()
        return None


def process(request, token, audioContent):
    # 读取音频文件
    host = 'nls-gateway.cn-shanghai.aliyuncs.com'
    # 设置HTTP请求头部
    httpHeaders = {
        'X-NLS-Token': token,
        'Content-type': 'application/octet-stream',
        'Content-Length': len(audioContent)
    }
    conn = http.client.HTTPConnection(host)
    conn.request(method='POST', url=request, body=audioContent, headers=httpHeaders)
    response = conn.getresponse()
    logging.debug('Response status and response reason:')
    logging.debug(response.status, response.reason)
    body = response.read()
    try:
        logging.debug('Recognize response is:')
        body = json.loads(body)
        logging.debug(body)
        status = body['status']
        if status == 20000000:
            result = body['result']
            logging.debug('Recognize result: ' + result)
            conn.close()
            return result
        else:
            logging.critical('Recognizer failed!')
            conn.close()
            return None
    except ValueError:
        logging.debug('The response is not json format string')
        conn.close()
        return None


def tts(appKey, token, voice, text):
    # 采用RFC 3986规范进行urlencode编码
    textUrlencode = text
    textUrlencode = urllib.parse.quote_plus(textUrlencode)
    textUrlencode = textUrlencode.replace("+", "%20")
    textUrlencode = textUrlencode.replace("*", "%2A")
    textUrlencode = textUrlencode.replace("%7E", "~")
    format = 'mp3'
    sampleRate = 16000
    return processPOSTRequest(appKey, token, voice, text, format, sampleRate)


def asr(appKey, token, wave_file):
    # 服务请求地址
    url = 'http://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/asr'
    pcm = audio.get_pcm_from_wavv(wave_file)
    # 音频文件
    format = 'pcm'
    sampleRate = 16000
    enablePunctuationPrediction = True
    enableInverseTextNormalization = True
    enableVoiceDetection = False
    # 设置RESTful请求参数
    request = url + '?appkey=' + appKey
    request = request + '&format=' + format
    request = request + '&sample_rate=' + str(sampleRate)
    if enablePunctuationPrediction:
        request = request + '&enable_punctuation_prediction=' + 'true'
    if enableInverseTextNormalization:
        request = request + '&enable_inverse_text_normalization=' + 'true'
    if enableVoiceDetection:
        request = request + '&enable_voice_detection=' + 'true'
    logging.debug('Request: ' + request)
    return process(request, token, pcm)
