# coding: utf8
'''
Created on 2012/12/03

@author: k_morishita
'''

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

def make_thrift_infer_client(klass, host,  port):
    # Make socket
    transport = TSocket.TSocket(host, port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = klass.Client(protocol)
    # Connect!
    transport.open()
    return client

def run_server(klass, handler, host=None, port=None):
    processor = klass.Processor(handler)
    transport = TSocket.TServerSocket(host=host, port=port)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
     
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    handler.server = server
     
    print "Starting server"
    server.serve()
    print "done!"


