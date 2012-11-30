# coding: utf8
'''
Created on 2012/11/30

@author: k_morishita
'''

import os
import sys
import time
from datacollector.import_hwdata import ImportHWData
from nnservice.settings import DEFAULT_LARNING_OPTION
from nnservice.nntrainer import NNTrainer
import logging
from nnservice.nnserver import make_thrift_infer_client
import subprocess
from thrift.transport.TTransport import TTransportException

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
ENV = {"PYTHONPATH": THIS_DIR+"/.."}

def run(typename_list):
    for typename in typename_list:
        start_machine_if_not_started(typename)
    for typename in typename_list:
        logging.info("run: [%s]" % typename)
        update_machine(typename)

def update_machine(typename):
    ip = ImportHWData(typename)
    ip.multiply = DEFAULT_LARNING_OPTION.get("data_multiply", 10)
    ip.noise_range = DEFAULT_LARNING_OPTION.get("data_noise_range", [0.9,1.1])
    updated, retinfo = ip.run_if_updated()
    if updated:
        logging.info("Data is Updated: run training")
        nnt = NNTrainer(typename)
        nnt.run()
        restart_machine(typename)
    else:
        logging.info("No Data Updated, skip")

def restart_machine(typename):
    try:
        client = make_thrift_infer_client(typename)
        client.halt()
    except TTransportException, e:
        logging.warn(repr(e))
    start_machine(typename)

def start_machine(typename):
    p = subprocess.Popen(["python", "%s/nnserver.py" % THIS_DIR, typename], env=os.environ)

def start_machine_if_not_started(typename):
    try:
        client = make_thrift_infer_client(typename)
        client.infer([0])
    except TTransportException, e:
        start_machine(typename)
    


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run(sys.argv[1:] or ["numbers"])
