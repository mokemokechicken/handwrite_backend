# coding: utf8
'''Localのnn_idで表されるNNMachineをNNBackendに送信する

Created on 2012/12/03
@author: k_morishita
'''


import sys
import logging

from thrift.transport.TTransport import TTransportException
from nnservice.thrift_util import make_thrift_backend_client


def backend_server_ctl(cmd, typename, nn_id):
    try:
        client = make_thrift_backend_client()
        client.infer_server_ctl(cmd, typename, int(nn_id))
    except TTransportException, e:
        logging.error(repr(e))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    if (len(sys.argv) != 4):
        print "Usage: server_ctl.py <cmd> <typename> <nn_id>"
        print "cmd: {start,stop,restart}"
    else:
        backend_server_ctl(sys.argv[1], sys.argv[2], sys.argv[3])
