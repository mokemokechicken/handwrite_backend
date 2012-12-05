# coding: utf8
'''
Created on 2012/11/28

@author: k_morishita
'''

from unittest.case import TestCase

from ..db import NNDatabase
from ..repositories import LearnDataRepository
from ..models import LearnData, NNMachine, NNEvaluate, NNEvaluateResult
from sqlalchemy.sql.expression import select
import datetime
from nnservice.repositories import NNMachineRepository, NNEvaluateRepository


class LearnDataRepositoryTest(TestCase):
    def setUp(self):
        self.db = NNDatabase(connection="sqlite://")
        self.db.create_table(LearnData)
        self.obj = LearnDataRepository(self.db)
    
    def tearDown(self):
        self.db.close()
    
    def test_add(self):
        dt = datetime.datetime.now()
        model = LearnData()
        model.name = "hoge"
        model.generation = 2
        model.num_in = 3
        model.num_out = 4
        model.num_row = 5
        model.data = "XXXX"
        model.create_datetime = dt
        self.obj.add(model)
        
        session = self.db.Session()
        q = session.query(LearnData).all()
        self.assertEquals(1, len(q))
        m = q[0]
        self.assertEquals("hoge", m.name)
        self.assertEquals(2, m.generation)
        self.assertEquals(3, m.num_in)
        self.assertEquals(4, m.num_out)
        self.assertEquals(5, m.num_row)
        self.assertEquals("XXXX", m.data)
        self.assertTrue(dt <= m.create_datetime <= datetime.datetime.now())
    
    def test_count(self):
        self.obj.add(LearnData(name="hoge"))
        self.obj.add(LearnData(name="hoge"))
        self.obj.add(LearnData(name="moke"))
        
        self.assertEquals(2, self.obj.count_number_of_name("hoge"))
        self.assertEquals(1, self.obj.count_number_of_name("moke"))
        self.assertEquals(0, self.obj.count_number_of_name("hogehoge"))

    def test_get(self):
        self.obj.add(LearnData(name="hoge", generation=1))
        self.obj.add(LearnData(name="hoge", generation=2))
        self.obj.add(LearnData(name="moke", generation=1))
        
        self.assertEquals(2, self.obj.get("hoge", 2).generation)
        self.assertEquals(1, self.obj.get("hoge", 1).generation)
        self.assertEquals(2, self.obj.get("hoge").generation)
        self.assertEquals(1, self.obj.get("moke").generation)
        
class NNMachineRepositoryTest(TestCase):
    def setUp(self):
        self.db = NNDatabase(connection="sqlite://")
        for m in [NNMachine, NNEvaluate, NNEvaluateResult]:
            self.db.create_table(m)

    def tearDown(self):
        self.db.close()
    
    def test_models_after(self):
        repo = NNMachineRepository(self.db)
        name = "hoge"
        for _ in range(5):
            repo.add(NNMachine(name=name))
        for _ in range(5):
            repo.add(NNMachine(name="MMMMMM"))
        ret = list(repo.get_models_after(name, "3"))
        self.assertEquals(2, len(ret))
        self.assertEquals(4, ret[0].id)
        self.assertEquals(5, ret[1].id)
    
class NNEvaluateRepositoryTest(TestCase):
    def setUp(self):
        self.db = NNDatabase(connection="sqlite://")
        for m in [LearnData, NNMachine, NNEvaluate, NNEvaluateResult]:
            self.db.create_table(m)

    def tearDown(self):
        self.db.close()
    
    def test_get_latest_evaluation(self):
        l_repo = LearnDataRepository(self.db)
        #m_repo = NNMachineRepository(self.db)
        e_repo = NNEvaluateRepository(self.db)
        name = "hoge"
        for _ in range(3):
            l_model = LearnData(name=name)
            l_repo.add(l_model)
            e_repo.add(NNEvaluate(name=name, learn_data_id=l_model.id))
        e_model = e_repo.get_latest_evaluation(name)
        self.assertIsNotNone(e_model)
        self.assertEquals(3, e_model.id)
        self.assertEquals(3, e_model.learn_data_id)
        
    def test_get_latest_evaluation_empty(self):
        e_repo = NNEvaluateRepository(self.db)
        e_model = e_repo.get_latest_evaluation("hoge")
        self.assertEquals(None, e_model)
    
    def test_check_related_results(self):
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
        for m in machines[1:]:
            er_model = NNEvaluateResult(nneval_id=e_model.id, nn_id=m.id, score=0.2)
            e_repo.add(er_model)
        
        e_model2 = e_repo.get_latest_evaluation(name)
        self.assertEquals(4, len(e_model2.results))
        
    def test_get_latest_eval_result(self):
        l_repo = LearnDataRepository(self.db)
        m_repo = NNMachineRepository(self.db)
        e_repo = NNEvaluateRepository(self.db)
        name = "hoge"
        machines = [NNMachine(name=name) for _ in range(5)]
        for m in machines:
            m_repo.add(m)

        l_model = LearnData(name=name)
        l_repo.add(l_model)
        e_model1 = NNEvaluate(name=name, learn_data_id=l_model.id)
        e_repo.add(e_model1)
        e_model2 = NNEvaluate(name=name, learn_data_id=l_model.id)
        e_repo.add(e_model2)
        
        for mi, m in enumerate(machines[1:]):
            for ei, e_model in enumerate([e_model1, e_model2]):
                er_model = NNEvaluateResult(nneval_id=e_model.id, nn_id=m.id, score=(2+ei+mi)/10.0)
                e_repo.add(er_model)
        
        er_model = e_repo.get_latest_eval_result(machines[0])
        self.assertIsNone(er_model)
        
        er_model = e_repo.get_latest_eval_result(machines[1])
        self.assertIsNotNone(er_model)
        self.assertEquals(0.3, er_model.score)
        
        er_model = e_repo.get_latest_eval_result(machines[3])
        self.assertIsNotNone(er_model)
        self.assertEquals(0.5, er_model.score)
        
        
        
