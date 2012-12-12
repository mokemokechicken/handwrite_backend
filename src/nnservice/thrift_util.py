# coding: utf8
'''
Created on 2012/12/03

@author: k_morishita
'''

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from nnservice import settings
from nnservice.interface import NNBackend, Infer
from configservice_client.config import load_config

def make_thrift_client(klass, host,  port):
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
     
    print "Starting server: %s" % (repr(handler))
    server.serve()

def get_infer_endpoint(typename):
    config = load_config(typename)
    return (config["infer_server_host"], config["infer_server_port"])
    # return settings.SERVICE_ENDPOINTS.get(typename, ("127.0.0.1", 10000))

def make_thrift_infer_client(typename):
    host, port = get_infer_endpoint(typename)
    return make_thrift_client(Infer, host, port)

def make_thrift_backend_client():
    host, port = settings.BACKEND_HOST, settings.BACKEND_PORT
    return make_thrift_client(NNBackend, host, port)
