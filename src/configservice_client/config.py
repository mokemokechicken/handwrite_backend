# coding: utf8
'''
Created on 2012/12/12

@author: k_morishita
'''


import copy
import time

from configservice_client.client import ConfigClient

CONFIG_SERVER_URL = "http://localhost:8000/config"

_CONFIG_CACHE = {}
_CONFIG_CACHE_TIME = {}
CACHE_EXPIRE = 10

def load_config(charset_type):
    if charset_type not in _CONFIG_CACHE or _CONFIG_CACHE_TIME[charset_type]+CACHE_EXPIRE < time.time():
        cc = ConfigClient(CONFIG_SERVER_URL)
        _CONFIG_CACHE[charset_type] = cc.get_config(charset_type)
        _CONFIG_CACHE_TIME[charset_type] = time.time()
    return copy.copy(_CONFIG_CACHE[charset_type])


