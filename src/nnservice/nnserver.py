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

from nnservice import settings

class InferServiceHandler(object):
    def __init__(self, typename=None, nn_id=None):
        if nn_id is None:
            self.service_obj = NNInfer.best_machine(typename=typename)
        else:
            self.build_machine(nn_id)

    def build_machine(self, nn_id):
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
    
    def update_nnmachine(self, nn_id):
        cur_id = self.nn_id
        if nn_id == 0:
            self.service_obj = NNInfer.best_machine(typename=self.typename)
        else:
            self.build_machine(nn_id)
        print "reload nn_id=%s" % self.nn_id
        return cur_id != self.nn_id
    
    def halt(self):
        print "halt"
        sys.exit(0)
    
    def _typename(self):
        return self.service_obj.typename
    typename = property(_typename)
    
    def _nn_id(self):
        return self.service_obj.model.id
    nn_id = property(_nn_id)

def get_endpoint(typename):
    return settings.SERVICE_ENDPOINTS.get(typename, ("127.0.0.1", 10000))

def make_thrift_infer_client(typename):
    host, port = get_endpoint(typename)
    # Make socket
    transport = TSocket.TSocket(host, port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Infer.Client(protocol)
    # Connect!
    transport.open()
    return client

def run_server(typename=None, nn_id=None):
    handler = InferServiceHandler(typename=typename, nn_id=nn_id)
    processor = Infer.Processor(handler)
    _, port = get_endpoint(handler.typename)
    transport = TSocket.TServerSocket(port=port)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
     
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    handler.server = server
     
    print "Starting infer server[%s:%d] port=%d ..." % (handler.typename, handler.nn_id, port)
    server.serve()
    print "done!"

if __name__ == "__main__":
    import sys
    typename = nn_id = None
    try:
        nn_id = len(sys.argv) > 1 and int(sys.argv[1]) or None
    except ValueError:
        typename = sys.argv[1]
    run_server(typename, nn_id)
