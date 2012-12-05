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
    _session = None
    def __init__(self, database):
        """
        
        @param engine: NNDatabase object
        """
        self.db = database

    def add(self, model):
        model.create_datetime = datetime.datetime.now()
        self.session.add(model)
        self.session.commit()
        model.id
    
    def _get_session(self):
        if self._session is None:
            self._session = self.db.session
        return self._session
    def _set_session(self, session):
        self._session = session
    session = property(_get_session, _set_session)

class LearnDataRepository(RepositoryBase):
    modelClass= models.LearnData
    
    def count_number_of_name(self, typename):
        result = self.session.query(func.count(self.modelClass.id)).filter_by(name=typename)
        return int(result[0][0])
        
    def get(self, typename, generation=None):
        if generation is None:
            q = self.session.query(self.modelClass).filter_by(name=typename).order_by(self.modelClass.generation.desc()).first()
        else:
            q = self.session.query(self.modelClass).filter_by(name=typename, generation=generation).one()
        return q

    def get_updated_since(self, typename, before_sec):
        q = self.session.query(self.modelClass).filter_by(name=typename).order_by(self.modelClass.generation.desc())
        q = q.filter(self.modelClass.create_datetime > datetime.datetime.now() - datetime.timedelta(0, before_sec))
        return q.first()
        
    
class NNMachineRepository(RepositoryBase):
    modelClass = models.NNMachine
    
    def get(self, nn_id):
        return self.session.query(self.modelClass).filter_by(id=nn_id).one()
    
    def get_best_model(self, typename=None):
        q = self.session.query(self.modelClass).order_by(self.modelClass.generation.desc(), self.modelClass.score)
        if typename is not None:
            q = q.filter_by(name=typename)
        return q.first()
    
    def get_models_after(self, typename, nn_id):
        q = self.session.query(self.modelClass).filter(self.modelClass.id > nn_id).order_by(self.modelClass.id)
        q = q.filter_by(name=typename) 
        return q

class NNEvaluateRepository(RepositoryBase):
    modelClass = models.NNEvaluate
    detailClass = models.NNEvaluateResult

    def get_latest_evaluation(self, typename):
        q = self.session.query(self.modelClass).filter_by(name=typename).order_by(self.modelClass.id.desc())
        return q.first()

    def get_latest_eval_result(self, m_model):
        """NNMachineに関する最新の評価結果を返す。まだ評価がなければNoneを返す。
        
        @param NNMachine m_model
        @return NNEvaluateResult
        """
        q = self.session.query(self.detailClass).filter_by(nn_id=m_model.id).order_by(self.detailClass.id.desc())
        return q.first()
