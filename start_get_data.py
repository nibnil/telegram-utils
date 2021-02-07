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
    get_data(config)
    save_config(config)

