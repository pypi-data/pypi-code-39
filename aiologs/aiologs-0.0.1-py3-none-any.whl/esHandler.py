from elasticsearch_async import AsyncElasticsearch
from datetime import datetime
from aiologs import LoggerConfig
import asyncio



async def addlogs(data):
    """
    192.168.88.103
    """
    assert len(LoggerConfig.targetDB)>0
    client = AsyncElasticsearch(hosts=LoggerConfig.targetDB)
    task=[]
    for item in data:
        task.append(client.index(index=f'aiologs-{datetime.now().strftime("%Y.%m.%d")}' ,doc_type='_doc' ,id=None,body=item))
    await asyncio.gather(*task)
    
    
   