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

class LearnDataRepositoryTest(TestCase):
    def setUp(self):
        self.db = NNDatabase(connection="sqlite://")
        self.db.create_table(LearnData)
        self.obj = LearnDataRepository(self.db)
    
    def test_add(self):
        model = LearnData()
        model.name = "hoge"
        model.generation = 2
        model.num_in = 3
        model.num_out = 4
        model.num_row = 5
        model.data = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        self.obj.add(model)
        
        session = self.db.Session()
        q = session.query(LearnData).all()
        self.assertEquals(1, len(q))
    
    def test_count(self):
        self.obj.add(LearnData(name="hoge"))
        self.obj.add(LearnData(name="hoge"))
        self.obj.add(LearnData(name="moke"))
        
        self.assertEquals(2, self.obj.count_number_of_name("hoge"))
        self.assertEquals(1, self.obj.count_number_of_name("moke"))
        self.assertEquals(0, self.obj.count_number_of_name("hogehoge"))


    
