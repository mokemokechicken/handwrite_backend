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

class BackendServiceHandler(object):
    def __init__(self):
        self.db = NNDatabase()

    def store_nnmachine(self, name, num_in, num_out, nnconfig, score, data):
        nn_model = NNMachine(name=name, num_in=num_in, num_out=num_out, nnconfig=nnconfig, score=score, data=data)
        repo = NNMachineRepository(self.db)
        repo.add(nn_model)
        return True

def run_server():
    handler = BackendServiceHandler()
    thrift_util.run_server(NNBackend, handler, port=settings.BACKEND_PORT)

def make_thrift_backend_client():
    host, port = settings.BACKEND_HOST, settings.BACKEND_PORT
    return thrift_util.make_thrift_infer_client(NNBackend, host, port)

if __name__ == '__main__':
    run_server()
