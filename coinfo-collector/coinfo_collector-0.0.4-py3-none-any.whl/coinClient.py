# -*- coding: utf-8 -*-
import asyncio
import logging
import queue
import os
import threading
import requests
from time import sleep
import ujson
from utail_base import web_support, threading_support

# from .coinCommons import CoinCommons as CC

log = logging.getLogger('coininfo_collector')

api_prefix = 'https://api.coingecko.com/api/v3/'

limitRequestsPerMin = int(os.environ['limitRequestsPerMin']) if 'limitRequestsPerMin' in os.environ else 100
# self._requestDurationForOneRequest = float(limitRequestsPerMin) / 60.0

requestCostTime = float(60) / float(limitRequestsPerMin)


class CoinClient:
    def __init__(
        self, loggerName='coininfo_collector', 
        keepJobsInQ = 5,
        aliveURL='http://127.0.0.1:6000/sche/coinAlive',
        requestURL='http://127.0.0.1:6000/sche/coinJobRequest',
        reportURL='http://127.0.0.1:6000/sche/coinJobReport',
        logURL='http://127.0.0.1:6000/sche/coinJobReport',
        jobCoin = True,
        jobTicker = True,
    ):
        self._log = logging.getLogger(loggerName)
        self._keepJobsInQ = keepJobsInQ

        self._aliveURL = aliveURL
        self._requestURL = requestURL
        self._reportURL = reportURL
        self._logURL = logURL

        self._jobCoin = jobCoin
        self._jobTicker = jobTicker

        # job q
        self._jobQ = queue.Queue()
        self._reportQ = queue.Queue()

        self._requestJobList = list()

        # make Job List.
        self._makeJobList()

        self._tickerPage = 1
        self._coinsMarketPage = 1

        self._tickerList = list()


        # 보고 쓰레드 시작
        treport = threading.Thread(
            target=self._reportTask,
            name='coinReport'
        )             
        treport.setDaemon(False)
        treport.start()

        
        # 요청 쓰레드 시작
        trequest = threading.Thread(
            target=self._requestTask,
            name='coinRequest'
        )             
        trequest.setDaemon(False)
        trequest.start()

        # 작업 쓰레드 시작
        t = threading.Thread(
            target=self._runTask,
            # args=[self._pjs, threadName, i], 
            name='coinClient'
        )             
        t.setDaemon(False)
        t.start()

    def _makeJobList(self):
        if self._jobCoin is False \
            and self._jobTicker is False:
            web_support.raiseHttpError(log, 0, 'None jobs..')

        if self._jobCoin is True:
            self._requestJobList.append('jobCoin')
        if self._jobTicker is True:
            self._requestJobList.append('jobTicker')


    def _reportTask(self):
        while True:
            try:
                if self._reportQ.empty() is True:
                    sleep(1)
                    continue

                job, target_id, output = self._reportQ.get()

                response = requests.post(
                    self._reportURL,
                    verify=False,
                    json={
                        'job':job,
                        'id':target_id,
                        'output':output,
                    },
                )

                if response.status_code != 200:
                    log.error('failed report. code:{} msg:{}'.format(
                        response.status_code, response.text))
                    sleep(1)
                    continue

            except Exception as inst:
                log.error('exception in _reportTask. msg:{}'.format(inst.args))


    def _requestTask(self):

        while True:
            try:
                if requests.post(
                    self._aliveURL
                ).status_code == 200:
                    break
                
            except:
                log.debug('connecting to coin-scheduler')
                sleep(1)
                continue
        
        while True:
            try:
                if self._keepJobsInQ <= self._jobQ.qsize():
                    sleep(1)
                    continue

                response = requests.post(
                    self._requestURL,
                    verify=False,
                    json={
                        'jobs':self._requestJobList,
                    },
                )

                if response.status_code != 200:
                    log.error('failed _getJobCoinList. code:{} msg:{}'.format(response.status_code, response.status_code.text))

                    sleep(1)
                    continue

                jo = ujson.loads(response.text)
                #print(ujson.dumps(jo, ensure_ascii=False))

                for job in jo['jobs']:
                    self._jobQ.put(job)

                if 0 == len(jo['jobs']):
                    sleep(3)

            except Exception as inst:
                log.error('failed _getJobCoinList. msg:{}'.format(inst.args))
                sleep(3)

    def _runTask(self):
        while True:
            try:
                if self._jobQ.empty():
                    sleep(1)
                    continue

                job = self._jobQ.get()
                if 'id' not in job:
                    job['id'] = 0

                #print(job)

                endJob = False
                self._tickerPage = 1
                self._coinsMarketPage = 1
                output = {}

                while endJob is False:
                    if job['job'] == 'coins_markets':
                        if 'data' not in output:
                            output['data'] = list()
                        endJob = self._requestCoinsMarkets(output)
                    elif job['job'] == 'market_chart':
                        endJob = self._requestMarketChart(job['id'], output)
                    elif job['job'] == 'global':
                        endJob = self._requestGlobal(output)
                    elif job['job'] == 'ticker':
                        if 'tickers' not in output:
                            output['tickers'] = list()
                        endJob = self._requestTicker(job['id'], output)

                self._reportQ.put((
                    job['job'],
                    job['id'],
                    output
                ))

            except Exception as inst:
                log.error('exception in _runTask. job:{} msg:{}'.format(job, inst.args))



    @threading_support.timeDuration(log, requestCostTime)
    def _requestCoinsMarkets(self, output):
        perPage = 250

        response = requests.request(
            "GET",
            api_prefix + 'coins/markets?vs_currency=usd&per_page={}&page={}&order=volume_desc'.format(
                perPage, self._coinsMarketPage
            ),
            data='', 
            headers={'cache-control': 'no-cache'},
        )

        if 200 != response.status_code:
            web_support.raiseHttpError(log, response.status_code, response.text)

        self._coinsMarketPage += 1

        jo = ujson.loads(response.text)

        try:
            arraySize = 0
            for ent in jo:
                arraySize += 1
                output['data'].append(ent)

            return 250 > arraySize
        except Exception as inst:
            web_support.raiseHttpError(
                log, 
                response.status_code, 
                'exception in _requestCoinsMarkets. msg:{}. page:{}'.format(
                inst.args, self._coinsMarketPage)
            )

    @threading_support.timeDuration(log, requestCostTime)
    def _requestMarketChart(self, target_id, output):
        response = requests.request(
            "GET",
            api_prefix + 'coins/{}/market_chart?vs_currency=usd&days=1'.format(
                target_id,
            ),
            headers={'cache-control': 'no-cache'},
        )

        if 200 != response.status_code:
            web_support.raiseHttpError(log, response.status_code, response.text)

        self._coinsMarketPage += 1

        jo = ujson.loads(response.text)
        jo['cid'] = str(target_id)
        jo['days'] = 1

        output['data'] = jo
        return True

    @threading_support.timeDuration(log, requestCostTime)
    def _requestGlobal(self, output):
        response = requests.request(
            "GET",
            api_prefix + 'global',
            headers={'cache-control': 'no-cache'},
        )

        if 200 != response.status_code:
            web_support.raiseHttpError(log, response.status_code, response.text)

        jo = ujson.loads(response.text)

        output['data'] = jo
        return True



    @threading_support.timeDuration(log, requestCostTime )
    def _requestTicker(self, target_id, output):
        response = requests.request(
            "GET",
            api_prefix + 'exchanges/{}/tickers?page={}&order=volume_desc'.format(
                target_id, self._tickerPage
            ),
            data='', 
            headers={'cache-control': 'no-cache'},
        )

        if 200 != response.status_code:
            web_support.raiseHttpError(log, response.status_code, response.text)

        self._tickerPage += 1

        jo = ujson.loads(response.text)

        try:
            output['tickers'].extend(jo['tickers'])
        except Exception as inst:
            web_support.raiseHttpError(
                log, 
                response.status_code, 
                '_requestTicker. no tickers. msg:{}. target_id:{}'.format(
                inst.args, target_id)
            )

        if len(output['tickers']) == 0:
            web_support.raiseHttpError(
                log, 
                0, 
                '_requestTicker. no tickers. (not error). exchange:{}'.format(
                target_id)
            )

        # ticker 갯수가 100개 미만일 경우 마지막 페이지 입니다.
        return 100 > len(jo['tickers'])
