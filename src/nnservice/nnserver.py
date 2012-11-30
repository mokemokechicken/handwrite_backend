# coding: utf8
'''
Created on 2012/11/29

@author: k_morishita
'''

from __future__ import absolute_import

from nnservice.interface import Infer
#from nnservice.interface.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from nnservice.nninfer import NNInfer
from nnservice.repositories import NNMachineRepository
from nnservice.db import NNDatabase
import time


class InferServiceHandler(object):
    def __init__(self, nn_id=None):
        if nn_id is None:
            self.service_obj = NNInfer.best_machine()
        else:
            nn_model = NNMachineRepository(NNDatabase()).get(nn_id)
            self.service_obj = NNInfer(nn_model).setup_nnmachine()
    
    def infer(self, xs):
        if self.service_obj.model.num_in != len(xs):
            print "error length %d != %d" % (self.service_obj.model.num_in, len(xs))
            return []
        start_time = time.time()
        y, ys = self.service_obj.infer(xs)
        print "infer %s (%f msec)" % (y, (time.time() - start_time)*1000) 
        return ys

if __name__ == "__main__":
    import sys
    nn_id = len(sys.argv) > 1 and int(sys.argv[1]) or None
    handler = InferServiceHandler(nn_id)
    processor = Infer.Processor(handler)
    transport = TSocket.TServerSocket(port=9999)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
     
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
     
    print "Starting python server..."
    server.serve()
    print "done!"
