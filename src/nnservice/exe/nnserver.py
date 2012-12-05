# coding: utf8
'''
Created on 2012/11/29

@author: k_morishita
'''

import logging

from nnservice.interface import Infer
#from nnservice.interface.ttypes import *

from nnservice.nninfer import NNInfer
from nnservice.repositories import NNMachineRepository, NNEvaluateRepository
from nnservice.db import NNDatabase
import time

from nnservice import thrift_util
import json

class InferServiceHandler(object):
    def __init__(self, typename=None, nn_id=None, database=None):
        self.db = database or NNDatabase()
        if nn_id is None:
            self.service_obj = NNInfer.best_machine(typename=typename)
        else:
            self.build_machine(nn_id)

    def build_machine(self, nn_id):
        nn_model = NNMachineRepository(self.db).get(nn_id)
        self.service_obj = NNInfer(nn_model).setup_nnmachine()

    def infer(self, xs):
        if self.service_obj.model.num_in != len(xs):
            logging.error("error length %d != %d" % (self.service_obj.model.num_in, len(xs)))
            return []
        start_time = time.time()
        y, ys = self.service_obj.infer(xs)
        logging.info("infer %s (%f msec)" % (y, (time.time() - start_time)*1000)) 
        return ys
    
    def version(self):
        nn_model = self.service_obj.model
        nnconfig = json.loads(nn_model.nnconfig)
        e_repo = NNEvaluateRepository(self.db)
        er_model = e_repo.get_latest_eval_result(nn_model)
        ret = {
               "typename": nn_model.name,
               "in": nn_model.num_in,
               "out": nn_model.num_out,
               "score": er_model and er_model.score or -1,
               "hiddens": nnconfig.get("hiddens"),
               "nntype": nnconfig.get("type"),
               }
        logging.info("version: %s" % ret)
        return json.dumps(ret)
    
    def update_nnmachine(self, nn_id):
        cur_id = self.nn_id
        if nn_id == 0:
            self.service_obj = NNInfer.best_machine(typename=self.typename)
        else:
            self.build_machine(nn_id)
        logging.info("reload nn_id=%s" % self.nn_id)
        return cur_id != self.nn_id
    
    def halt(self):
        logging.info("halt")
        sys.exit(0)
    
    def ping(self):
        logging.info("ping received")
        return True
    
    def _typename(self):
        return self.service_obj.typename
    typename = property(_typename)
    
    def _nn_id(self):
        return self.service_obj.model.id
    nn_id = property(_nn_id)


def run_infer_server(typename=None, nn_id=None):
    handler = InferServiceHandler(typename=typename, nn_id=nn_id)
    _, port = thrift_util.get_infer_endpoint(handler.typename)
    thrift_util.run_server(Infer, handler, port=port)

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    typename = nn_id = None
    try:
        nn_id = len(sys.argv) > 1 and int(sys.argv[1]) or None
    except ValueError:
        typename = sys.argv[1]
    run_infer_server(typename, nn_id)
