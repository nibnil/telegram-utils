import logging

from socks import PROXY_TYPE_SOCKS5

from shell.config import get_config, save_config
from shell.get_data import get_data

if __name__ == '__main__':
    file_handler = logging.FileHandler('get_data.log')
    stream_handler = logging.StreamHandler()
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-s - %(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[file_handler, stream_handler])
    config = get_config()
    config.update({'API_ID': 1394345})
    config.update({'API_HASH': 'd4c1615831f01e0342c35e829e1a0b76'})
    config.update({'PROXY': {'proxy_type': PROXY_TYPE_SOCKS5,
                             'addr': '127.0.0.1',
                             'port': 51115}})
    config.update({'MONGODB_URL': 'mongodb://192.168.31.22:27017'})
    config.update({'MONGODB_DB': 'telegram-data'})
    config.update({'PHONE_NUMBER': '8616533915575'})
    config.update({'INTERVAL': 5})
    config.update({'FILE_PATH': r'E:\nibnil'})
    config.update({'MSG_LIMIT': 100})
    # get_data(config)
    save_config(config)

