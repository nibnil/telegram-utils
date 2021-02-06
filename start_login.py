import logging

from shell.config import get_config, save_config
from shell.shell_account import get_token


if __name__ == '__main__':
    file_handler = logging.FileHandler('login.log')
    stream_handler = logging.StreamHandler()
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-s - %(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[file_handler, stream_handler])
    config = get_config()
    phone_number = config.get('PHONE_NUMBER')
    url = config.get('MONGODB_URL')
    db = config.get('MONGODB_DB')
    print(url, db)
    get_token(phone_number=phone_number, url=url, db=db, config=config)
    save_config(config)
