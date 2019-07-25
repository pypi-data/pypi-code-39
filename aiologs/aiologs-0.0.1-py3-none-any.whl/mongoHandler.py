import motor.motor_asyncio
from aiologs import LoggerConfig


async def addlogs(data=[]):
    #"mongodb://ynt:ynt123456@192.168.88.103:27016/admin"
    if not data:
        return
    dataBaseName = 'aiologs'
    collectName = f'{LoggerConfig.projectName}_{LoggerConfig.env}'
    assert len(LoggerConfig.targetDB)>0
    config=LoggerConfig.targetDB[0]
    client = motor.motor_asyncio.AsyncIOMotorClient(config)
    db = client[dataBaseName]
    collection = db[collectName]
    await collection.insert_many(data)
