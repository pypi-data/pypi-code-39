# -*- coding: utf-8 -*-

from selenium.webdriver.remote.webdriver import WebDriver as WD, WebElement as WE
from selenium.common.exceptions import NoSuchElementException
from time import sleep

class SeleniumUtils:

    @staticmethod
    def _elmt(root, func, name, retryCnt, retryWaitSec):
        currentLoopCnt = 0

        while True:
            currentLoopCnt = currentLoopCnt + 1
            try:
                return func(root, name)
            except NoSuchElementException:
                
                sleep(retryWaitSec)

                if retryCnt > currentLoopCnt:
                    continue
                
                return None


    @staticmethod
    def _elmts(root, func, name, retryCnt, retryWaitSec):
        currentLoopCnt = 0

        while True:
            currentLoopCnt = currentLoopCnt + 1
            ret = func(root, name)
            if ret:
                return ret

            sleep(retryWaitSec)

            if retryCnt > currentLoopCnt:
                continue
                
            return None



    @staticmethod
    def _getFunc(node, funcName):
        if type(node) is WE:
            return WE.__dict__[funcName]
        else:
            return WD.__dict__[funcName]
            
            
    @staticmethod
    def elmt_class(root, className, retryCnt=3, retryWaitSec=3):
        cb = SeleniumUtils._getFunc(root, 'find_element_by_class_name')
        return SeleniumUtils._elmt(root, cb, className, retryCnt, retryWaitSec)


    @staticmethod
    def elmts_class(root, className, retryCnt=3, retryWaitSec=3):
        cb = SeleniumUtils._getFunc(root, 'find_elements_by_class_name')
        return SeleniumUtils._elmts(root, cb, className, retryCnt, retryWaitSec)


    @staticmethod
    def elmt_tag(root, tagName, retryCnt=3, retryWaitSec=3):
        cb = SeleniumUtils._getFunc(root, 'find_element_by_tag_name')
        return SeleniumUtils._elmt(root, cb, tagName, retryCnt, retryWaitSec)


    @staticmethod
    def elmts_tag(root, tagName, retryCnt=3, retryWaitSec=3):
        cb = SeleniumUtils._getFunc(root, 'find_elements_by_tag_name')
        return SeleniumUtils._elmts(root, cb, tagName, retryCnt, retryWaitSec)

    
    @staticmethod
    def elmt_name(root, name, retryCnt=3, retryWaitSec=3):
        cb = SeleniumUtils._getFunc(root, 'find_element_by_name')
        return SeleniumUtils._elmt(root, cb, name, retryCnt, retryWaitSec)


    @staticmethod
    def elmts_name(root, name, retryCnt=3, retryWaitSec=3):
        cb = SeleniumUtils._getFunc(root, 'find_elements_by_name')
        return SeleniumUtils._elmts(root, cb, name, retryCnt, retryWaitSec)


    @staticmethod
    def elmt_id(root, name, retryCnt=3, retryWaitSec=3):
        cb = SeleniumUtils._getFunc(root, 'find_element_by_id')
        return SeleniumUtils._elmt(root, cb, name, retryCnt, retryWaitSec)


    @staticmethod
    def elmts_id(root, name, retryCnt=3, retryWaitSec=3):
        cb = SeleniumUtils._getFunc(root, 'find_elements_by_id')
        return SeleniumUtils._elmts(root, cb, name, retryCnt, retryWaitSec)
