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

NNMACHINE_TYPES = {
                       "hw_numbers": [
                           #{"type": "dbn", "hiddens": [50,50], "suffix": "", "option": {}},
                           {"type": "sda", "hiddens": [9], "suffix": "", "option": {}},
                           {"type": "sda", "hiddens": [8], "suffix": "", "option": {}},
                           {"type": "sda", "hiddens": [7], "suffix": "", "option": {}},
                           {"type": "sda", "hiddens": [6], "suffix": "", "option": {}},
                           {"type": "sda", "hiddens": [5], "suffix": "", "option": {}},
                           {"type": "sda", "hiddens": [4], "suffix": "", "option": {}},
                           {"type": "sda", "hiddens": [3], "suffix": "", "option": {}},
#                           {"type": "sda", "hiddens": [25], "suffix": "", "option": {}},
#                           {"type": "sda", "hiddens": [50], "suffix": "", "option": {}},
#                           {"type": "sda", "hiddens": [100], "suffix": "", "option": {}},
                       ],
                  }
DEFAULT_LARNING_OPTION = {
    "pretraining_epochs": 300,
    "batch_size": 10,
    "pretrain_lr": 0.01,
    "k": 1,
    "training_epochs": 1000,
    "finetune_lr": 0.1,
    "improvement_threshold": 0.995,
    "patience_increase": 2,
    "patience_first": 700,
}
