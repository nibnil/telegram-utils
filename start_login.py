import logging

from shell.shell_account import get_token


if __name__ == '__main__':
    file_handler = logging.FileHandler('login.log')
    stream_handler = logging.StreamHandler()
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-s - %(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[file_handler, stream_handler])

    get_token(phone_number='8616533915575', url='mongodb://192.168.31.22:27017')
