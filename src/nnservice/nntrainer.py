# coding: utf8
'''NNMachineの学習を実際に行う

Created on 2012/11/28
@author: k_morishita
'''
from nnservice import settings
from nnservice.repositories import LearnDataRepository, NNMachineRepository
from nnservice.db import NNDatabase
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
from nnservice.nncommon import get_nnclass, deserialize_dataset

class NNTrainer(object):
    def __init__(self, typename, generation=None):
        self.typename = typename
        self.generation = generation
        self.db = NNDatabase()
        
    def run(self, callback=None):
        ld_model, dataset = self.load_learn_data()
        nnmachine_list = self.get_nnmachine_type_list()
        for config in nnmachine_list:
            nnmachine = self.build_machine(config, ld_model)
            self.learn(nnmachine, config, ld_model, dataset)
            valid_loss, test_loss = self.calc_score(nnmachine, dataset)
            nn_model = self.store_machine(nnmachine, config, ld_model, test_loss)
            if callback is not None:
                callback(nn_model)
            
    
    def load_learn_data(self):
        ld_model = LearnDataRepository(self.db).get(self.typename, self.generation)
        self.generation = ld_model.generation
        dataset = deserialize_dataset(ld_model)
        return ld_model, dataset
    
    def get_nnmachine_type_list(self):
        ret = []
        for c in settings.NNMACHINE_TYPES[self.typename]:
            config = copy.copy(settings.DEFAULT_LARNING_OPTION)
            config.update(c)
            ret.append(config)
        return ret
    

    def build_machine(self, config, ld_model):
        NNClass = get_nnclass(config["type"])
        nnmachine = NNClass(numpy_rng=numpy.random.RandomState(89677), 
                            n_ins=ld_model.num_in, n_outs=ld_model.num_out,
                            hidden_layers_sizes=config["hiddens"]
                            )
        return nnmachine

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
        return model

if __name__ == "__main__":
    import sys
    typename = len(sys.argv) > 1 and sys.argv[1] or "numbers"
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
    nnt = NNTrainer(typename)
    nnt.run()
