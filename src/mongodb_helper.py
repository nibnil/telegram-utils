import logging

import motor.motor_asyncio
from pymongo import UpdateOne


class MongodbHelper:

    def __init__(self, url='mongodb://127.0.0.1:27277', db='telegram-data'):
        self._mongodb = motor.motor_asyncio.AsyncIOMotorClient(url)
        self._db = self._mongodb[db]

    def __del__(self):
        del self._db
        del self._mongodb

    async def do_bulk_upsert(self,
                             col: str,
                             data: list,
                             filter_key: list,):

