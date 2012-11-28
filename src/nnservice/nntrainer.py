# coding: utf8
'''
Created on 2012/11/28

@author: k_morishita
'''
from nnservice import settings
from nnservice.repositories import LearnDataRepository
from nnservice.db import NNDatabase
from prjlib.nn.DBN import DBN
from prjlib.nn.SdA import SdA
from cStringIO import StringIO

from prjlib.nn.learning import load_data
import numpy

class NNTrainer(object):
    def __init__(self, typename, generation=None):
        self.typename = typename
        self.generation = generation
        self.db = NNDatabase()
        
    def run(self):
        ld_model, dataset = self.load_learn_data()
        nnmachine_list = self.get_nnmachine_type_list()
        for config in nnmachine_list:
            nnmachine = self.build_machine(config, ld_model)
            self.learn(nnmachine, config, ld_model, dataset)
            score = self.calc_score(nnmachine, dataset)
            self.store_machine(nnmachine, config, ld_model, score)
    
    def load_learn_data(self):
        ld_model = LearnDataRepository(self.db).get(self.typename, self.generation)
        ioobj = StringIO(ld_model.data)
        dataset = load_data(ioobj)
        ioobj.close()
        return ld_model, dataset
    
    def get_nnmachine_type_list(self):
        return settings.NNMACHINE_TYPES[self.typename]

    def build_machine(self, config, ld_model):
        NNClass = self.get_nnclass(config["type"])
        nnmachine = NNClass(numpy_rng=numpy.random.RandomState(89677), 
                            n_ins=ld_model.num_in, n_outs=ld_model.num_out,
                            hidden_layers_sizes=config["hiddens"]
                            )
        return nnmachine

    def get_nnclass(self, nntype):
        if nntype == "dbn":
            return DBN
        elif nntype == "sda":
            return SdA
    
    def learn(self, nnmachine, config, ld_model, dataset):
        pass
    
    def calc_score(self, nnmachine, dataset):
        pass
    
    def store_machine(self, nnmachine, config, ld_model, dataset):
        pass

if __name__ == "__main__":
    nnt = NNTrainer("hw_numbsers")
    nnt.run()
