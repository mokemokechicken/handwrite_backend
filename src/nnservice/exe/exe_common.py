# coding: utf8
'''
Created on 2012/12/04

@author: k_morishita
'''
from nnservice.thrift_util import make_thrift_infer_client
from thrift.transport.TTransport import TTransportException
import logging
import subprocess
import os

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

def restart_machine(typename, nn_id=None):
    stop_machine(typename)
    return start_machine(typename, nn_id)

def start_machine(typename=None, nn_id=None):
    args = ["python", "%s/nnserver.py" % THIS_DIR, nn_id or typename]
    subprocess.Popen(args, env=os.environ)
    return True

def stop_machine(typename):
    client = make_thrift_infer_client(typename)
    try:
        client.ping()
    except TTransportException:
        return False

    try:
        client.halt()
        return True
    except TTransportException, e:
        logging.warn(repr(e))
    return False

def start_machine_if_not_started(typename, nn_id=None):
    try:
        client = make_thrift_infer_client(typename)
        client.ping()
        return False
    except TTransportException:
        return start_machine(typename, nn_id)
