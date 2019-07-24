# -*- coding: utf-8 -*-

from easygrpc import Action
from .helloworld_pb2 import  HelloReply


class Hello(Action):

    async def execute(self, hello_request=None):
        return HelloReply(message=f'Hello {hello_request.name}!')

    # async def execute(self, hello_request=None):
    #     rec = await self.conn.fetchval("""
    #         SELECT row_to_json(t)
    #         FROM (
    #             SELECT
    #                 text as message
    #             FROM public.messages
    #             WHERE
    #                 id = $1
    #         ) as t
    #     """, 1)
    #     if rec is not None:
    #         return self.encode(rec, HelloReply)
    #     return None
