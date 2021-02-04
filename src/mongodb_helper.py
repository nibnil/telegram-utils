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
                             filter_key: list,
                             set_key: list = None,
                             set_on_insert_key: list = None):
        try:
            collection = self._db[col]
            requests = list()
            for d in data:
                filter_ = dict()
                for key in filter_key:
                    filter_.update({key: d.get(key)})
                set_ = dict()
                set_on_insert = dict()
                if set_key:
                    for key in set_key:
                        set_[key] = d.get(key)
                if set_on_insert_key:
                    for key in set_on_insert_key:
                        set_on_insert[key] = d.get(key)
                if set_key and set_on_insert_key:
                    update = {'$set': set_,
                              '$setOnInsert': set_on_insert}
                elif set_key:
                    update = {'$set': set_}
                elif set_on_insert_key:
                    update = {'$setOnInsert': set_on_insert}
                else:
                    return None
                request = UpdateOne(filter=filter_, update=update, upsert=True)
                requests.append(request)
            if requests:
                result = await collection.bulk_write(requests=requests)
                logging.info(f'DoBulkUpsert, '
                             f'col({col}), total({len(data)}), '
                             f'modified({result.modified_count}), upsert({result.upsert_count})')
                return result
            else:
                logging.info(f'DoBulkUpsert, '
                             f'requests is empty, filter_key({filter_key})')
                return None
        except Exception as ex:
            logging.exception(ex)
            return None

    async def do_find_one(self, col: str, filter_: dict, sort: list = None):
        try:
            collection = self._db[col]
            document = await collection.find_one(filter=filter_, sort=sort)
            if document:
                logging.info(f'DoFindOne, '
                             f'col({col}), doc({document.get("_id")})')
            else:
                logging.info(f'DoFindOne, '
                             f'col({col}), filter({filter_}), doc({document})')
            return document
        except Exception as ex:
            logging.exception(ex)
            return None


