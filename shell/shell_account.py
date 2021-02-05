import asyncio
import logging
from datetime import datetime

from socks import PROXY_TYPE_SOCKS5

from src.entity import TgAccountEntity, DOMAIN_DEFAULT, ACCOUNT_STATUS_DEFAULT
from src.mongodb_helper import MongodbHelper
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = 1394345
API_HASH = 'd4c1615831f01e0342c35e829e1a0b76'
proxy = {'proxy_type': PROXY_TYPE_SOCKS5,
         'addr': '127.0.0.1',
         'port': 51115}


async def get_tg_token(aio_loop, phone_number, url, db):
    mongodb = MongodbHelper(url=url, db=db)
    client = TelegramClient(phone_number,
                            API_ID, API_HASH, loop=aio_loop, proxy=proxy)
    try:
        await client.connect()
    except Exception as ex:
        logging.error('GetTgToken', ex)
        return
    send_code = await client.send_code_request(phone=phone_number)
    logging.info('GetTgToken, input code')
    value = input()
    me = await client.sign_in(code=value)
    account_id = str(me.id)
    username = me.username
    target = me.phone
    token = StringSession.save(client.session)
    tg_account = TgAccountEntity(account_id=account_id,
                                 domain=DOMAIN_DEFAULT,
                                 target=target,
                                 username=username,
                                 token=token,
                                 account_status=ACCOUNT_STATUS_DEFAULT,
                                 create_time=datetime.now(),
                                 update_time=datetime.now())
    data = [tg_account.to_dict()]
    await mongodb.do_bulk_upsert(col=TgAccountEntity.TABLE,
                                 data=data,
                                 filter_key=['account_id', 'target', 'domain', ],
                                 set_key=['domain', 'target', 'username', 'token', 'account_status', 'update_time'],
                                 set_on_insert_key=['account_id', 'create_time'])
    await client.disconnect()


def get_token(phone_number, url='mongodb://127.0.0.1:27017', db='telegram-data'):
    aio_loop = asyncio.get_event_loop()
    try:
        aio_loop.run_until_complete(get_tg_token(aio_loop, phone_number, url, db))
    finally:
        if not aio_loop.is_closed():
            aio_loop.close()
