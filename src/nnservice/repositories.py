# coding: utf8
'''
Created on 2012/11/28

@author: k_morishita
'''

from __future__ import absolute_import

from . import models
from sqlalchemy.sql.expression import func
import datetime


class LearnDataRepository(object):
    modelClass= models.LearnData
    
    def __init__(self, database):
        """
        
        @param engine: NNDatabase object
        """
        self.db = database
    
    def add(self, model, session=None, autocommit=True):
        session = session or self.db.Session()
        model.create_datetime = datetime.datetime.now()
        session.add(model)
        if autocommit:
            session.commit()
    
    def count_number_of_name(self, typename):
        session = self.db.Session()
        result = session.query(func.count(self.modelClass.id)).filter_by(name=typename)
        return int(result[0][0])
        
    
    
