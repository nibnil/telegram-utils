import json
import logging
import os
import sys
from getopt import getopt

CONFIG_PATH = 'config.json'


def find_config():
    config_path = CONFIG_PATH
    if os.path.exists(config_path):
        return config_path
    config_path = os.path.join(os.path.dirname(__file__), '../', config_path)
    if os.path.exists(config_path):
        return config_path
    logging.info(f'FindConfig, config path({config_path})')
    return None


def get_config():
    try:
        short_opts = 'hv'
        long_opts = ['help', 'version']
        config_path = find_config()
        optlist, args = getopt(sys.argv[1:], short_opts, long_opts)
        config = dict()
        for key, value in optlist:
            if key == '-c':
                config_path = value
            if config_path:
                with open(config_path, 'r') as fd:
                    config = json.load(fd)
            else:
                config = dict()
        return config
    except Exception as ex:
        logging.exception(ex)
        sys.exit(2)


def save_config(config: dict):
    with open(CONFIG_PATH, 'w') as fd:
        json.dump(config, fd, indent=4)
