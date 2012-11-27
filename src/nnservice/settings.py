# coding: utf8
'''
Created on 2012/11/26

@author: k_morishita
'''

import os

THIS_DIR = os.path.abspath(os.path.dirname(__file__))


DATABASE = {
            "schema": "sqlite",
            "host": "",
            "name": "nnservice.db",
            "user": "",
            "pass": "",
            }

DATABASE_FILE_DIR = THIS_DIR

DATA_SERVER = "localhost:8000"

ENDPOINTS = {
             "hw_numbers": "http://%s/data/api/hw_numbers" % DATA_SERVER,
             
             }