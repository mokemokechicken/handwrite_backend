# coding: utf8
'''
Created on 2012/11/29

@author: k_morishita
'''

import json
import theano
import numpy

from nnservice.db import NNDatabase
from nnservice.nncommon import build_nnmachine
from nnservice.repositories import NNMachineRepository


class NNInfer(object):
    
    @classmethod
    def best_machine(cls, typename=None):
        nn_model = NNMachineRepository(NNDatabase()).get_best_model(typename)
        infer = NNInfer(nn_model)
        infer.setup_nnmachine()
        return infer
    
    def __init__(self, nn_model):
        """
        
        @param NNMachine nn_model
        """
        self.model = nn_model
        self.config = json.loads(self.model.nnconfig)
    
    def setup_nnmachine(self):
        self.nnmachine = build_nnmachine(self.model)
        self.p_y_given_x = theano.function([self.nnmachine.x], self.nnmachine.p_y_given_x)
        self.y_pred = theano.function([self.nnmachine.x], self.nnmachine.y_pred)
        return self
    
    def _typename(self):
        return self.model.name
    typename = property(_typename)
    
    def infer(self, xs):
        """
        
        @param list xs: input values for inference.
        @return 2-tuple. (argmaxY, [<list of probabilities>])
        """
        x = numpy.asarray([xs])
        return self.y_pred(x)[0], self.p_y_given_x(x)[0]
