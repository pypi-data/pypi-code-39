# -*- coding: utf-8 -*-
import hashlib
import logging
import os

log = logging.getLogger(__name__)

class UtFileHashFilter:
    """
    필터링 되지않은 파일들은 default 그룹에 속합니다
    """
    def __init__(self):
        # _dic    key : group name / value : filter string's list
        self._dic = dict()
        self._exclude = []
        self._defaultGrName = 'default'

    """
    기본 기룹 이외에 별도의 그룹을 생성합니다.
    """
    def appendGroup(self, grName, *filterString):
        if grName == self._defaultGrName:
            raise Exception('reserved grName')

        self._dic[grName] = list()
        
        for i in range(len(filterString)):
            self._dic[grName].append(filterString[i])


    def appendExclude(self, stringValue):
        self._exclude.append(stringValue)


"""
파일 이름으로 그루핑합니다.
 예> 파일명에 'apple' 문자열이 포함된 파일이라면 'a'그룹
     'banana' 를 포함한 파일은 'b'그룹
     으로 지정하려 한다면 다음과 같이 필터를 생성합니다.
     필터링되지 않은 파일들은 모두 기본(default) 그룹에 속하게 됩니다.

     from utail_base import UtFileHashFilter as utFilter, UtFileHash as utHash
     
     filter = utfile_hash.UtFileHashFilter()
     filter.appendGroup('a', 'apple')
     filter.appendGroup('b', 'banana')

     myFileHash = utfile_hash.UtFileHash(dir='/Users/chase/Documents/work/utail/py37/svc_scrap/svc_scrap/scrap_scripts',
     groupFilter=filter)

     # 확인
     myFileHash.print()
"""
class UtFileHash:
    def __init__(self, directory,
      groupFilter: UtFileHashFilter=None,
     ):
        self._dicDefault = dict()
        self._dicUser = None

        self._dir = directory
        self._setDistributor(groupFilter)

    def clear(self):
        self._dicDefault.clear()
        if self._dicUser is not None:
            self._dicUser.clear()

    def _setDistributor(self, groupFilter):
        file_list = os.listdir(self._dir)

        for fn in file_list:
            path = self.get_path(fn)
            if os.path.isfile(path) is not True:
                continue

            if fn[0] is '.':
                # hidden file.
                continue

            excludingFile = False
            for excludeWord in groupFilter._exclude:
                if excludeWord in fn:
                    excludingFile = True
                    break

            if excludingFile is True:
                continue

            foundGrName = ''

            for registedGrName, registedFilterStringList in groupFilter._dic.items():
                for fs in registedFilterStringList:
                    if fs in fn:
                        foundGrName = registedGrName
                        break
                else:
                    continue # only executed if the inner loop did NOT break
                break # only executed if the inner loop DID break

            #print('grName: {}, filePath:{}'.format(foundGrName, path) )
            if '' == foundGrName:
                dic = self._dicDefault
            else:
                if self._dicUser is None:
                    self._dicUser = dict()
                if foundGrName not in self._dicUser:
                    self._dicUser[foundGrName] = dict()
                dic = self._dicUser[foundGrName]

            f = open(path, 'rb')
            data = f.read()
            f.close()
            dic[fn] = hashlib.md5(data).hexdigest()

    def get_path(self, fileName):
        return self._dir + '/' + fileName

    def exists(self, fileName):
        return fileName in self._dicDefault

    def makeFileHash(self, fileName, groupName=None):
        path = os.path.join(self._dir, fileName)
        if os.path.isfile(path) is not True:
            log.error('not found file. path:{}'.format(path))
            return None

            # hidden file.
        if fileName is '.':
            return None

        f = open(path, 'rb')
        data = f.read()
        f.close()

        if groupName is None:
            madeHash = self._dicDefault[fileName] = hashlib.md5(data).hexdigest()
        else:
            if self._dicUser is None:
                self._dicUser = dict()
            if groupName not in self._dicUser:
                self._dicUser[groupName] = dict()

            madeHash = self._dicUser[groupName][fileName] = hashlib.md5(data).hexdigest()
        return madeHash
      

    def getDigest(self, fileName) ->str:
        if fileName not in self._dicDefault:
            return None
        return self._dicDefault[fileName]

    def getUserDic(self, groupName):
        if self._dicUser is None:
            return None
        if groupName not in self._dicUser:
            return None
        return self._dicUser[groupName]


    def print(self):
        print('========= default =======')
        print(self._dicDefault)
        print('========= user =======')
        print(self._dicUser)

    
 


    
    