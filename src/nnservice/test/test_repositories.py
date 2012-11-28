# coding: utf8
'''
Created on 2012/11/28

@author: k_morishita
'''

from unittest.case import TestCase

from ..db import NNDatabase
from ..repositories import LearnDataRepository
from ..models import LearnData
from sqlalchemy.sql.expression import select
import datetime

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
        self.assertEquals(dt, m.create_datetime)
    
    def test_count(self):
        self.obj.add(LearnData(name="hoge"))
        self.obj.add(LearnData(name="hoge"))
        self.obj.add(LearnData(name="moke"))
        
        self.assertEquals(2, self.obj.count_number_of_name("hoge"))
        self.assertEquals(1, self.obj.count_number_of_name("moke"))
        self.assertEquals(0, self.obj.count_number_of_name("hogehoge"))


    
