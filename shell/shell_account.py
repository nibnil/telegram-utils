import asyncio

from socks import PROXY_TYPE_SOCKS5

API_ID = 1394345
API_HASH = 'd4c1615831f01e0342c35e829e1a0b76'
proxy = {'proxy_type': PROXY_TYPE_SOCKS5,
         'addr': '127.0.0.1',
         'port': 51115}


async def get_tg_token(aio_loop, phone_number):

    pass


def get_token(phone_number):
    aio_loop = asyncio.get_event_loop()
    try:
        aio_loop.run_until_complete(get_tg_token(aio_loop, phone_number))
    finally:
        if not aio_loop.is_closed():
            aio_loop.close()
