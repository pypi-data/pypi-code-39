# -*- coding: utf-8 -*-
from novelTools.novelSpider import novelSpider
from novelTools.novelParser import novelParser
from novelTools.novelORM import novelORM, Site, Novel
from sqlalchemy import func
import time

class novelDownloader(novelSpider, novelParser, novelORM):
    def __init__(self, config):
        novelSpider.__init__(self)
        novelParser.__init__(self)
        novelORM.__init__(self, config)
        self.siteNovelUrl = 'https://www.qu.la/book/'

    def getCharptContent(self, novelId=None, charptNum=None):
        '''
        @desc：下载某书章节内容
        @param：novelId 小说id
        @param：charptNum 章节数量
        '''
        if novelId == None and charptNum == None:
            novelId = self.session.query(Site).count()
            if novelId == 0 :
                return None
            charpts = self.session.query(Novel).filter_by(
                charptContent=''
            ).all()
        elif novelId == None and type(charptNum) == int:
            charpts = self.session.query(Novel).filter_by(
                charptContent=''
            ).limit(charptNum)
        elif type(novelId) == int and charptNum == None:
            charpts = self.session.query(Novel).filter_by(
                novelId=novelId,
                charptContent=''
            ).all()
        elif type(novelId) == int and type(charptNum) == int:
            charpts = self.session.query(Novel).filter_by(
                novelId=novelId,
                charptContent=''
            ).limit(charptNum)

        for charpt in charpts:
            charptHtml = self.getHtml(charpt.charptUrl)
            charptContent = self.parseCharptContent(charptHtml, charpt.charptUrl)
            self.session.query(Novel).filter_by(id=charpt.id).update({
                Novel.charptContent: charptContent
            })
            self.session.commit()
            time.sleep(1)

    def getCharptList(self, novelNum):
        '''
        @desc：下载若干本小说章节列表、相应小说信息
        @param：novelNum 小说数量
        '''
        curNovelNum = self.session.query(Site).count()
        for novelId in range(curNovelNum+1,curNovelNum+1+novelNum):
            novelHomeUrl = self.siteNovelUrl + str(novelId)
            novelHomeHtml = self.getHtml(novelHomeUrl)
            novelInfo = self.parseNovelData(novelHomeHtml, novelHomeUrl)
            self.session.add(Site(
                novelName = novelInfo['novelName'],
                novelHomeUrl = novelHomeUrl,
                novelAuthor = novelInfo['novelAuthor'],
                novelIntro = novelInfo['novelIntro'],
                novelType = 'unknown',
                novelImg= novelInfo['novelImg'],
                lastUpdate= novelInfo['lastUpdate'],
                novelIsFinished = 0,
                charptIsFinished = 0
            ))
            charpts = self.parseCharptList(novelHomeHtml, novelHomeUrl)
            for charpt in charpts:
                self.session.add(Novel(
                    novelId = novelId,
                    charptName = charpt['charptName'],
                    charptUrl = charpt['charptUrl'],
                    charptContent = charpt['charptContent']
                ))
            self.session.commit()
            time.sleep(1)
