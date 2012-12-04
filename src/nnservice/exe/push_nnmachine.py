# coding: utf8
'''Localのnn_idで表されるNNMachineをNNBackendに送信する

Created on 2012/12/03
@author: k_morishita
'''


import sys
import logging

from thrift.transport.TTransport import TTransportException

from nnservice.thrift_util import make_thrift_backend_client
from nnservice.repositories import NNMachineRepository
from nnservice.db import NNDatabase

def run(args):
    for nn_id in args:
        send_to_remote_backend(nn_id)

def send_to_remote_backend(nn_id):
    try:
        nn_model = NNMachineRepository(NNDatabase()).get(nn_id)
        client = make_thrift_backend_client()
        client.store_nnmachine(nn_model.name, nn_model.num_in, nn_model.num_out,
                               nn_model.nnconfig, nn_model.score, nn_model.data)
    except TTransportException, e:
        logging.error(repr(e))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    args = sys.argv[1:]
    run(args)
