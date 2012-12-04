# coding: utf8
'''
Created on 2012/12/04

@author: k_morishita
'''

from __future__ import absolute_import

from unittest.case import TestCase

from ..db import NNDatabase
from ..models import LearnData, NNMachine, NNEvaluate, NNEvaluateResult
from ..repositories import LearnDataRepository, NNMachineRepository, NNEvaluateRepository
from nnservice.exe.nnselector import NNSelector


class NNSelectorTest(TestCase):
    def setUp(self):
        self.db = NNDatabase(connection="sqlite://")
        for m in [LearnData, NNMachine, NNEvaluate, NNEvaluateResult]:
            self.db.create_table(m)
    
    def tearDown(self):
        self.db.close()
    
    def test_find_fine_machines_and_non_eval_machines(self):
        l_repo = LearnDataRepository(self.db)
        m_repo = NNMachineRepository(self.db)
        e_repo = NNEvaluateRepository(self.db)
        name = "hoge"
        machines = [NNMachine(name=name) for _ in range(5)]
        for m in machines:
            m_repo.add(m)

        l_model = LearnData(name=name)
        l_repo.add(l_model)
        e_model = NNEvaluate(name=name, learn_data_id=l_model.id)
        e_repo.add(e_model)
        for i, m in enumerate(machines[:3]):
            er_model = NNEvaluateResult(nneval_id=e_model.id, nn_id=m.id, score=i/10.0)
            e_repo.add(er_model)
        ###
        selector = NNSelector(self.db)
        machines = selector.find_fine_machines_and_non_eval_machines(e_model, 2) # shold be 1,2,4,5
        self.assertEquals(4, len(machines))
        self.assertEquals(1, machines[0].id)
        self.assertEquals(2, machines[1].id)
        self.assertEquals(4, machines[2].id)
        self.assertEquals(5, machines[3].id)
        
    def test_find_fine_machines_and_non_eval_machines_empty(self):
        l_repo = LearnDataRepository(self.db)
        m_repo = NNMachineRepository(self.db)
        e_repo = NNEvaluateRepository(self.db)
        name = "hoge"

        l_model = LearnData(name=name)
        l_repo.add(l_model)
        e_model = NNEvaluate(name=name, learn_data_id=l_model.id)
        e_repo.add(e_model)
        ###
        selector = NNSelector(self.db)
        machines = selector.find_fine_machines_and_non_eval_machines(e_model, 2) # shold be 1,2,4,5
        self.assertEquals([], machines)
