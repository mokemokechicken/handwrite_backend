# coding: utf8
'''
Created on 2012/11/28

@author: k_morishita
'''
from nnservice import settings
from nnservice.repositories import LearnDataRepository, NNMachineRepository
from nnservice.db import NNDatabase
from prjlib.nn.DBN import DBN
from prjlib.nn.SdA import SdA
from cStringIO import StringIO

from prjlib.nn.learning import load_data, pretraining_model, fine_tune_model,\
    evaluate_model
import numpy
import copy
from nnservice.models import NNMachine
import json
from prjlib.nn.state_persistent import save_params
import tempfile
import logging

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
            valid_loss, test_loss = self.calc_score(nnmachine, dataset)
            self.store_machine(nnmachine, config, ld_model, test_loss)
    
    def load_learn_data(self):
        ld_model = LearnDataRepository(self.db).get(self.typename, self.generation)
        self.generation = ld_model.generation
        ioobj = StringIO(ld_model.data)
        dataset = load_data(ioobj)
        ioobj.close()
        return ld_model, dataset
    
    def get_nnmachine_type_list(self):
        ret = []
        for c in settings.NNMACHINE_TYPES[self.typename]:
            config = copy.copy(settings.DEFAULT_LARNING_OPTION)
            config.update(c)
            ret.append(config)
        return ret
    

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
        pretraining_model(nnmachine, dataset[0][0], **config)
        fine_tune_model(nnmachine, dataset, **config)
    
    def calc_score(self, nnmachine, dataset):
        """
        
        @return 2-tuple: (validation_loss, test_loss)   (float)
        """
        return evaluate_model(nnmachine, dataset)

    def store_machine(self, nnmachine, config, ld_model, score):
        repo = NNMachineRepository(self.db)
        model = NNMachine(name=self.typename, generation=self.generation,
                          num_in=ld_model.num_in, num_out=ld_model.num_out,
                          nnconfig=json.dumps(config),
                          score=score)
        tmpf = tempfile.TemporaryFile()
        save_params(tmpf, nnmachine)
        tmpf.seek(0)
        model.data = tmpf.read()
        repo.add(model)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    nnt = NNTrainer("hw_numbers")
    nnt.run()
