# coding: utf8
'''
Created on 2012/11/30

@author: k_morishita
'''

import sys
from datacollector.import_hwdata import ImportHWData
from nnservice.settings import DEFAULT_LARNING_OPTION
from nnservice.nntrainer import NNTrainer
import logging
from nnservice.exe.exe_common import start_machine_if_not_started,\
    restart_machine


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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    run(sys.argv[1:] or ["numbers"])
