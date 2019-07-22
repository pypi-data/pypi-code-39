# -*- coding: utf-8 -*-
# nlp_support

import jpype
from konlpy.tag import Komoran
import logging
import re
import threading


log = logging.getLogger(__name__)



class NLPManager:
    instance_cnt = 0

    def __init__(self, userdic=None):
        self._komoran = Komoran(userdic=userdic)

        NLPManager.instance_cnt += 1
        log.debug('created NLPManager. count of NLPManager instances : {}'.format(NLPManager.instance_cnt))
        

    def __del__(self):
        log.debug('deleted NLPManager')

        NLPManager.instance_cnt -= 1
        log.debug('deleted NLPManager. count of NLPManager instances : {}'.format(NLPManager.instance_cnt))

    @staticmethod
    def split_sentences(text):
        try:
            text = text.replace('\n', '')
                
            all_sentences = []
            lines = [line for line in text.strip().splitlines() if line.strip()]
            
            for line in lines:
                sentences = re.split("(?<=[.?!])\s+", line)
                sentences = [s.strip() for s in sentences if s.strip()]
                all_sentences += sentences
        except Exception as inst:
            raise Exception('falied split_sentences. msg:{}'.format(inst.args))
        
        return all_sentences


    def getTags(self, text, filterFunc=None, tagsMax=3, cbKeywordList=None):
        jpype.attachThreadToJVM()

        splited_sentences = NLPManager.split_sentences(text)

        wordsMap = dict()

        try:
            for sentences in splited_sentences:
                result = self._komoran.pos(sentences)
                for v in result:
                    # NN:명사, OL:외국어
                    # if 'NN' in v[1] or 'OL' in v[1]:
                    # NNG 일반명사   NNP 고유명사
                    if 'NNP' == v[1] or 'NNG' == v[1]:
                        if v[0] in wordsMap:
                            wordsMap[str(v[0])] = int(wordsMap[str(v[0])]) + 1
                        else:
                            wordsMap[str(v[0])] = 1
                            
        except Exception as inst:
            raise Exception('falied komoran.pos() msg:{} sencence:{}'.format(inst.args, sentences))

        wordsList = list()
        for key, value in wordsMap.items():
            wordsList.append([value, key])

        wordsList.sort(reverse=True)

        if cbKeywordList is not None:
            cbKeywordList(wordsList)

        if filterFunc is not None:
            filterFunc(wordsList)

        slicedList = wordsList[int(0):int(tagsMax)]

        returnValue = list()
        for v in slicedList:
            returnValue.append(v[1])

        return returnValue


    @staticmethod
    def getTagsStatic(sentences, userdic=None, filterFunc=None, tagsMax=3):
        sentences = sentences.replace('\n', '')
        komoran = Komoran(userdic=userdic)
        
        wordsMap = dict()
        # result = kkma.pos(sentences)
        result = komoran.pos(sentences)
        for v in result:
            # NN:명사, OL:외국어
            # if 'NN' in v[1] or 'OL' in v[1]:
            # NNG 일반명사   NNP 고유명사
            if 'NNP' == v[1] or 'NNG' == v[1]:
                if v[0] in wordsMap:
                    wordsMap[str(v[0])] = int(wordsMap[str(v[0])]) + 1
                else:
                    wordsMap[str(v[0])] = 1

        wordsList = list()
        for key, value in wordsMap.items():
            wordsList.append([value, key])

        if filterFunc is not None:
            filterFunc(wordsList)

        wordsList.sort(reverse=True)
        slicedList = wordsList[int(0):int(tagsMax)]

        returnValue = list()
        for v in slicedList:
            returnValue.append(v[1])

        return returnValue

if __name__ == "__main__":
    # static test
    # print(NLPManager.getTagsStatic('나는 아무런 생각이 없다. 왜냐하면 아무런 생각이 없기 때문이다.'))

    nlp = NLPManager()
    print( nlp.getTags('뭐타야하냐면 \n아톰') )

    # from utail_base import string_support
    # nlp = NLPManager()
    # tm = string_support.TextManip()
    # tm.makeDic(
    #         log, 
    #         ('exceptNormal', "./user_dic_except.txt"),
    #         ('exceptHotKeywords', "./user_dic_except_hotkeywords.txt"),
    #     )




class NLPManagerPoolBaseClass:
	pass

class NLPManagerPoolSingleton(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(NLPManagerPoolSingleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]


class NLPManagerPool(NLPManagerPoolBaseClass, metaclass=NLPManagerPoolSingleton):
    def __init__(self):
        log.info('Create NLPManagerPool ... ')
        self._lock = threading.Lock()

        self._map = dict()


    def createPool(self, threadName, userDic=None):
        #with self._lock:
        self._map[threadName] = NLPManager(userdic=userDic)

    def get(self, threadName):
        # with self._lock:
        return self._map[threadName]