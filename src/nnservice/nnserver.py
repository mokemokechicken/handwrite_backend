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


class InferServiceHandler(object):
    def __init__(self):
        self.service_obj = NNInfer.best_machine()
    
    def infer(self, xs):
        print "infer"
        if self.service_obj.model.num_in != len(xs):
            print "error length %d != %d" % (self.service_obj.model.num_in, len(xs))
            return []
        y, ys = self.service_obj.infer(xs)
        return ys

if __name__ == "__main__":
    handler = InferServiceHandler()
    processor = Infer.Processor(handler)
    transport = TSocket.TServerSocket(port=9999)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
     
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
     
    print "Starting python server..."
    server.serve()
    print "done!"
