# -*- coding: utf-8 -*-
import asyncio
import logging
import queue
import os
import threading
import requests
from timeit import default_timer as timer
import ujson
from utail_base import web_support

# from .coinCommons import CoinCommons as CC

log = logging.getLogger('coininfo_collector')

api_prefix = 'https://api.coingecko.com/api/v3/'

class CoinScheduler:
    limitRequestsPerMin = int(os.environ['limitRequestsPerMin']) if 'limitRequestsPerMin' in os.environ else 100.0

    requestCostTime = float(60) / float(limitRequestsPerMin)

    costAdj = 1.0 / 100.0 * float(limitRequestsPerMin)

    # coins/markets
    fixedrp_coins_markets = 60.0 / costAdj
    # global
    fixedrp_global = 180.0 / costAdj
    # market_chart
    fixedrp_market_chart = 7.0 / costAdj


    def __init__(self, loggerName='coininfo_collector'):
        self._log = logging.getLogger(loggerName)

        # job coins q
        self._coinQ = queue.Queue()
        # job tickers q
        self._exchangeQ = queue.Queue()
        # job fixedFq q
        self._fixedQ = queue.Queue()
        # job fixedFq q
        self._fixedOnceQ = queue.Queue()

        #
        self._lockExchanges = threading.Lock()
        # 거래ㅇ 상세 정보
        self._exchanges = list()

        self._tickCnt = 0


        # 거래소 정보
        self._exchangesUpdate()

        # 작업큐 생성
        self.tick()

        # 작업 쓰레드 시작
        t = threading.Thread(
            target=self._runTask,
            # args=[self._pjs, threadName, i], 
            name='coinScheduler'
        )             
        t.setDaemon(False)
        t.start()

    def _runTask(self):
        #loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        asyncio.ensure_future(self._getJobFixedFreq())
        asyncio.ensure_future(self._getJobCoinList())
        asyncio.ensure_future(self._getExchangeJobList())

        loop.run_forever()

        print('broken task')


    def ping(self):
        pass

    def _exchangesUpdate(self):
        response = requests.request(
            'GET',
            'https://api.coingecko.com/api/v3/exchanges',
            headers={'cache-control': 'no-cache'},
        )

        if 200 != response.status_code:
            web_support.raiseHttpError(log, response.status_code, 'failed _exchangesUpdate')

        jo = ujson.loads(response.text)

        with self._lockExchanges:

            self._exchanges.clear()

            #print(ujson.dumps(jo, ensure_ascii=False))
            for ent in jo:
                self._exchanges.append(ent)


    async def _getJobFixedFreq(self):
        elapsed_coins_markets = 0.0
        elapsed_market_chart = 0.0
        elapsed_global = 0.0

        sleepTimeUnit = 0.1

        try:
            while True:
                startTime = timer()

                await asyncio.sleep(sleepTimeUnit)

                if self._fixedQ.qsize() > 100:
                    log.error('Process the fixed-Q quickly')
                    continue

                if CoinScheduler.fixedrp_coins_markets <= elapsed_coins_markets:
                    elapsed_coins_markets = 0.0
                    if self._fixedOnceQ.empty() is True:
                        self._fixedOnceQ.put({'job':'coins_markets'})

                if CoinScheduler.fixedrp_market_chart <= elapsed_market_chart:
                    elapsed_market_chart = 0.0

                    if self._coinQ.empty() is False:
                        self._fixedQ.put({'job':'market_chart', 'id':self._coinQ.get()})
                    else:
                        log.error('coinQ is empty')

                if CoinScheduler.fixedrp_global <= elapsed_global:
                    elapsed_global = 0.0
                    self._fixedQ.put({'job':'global'})

                
                elapsed = timer() - startTime

                elapsed_coins_markets += elapsed
                elapsed_market_chart += elapsed
                elapsed_global += elapsed

        except Exception as inst:
            log.error('exception in _getJobFixedFreq. msg:{}'.format(inst.args))
                
                
    async def _getJobCoinList(self):
        while True:
            try:
                if 1000 <= self._coinQ.qsize():
                    await asyncio.sleep(1)
                    continue

                startTime = timer()

                response = requests.request(
                    'GET',
                    'https://api.coingecko.com/api/v3/coins/list',
                    headers={'cache-control': 'no-cache'},
                )

                if 200 != response.status_code:
                    web_support.raiseHttpError(log, response.status_code, 'failed _getJobCoinList')

                #print('_getJobCoinList')

                jo = ujson.loads(response.text)
                #print(ujson.dumps(jo, ensure_ascii=False))

                for ent in jo:
                    self._coinQ.put(str(ent['id']))

            except Exception as inst:
                log.error('exception in _getJobCoinList. msg:{}'.format(inst.args))

            elapsed = timer() - startTime
            if float(CoinScheduler.requestCostTime) > (elapsed):
                await asyncio.sleep(float(CoinScheduler.requestCostTime) - float(elapsed))

    async def _getExchangeJobList(self):
        await asyncio.sleep(1)

        while True:
            try:
                if 15 <= self._exchangeQ.qsize():
                    await asyncio.sleep(0.1)
                    continue

                startTime = timer()

                response = requests.request(
                    'GET',
                    # CC.api_prefix + 'exchanges/list',  --> 거래내역 없는 거래소도 포함됨.
                    api_prefix + 'exchanges',
                    headers={'cache-control': 'no-cache'},
                )

                if 200 != response.status_code:
                    web_support.raiseHttpError(log, response.status_code, 'failed _getExchangeJobList')

                #print('_getExchangeJobList')

                jo = ujson.loads(response.text)
                #print(ujson.dumps(jo, ensure_ascii=False))

                for ent in jo:
                    self._exchangeQ.put(str(ent['id']))

            except Exception as inst:
                log.error('exception in _getExchangeJobList. msg:{}'.format(inst.args))

            elapsed = timer() - startTime
            if float(CoinScheduler.requestCostTime) > (elapsed):
                await asyncio.sleep(float(CoinScheduler.requestCostTime) - float(elapsed))

    
    # def _getExchangeInfo(self):
    #     response = requests.request(
    #         'GET',
    #         'https://api.coingecko.com/api/v3/exchanges/list',
    #         headers={'cache-control': 'no-cache'},
    #     )

    #     if 200 != response.status_code:
    #         web_support.raiseHttpError(log, response.status_code, 'failed _getExchangeJobList')

    #     jo = ujson.loads(response.text)
    #     #print(ujson.dumps(jo, ensure_ascii=False))

    #     for ent in jo:
    #         self._exchangeQ.put(str(ent['id']))

    
    # def _popCoinJob(self, cnt=10):
    #     outList = list()

    #     for _ in range(cnt):
    #         if self._coinQ.empty():
    #             break

    #         outList.append(
    #             {
    #                 'job':'coin',
    #                 'id':self._coinQ.get()
    #             }
    #         )
    #     return outList

    def _popTickerJob(self, cnt=10):
        outList = list()

        for _ in range(cnt):
            if self._exchangeQ.empty():
                break

            outList.append(
                {
                    'job':'ticker',
                    'id':self._exchangeQ.get()
                }
            )
        return outList


    def tick(self):
        self._tickCnt += 1

        if self._tickCnt >= 60:
            self._tickCnt = 0



    def allocJob(self, jobs:list):
        output = list()

        if self._fixedOnceQ.empty() is False:
            fixedJob = self._fixedOnceQ.get()
            output.append(fixedJob)
            return output

        jobCnt = 0

        
        while True:
            if self._fixedQ.empty() is True:
                break
            fixedJob = self._fixedQ.get()
            output.append(fixedJob)
            jobCnt += 1

        requestUnit = 5
        if jobCnt >= requestUnit:
            return output

        # if 'jobCoin' in jobs:
        #     output.extend( self._popCoinJob(requestUnit - jobCnt) )

        if 'jobTicker' in jobs:
            output.extend( self._popTickerJob(requestUnit - jobCnt) )

        return output
