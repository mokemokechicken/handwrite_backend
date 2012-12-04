# coding: utf8
'''
Created on 2012/11/29

@author: k_morishita
'''

from __future__ import absolute_import

from nnservice.interface import Infer
#from nnservice.interface.ttypes import *

from nnservice.nninfer import NNInfer
from nnservice.repositories import NNMachineRepository
from nnservice.db import NNDatabase
import time

from nnservice import thrift_util
from nnservice.thrift_util import get_infer_endpoint

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


def run_server(typename=None, nn_id=None):
    handler = InferServiceHandler(typename=typename, nn_id=nn_id)
    _, port = get_infer_endpoint(handler.typename)
    thrift_util.run_server(Infer, handler, port=port)

if __name__ == "__main__":
    import sys
    typename = nn_id = None
    try:
        nn_id = len(sys.argv) > 1 and int(sys.argv[1]) or None
    except ValueError:
        typename = sys.argv[1]
    run_server(typename, nn_id)
