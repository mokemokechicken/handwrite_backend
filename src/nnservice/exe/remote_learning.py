# coding: utf8
'''学習データを外部から取得して、学習を行い、学習結果のNNMachineをNNBackendに送信する

Created on 2012/12/03
@author: k_morishita
'''

import sys
import logging

from thrift.transport.TTransport import TTransportException

from datacollector.import_hwdata import ImportHWData
from nnservice.settings import DEFAULT_LARNING_OPTION
from nnservice.nntrainer import NNTrainer
from nnservice.thrift_util import make_thrift_backend_client
from nnservice.repositories import NNMachineRepository
from nnservice.db import NNDatabase

def run(typename_list):
    for typename in typename_list:
        logging.info("run: [%s]" % typename)
        update_machine(typename)

def update_machine(typename, force=False):
    ip = ImportHWData(typename)
    ip.multiply = DEFAULT_LARNING_OPTION.get("data_multiply", 10)
    ip.noise_range = DEFAULT_LARNING_OPTION.get("data_noise_range", [0.9,1.1])
    updated, retinfo = ip.run_if_updated()
    if updated:
        logging.info("Data is Updated: run training")
        nnt = NNTrainer(typename)
        nnt.run(callback=send_to_remote_backend)
    else:
        logging.info("No Data Updated, skip")

def send_to_remote_backend(nn_model=None, nn_id=None):
    try:
        if nn_model is None and nn_id is None:
            return
        if nn_model is None:
            nn_model = NNMachineRepository(NNDatabase()).get_by_id(nn_id)
        client = make_thrift_backend_client()
        client.store_nnmachine(nn_model.name, nn_model.num_in, nn_model.num_out,
                               nn_model.nnconfig, nn_model.score, nn_model.data)
    except TTransportException, e:
        logging.error(repr(e))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    args = sys.argv[1:]
    run(args or ["numbers"])
