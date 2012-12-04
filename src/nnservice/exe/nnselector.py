# coding: utf8
'''
Created on 2012/12/04

@author: k_morishita
'''

from __future__ import with_statement

import logging

from nnservice.repositories import NNMachineRepository, NNEvaluateRepository,\
    LearnDataRepository
from nnservice.db import NNDatabase
from nnservice.models import NNEvaluate, NNEvaluateResult
from nnservice.nncommon import build_nnmachine, deserialize_dataset
from prjlib.nn.learning import evaluate_model
from nnservice.exe.exe_common import restart_machine
from datacollector.import_hwdata import ImportHWData

class NNSelector(object):
    def __init__(self, db=None):
        self.db = db or NNDatabase()
        self.e_repo = NNEvaluateRepository(self.db)
        self.m_repo = NNMachineRepository(self.db)
        
    def select_and_launch_nnmachine(self, typename, candidate_num=3):
        machines = self.get_target_machines(typename, candidate_num)
        l_model = self.prepare_learn_model(typename)
        e_model = NNEvaluate(name=typename, learn_data_id=l_model.id)
        self.e_repo.add(e_model)
        best_score = 1
        best_model = None
        for m_model in machines:
            logging.info("Evaluating nn_id=%s" % m_model.id)
            r_model = self.evaluate_machine(m_model, l_model)
            r_model.nneval_id = e_model.id
            self.e_repo.add(r_model)
            if r_model.score < best_score:
                best_score = r_model.score
                best_model = m_model
                logging.info("update best score[nn_id=%s]: %.3f%%" % (m_model.id, best_score*100))
        if best_model:
            self.launch_nnmachine(best_model)
    
    def get_target_machines(self, typename, candidate_num):
        last_emodel = self.e_repo.get_latest_evaluation(typename)
        if last_emodel:
            machines = self.find_fine_machines_and_non_eval_machines(last_emodel, candidate_num)
        else:
            machines = self.m_repo.get_models_after(typename, 0)[-candidate_num:]
        return machines
    
    def prepare_learn_model(self, typename, before_sec=3600):
        late_model = LearnDataRepository(self.db).get_updated_since(typename, before_sec)
        if late_model:
            return late_model
        importer = ImportHWData(typename)
        importer.multiply = 3
        importer.run_import()
        return importer.ld_model
    
    def evaluate_machine(self, m_model, l_model):
        machine = build_nnmachine(m_model)
        dataset = deserialize_dataset(l_model)
        v_loss, t_loss = evaluate_model(machine, dataset)
        r_model = NNEvaluateResult(nn_id=m_model.id, score=t_loss)
        return r_model

    def find_fine_machines_and_non_eval_machines(self, e_model, candidate_num):
        past_best_n = sorted(e_model.results, lambda a,b: cmp(a.score, b.score))[:candidate_num]
        ret = [r.nnmachine for r in past_best_n]
        if e_model.results:
            max_id_results = max(e_model.results, key=lambda r: r.nn_id)
            mms = list(self.m_repo.get_models_after(e_model.name, max_id_results.nn_id))
        else:
            mms = list(self.m_repo.get_models_after(e_model.name, 0))[-candidate_num:]
        ret.extend(mms)
        return ret
    
    def launch_nnmachine(self, m_model):
        restart_machine(m_model.name, m_model.id)

if __name__ == "__main__":
    import os, sys
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    try:
        fd = os.open(__file__, os.O_RDONLY|os.O_EXLOCK|os.O_NONBLOCK)
        selector = NNSelector()
        selector.select_and_launch_nnmachine(sys.argv[1], 3)
    except OSError:
        logging.warn("nnselector already running, exit")
        sys.exit(1)

