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
        
    def get(self, typename, generation=None):
        session = self.db.Session()
        if generation is None:
            q = session.query(self.modelClass).filter_by(name=typename).order_by(self.modelClass.generation.desc()).first()
        else:
            q = session.query(self.modelClass).filter_by(name=typename, generation=generation).one()
        return q

    
class NNMachineRepository(object):
    modelClass = models.NNMachine
    
    def __init__(self, database):
        self.db = database
    
    def add(self, model):
        session = self.db.Session()
        model.create_datetime = datetime.datetime.now()
        session.add(model)
        session.commit()
    
    def get(self, nn_id):
        session = self.db.Session()
        return session.query(self.modelClass).filter_by(id=nn_id).one()
    
    def get_best_model(self, typename=None):
        session = self.db.Session()
        q = session.query(self.modelClass).order_by(self.modelClass.generation.desc(), self.modelClass.score)
        if typename is not None:
            q = q.filter_by(name=typename)
        return q.first()
    
    def get_models_after(self, typename, nn_id):
        session = self.db.Session()
        q = session.query(self.modelClass).filter(self.modelClass.id > nn_id).order_by(self.modelClass.id)
        q = q.filter_by(name=typename) 
        return q

class NNEvaluateRepository(object):
    modelClass = models.NNEvaluate

    def __init__(self, database):
        self.db = database
    
    def add(self, model):
        session = self.db.Session()
        model.create_datetime = datetime.datetime.now()
        session.add(model)
        session.commit()
    
    def get_latest_evaluation(self, typename):
        session = self.db.Session()
        q = session.query(self.modelClass).filter_by(name=typename).order_by(self.modelClass.id.desc())
        return q.first()

