# coding: utf8
'''
Created on 2012/12/03

@author: k_morishita
'''

from nnservice.interface import NNBackend

from nnservice import thrift_util, settings
from nnservice.db import NNDatabase
from nnservice.repositories import NNMachineRepository
from nnservice.models import NNMachine
from nnservice.exe.exe_common import start_machine_if_not_started,\
    restart_machine, stop_machine
import logging

class BackendServiceHandler(object):
    def __init__(self):
        self.db = NNDatabase()

    def store_nnmachine(self, name, num_in, num_out, nnconfig, score, data):
        nn_model = NNMachine(name=name, num_in=num_in, num_out=num_out, nnconfig=nnconfig, score=score, data=data)
        repo = NNMachineRepository(self.db)
        repo.add(nn_model)
        return True
    
    def infer_server_ctl(self, cmd, typename, nn_id):
        cmd = cmd.lower()
        if cmd == "start":
            return start_machine_if_not_started(typename, nn_id)
        elif cmd == "restart":
            return restart_machine(typename, nn_id)
        elif cmd == "stop":
            return stop_machine(typename)
        else:
            logging.warn("Unknown command=[%s]" % cmd)
            return False

def run_backend_server():
    handler = BackendServiceHandler()
    thrift_util.run_server(NNBackend, handler, port=settings.BACKEND_PORT)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    run_backend_server()
