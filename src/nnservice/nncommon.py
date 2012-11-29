# coding: utf8
'''
Created on 2012/11/29

@author: k_morishita
'''

from __future__ import absolute_import

from prjlib.nn.DBN import DBN
from prjlib.nn.SdA import SdA
import json
from prjlib.nn.state_persistent import load_params
from cStringIO import StringIO
import numpy

def get_nnclass(nntype):
    if nntype == "dbn":
        return DBN
    elif nntype == "sda":
        return SdA

def build_nnmachine(nnmachine_model):
    config = json.loads(nnmachine_model.nnconfig)
    sio = StringIO(nnmachine_model.data)
    params = load_params(sio)
    sio.close()
    NNClass = get_nnclass(config["type"])
    nnmachine_model = NNClass(numpy_rng=numpy.random.RandomState(89677), 
                        n_ins=nnmachine_model.num_in, n_outs=nnmachine_model.num_out,
                        hidden_layers_sizes=config["hiddens"],
                        params=params
                        )
    return nnmachine_model
    
