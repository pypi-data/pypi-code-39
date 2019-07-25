import aiofiles
import datetime
import os
import socket
import uvloop
import asyncio
from enum import Enum
import ujson
from threading import Thread

class LoggerConfig():
    """
    projectName:项目名称，用于区分文件夹
    isJsonSerialize：是否进行json序列化，默认是标签模式
    ifConsole：是否进行print
    ifFile：是否记录日志文件
    fileName：文件名称，默认是按照时间进行创建
    path：文件保存路径
    asyncWrite:是否直接写入数据库
    dbtype：存入数据库类型，0es，1mongodb
    targetDB：数据库库链接 []里面放链接字符串
    """
    ifFile = 0
    ifConsole = 0
    fileName = ""
    path = "./"
    projectName = "undefine"
    asyncWrite = 0
    dbtype = 0
    targetDB = []
    env = "develop"
    ip="127.0.0.1"

    @staticmethod
    def addConfig(config):
        if "ifFile" in config:
            LoggerConfig.ifFile = config["ifFile"]
        if "ifConsole" in config:
            LoggerConfig.ifConsole = config["ifConsole"]
        if "fileName" in config:
            LoggerConfig.fileName = config["fileName"]
        if "path" in config:
            LoggerConfig.path = config["path"]
        if "projectName" in config:
            LoggerConfig.projectName = config["projectName"]
        if "asyncWrite" in config:
            LoggerConfig.asyncWrite = config["asyncWrite"]
        if "dbtype" in config:
            LoggerConfig.dbtype = config["dbtype"]
        if "targetDB" in config:
            LoggerConfig.targetDB = config["targetDB"]
        if "env" in config:
            LoggerConfig.env = config["env"]
        #获取本机IP
        ip="127.0.0.1"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        LoggerConfig.ip=ip

class LogLevel(Enum):
    """
    错误日志
    """
    INFO = 1,
    WARNING = 2,
    ERROR = 3,
    CRITICAL = 4,
    DEBUG = 5

    @staticmethod
    def getEnumName(logLevel):
        if LogLevel.WARNING == logLevel:
            return "WARNING"
        elif LogLevel.ERROR == logLevel:
            return "ERROR"
        elif LogLevel.CRITICAL == logLevel:
            return "CRITICAL"
        elif LogLevel.DEBUG == logLevel:
            return "DEBUG"
        else:
            return "INFO"



class Logger():
    """
    初始化log服务
    """

    def __init__(self,isJsonSerialize=1):
        """
        projectName:项目名称，用于区分文件夹
        isJsonSerialize：是否进行json序列化，默认是标签模式
        ifConsole：是否进行print
        ifFile：是否记录日志文件
        fileName：文件名称，默认是按照时间进行创建
        path：文件保存路径
        asyncWrite:是否直接写入数据库
        dbtype：存入数据库类型，0es，1mongodb
        targetDB：数据库库链接 {host:"",port:""}
        """
        self.isJsonSerialize = isJsonSerialize
        self.tasks=[]
        self.datas=[]

    async def info(self, module='', category='', sub_category='', msg=None, extra=None, filter1="", filter2=""):
        """
        记录日志
        module:模块 用于区分日志的模块
        category:大分类 用于区分日志
        sub_category:小分类 用于区分日志
        msg:日志内容
        extra:扩展信息
        filter1: 过滤条件1
        filter2: 过滤条件2
        """
        await self.log(module=module, category=category, sub_category=sub_category, msg=msg,
                 extra=extra, filter1=filter1, filter2=filter2, logLevel=LogLevel.INFO)

    async def warning(self, module='', category='', sub_category='', msg=None, extra=None, filter1="", filter2=""):
        """
        记录日志
        module:模块 用于区分日志的模块
        category:大分类 用于区分日志
        sub_category:小分类 用于区分日志
        msg:日志内容
        extra:扩展信息
        filter1: 过滤条件1
        filter2: 过滤条件2
        """
        await self.log(module=module, category=category, sub_category=sub_category, msg=msg, extra=extra,
                 filter1=filter1, filter2=filter2, logLevel=LogLevel.WARNING)

    async def error(self, module='', category='', sub_category='', msg=None, extra=None, filter1="", filter2=""):
        """
        记录日志
        module:模块 用于区分日志的模块
        category:大分类 用于区分日志
        sub_category:小分类 用于区分日志
        msg:日志内容
        extra:扩展信息
        filter1: 过滤条件1
        filter2: 过滤条件2
        """
        await self.log(module=module, category=category, sub_category=sub_category, msg=msg,
                 extra=extra, filter1=filter1, filter2=filter2, logLevel=LogLevel.ERROR)

    async def critical(self, module='', category='', sub_category='', msg=None, extra=None, filter1="", filter2=""):
        """
        记录日志
        module:模块 用于区分日志的模块
        category:大分类 用于区分日志
        sub_category:小分类 用于区分日志
        msg:日志内容
        extra:扩展信息
        filter1: 过滤条件1
        filter2: 过滤条件2
        """
        await self.log(module=module, category=category, sub_category=sub_category, msg=msg, extra=extra,
                 filter1=filter1, filter2=filter2, logLevel=LogLevel.CRITICAL)

    async def debug(self, module='', category='', sub_category='', msg=None, extra=None, filter1="", filter2=""):
        """
        记录日志
        module:模块 用于区分日志的模块
        category:大分类 用于区分日志
        sub_category:小分类 用于区分日志
        msg:日志内容
        extra:扩展信息
        filter1: 过滤条件1
        filter2: 过滤条件2
        """
        await self.log(module=module, category=category, sub_category=sub_category, msg=msg,
                 extra=extra, filter1=filter1, filter2=filter2, logLevel=LogLevel.DEBUG)

    async def log(self, module='', category='', sub_category='', msg=None, extra=None, filter1="", filter2="", logLevel=LogLevel.INFO, serializeEncoder=None):
        """
        记录日志
        module:模块 用于区分日志的模块
        category:大分类 用于区分日志
        sub_category:小分类 用于区分日志
        msg:日志内容
        extra:扩展信息
        filter1: 过滤条件1
        filter2: 过滤条件2
        logLevel:日志等级
        serializeEncoder:序列化方式
        """

        if serializeEncoder is not None:
            self.tasks.append(serializeEncoder(
                module, category, sub_category, msg, extra,filter1,filter2, logLevel))
        elif self.isJsonSerialize == 1:
            self.tasks.append(self._jsonSerialize(
                module, category, sub_category, msg, extra, filter1,filter2,logLevel))
        else:
            self.tasks.append(self._serialize(
                module, category, sub_category, msg, extra, filter1,filter2,logLevel))
        self.datas.append({
            "addtime": datetime.datetime.now(),
            "logLevel": LogLevel.getEnumName(logLevel),
            "module": module,
            "category": category,
            "sub_category": sub_category,
            "msg":msg,
            "extra": extra,
            "filter1": filter1,
            "filter2": filter2,
            "ip":LoggerConfig.ip,
            "peoject":LoggerConfig.projectName,
            "env":LoggerConfig.env,
        })
        

    def _serialize(self, module='', category='', sub_category='', msg=None, extra=None, filter1="", filter2="", logLevel=LogLevel.INFO):
        logStr = f'<addtime>{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</addtime><logLevel>{LogLevel.getEnumName(logLevel)}</logLevel>'
        logStr = f'{logStr}<module>{module}</module><category>{category}</category><sub_category>{sub_category}</sub_category><msg>{msg}</msg><extra>{extra}</extra>'
        logStr = f'{logStr}<msg>{ujson.dumps(msg)}</msg><extra>{ujson.dumps(extra)}</extra>'
        logStr = f'{logStr}<filter1>{filter2}</filter1><filter2>{filter2}</filter2>'
        logStr = f'{logStr}<ip>{LoggerConfig.ip}</ip><peoject>{LoggerConfig.projectName}</peoject><env>{LoggerConfig.env}</env>'
        return logStr

    def _jsonSerialize(self, module='', category='', sub_category='', msg=None, extra=None, filter1="", filter2="", logLevel=LogLevel.INFO):
        logDic = {
            "addtime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "logLevel": LogLevel.getEnumName(logLevel),
            "module": module,
            "category": category,
            "sub_category": sub_category,
            "msg": ujson.dumps(msg),
            "extra": ujson.dumps(extra),
            "filter1": filter1,
            "filter2": filter2,
            "ip":LoggerConfig.ip,
            "peoject":LoggerConfig.projectName,
            "env":LoggerConfig.env,
        }
        return ujson.dumps(logDic)

    def __del__(self):
        run_loop_thread = Thread(target=addFileByThread, args=(self.tasks,self.datas)) # 将次事件循环运行在一个线程中，防止阻塞当前主线程
        run_loop_thread.start() # 运行线程，同时协程事件循环也会运行


async def addFile(tasks, datas):
    if tasks:
        if LoggerConfig.ifFile == 1:
            assert os.path.exists(LoggerConfig.path)
            rootPath = LoggerConfig.path+"/"+LoggerConfig.projectName
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            fileNameTemp = LoggerConfig.fileName
            if not fileNameTemp:
                fileNameTemp = datetime.datetime.now().strftime(
                    "%Y-%m-%d_%H-%M-%S")
            fileNameTemp = f'{fileNameTemp}_{LoggerConfig.env}'
            async with aiofiles.open(f'{rootPath}/{fileNameTemp}.txt', 'a') as f:
                for task in tasks:
                    await f.write(task+"\n")
        
        if LoggerConfig.ifConsole == 1:
            for task in tasks:
                print(task)
    if datas:
        if LoggerConfig.asyncWrite == 1:
            if LoggerConfig.dbtype == 0:
                import  aiologs.esHandler as esHandler
                await esHandler.addlogs(datas)
            else:
                import aiologs.mongoHandler as mongoHandler
                await mongoHandler.addlogs(datas)


async def testsss(a,b):
    for i in a:
        print(i)
    print("=========================================================")
    for i in b:
        print(i)

def addFileByThread(tasks,data):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(addFile(tasks,data))
