# coding: utf8
'''
Created on 2012/11/28

@author: k_morishita
'''

from __future__ import absolute_import

from . import models
from sqlalchemy.sql.expression import func
import datetime


class RepositoryBase(object):
    def __init__(self, database):
        """
        
        @param engine: NNDatabase object
        """
        self.db = database

    def add(self, model):
        session = self.db.Session()
        model.create_datetime = datetime.datetime.now()
        session.add(model)
        session.commit()
        model.id

class LearnDataRepository(RepositoryBase):
    modelClass= models.LearnData
    
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

    def get_updated_since(self, typename, before_sec):
        session = self.db.Session()
        q = session.query(self.modelClass).filter_by(name=typename).order_by(self.modelClass.generation.desc())
        q = q.filter(self.modelClass.create_datetime > datetime.datetime.now() - datetime.timedelta(0, before_sec))
        return q.first()
        
    
class NNMachineRepository(RepositoryBase):
    modelClass = models.NNMachine
    
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

class NNEvaluateRepository(RepositoryBase):
    modelClass = models.NNEvaluate

    def get_latest_evaluation(self, typename):
        session = self.db.Session()
        q = session.query(self.modelClass).filter_by(name=typename).order_by(self.modelClass.id.desc())
        return q.first()

