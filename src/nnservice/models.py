# coding: utf8
'''
Created on 2012/11/26

@author: k_morishita
'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column, Sequence, ForeignKey
import sqlalchemy.types as t
from sqlalchemy.orm import relation, backref

Base = declarative_base()

class LearnData(Base):
    __tablename__ = "learn_data"
    
    id = Column(t.Integer, Sequence('learn_data_id_seq'), primary_key=True)
    name = Column(t.String(256))
    generation = Column(t.Integer)
    num_in = Column(t.Integer)
    num_out = Column(t.Integer)
    num_row = Column(t.Integer)
    data = Column(t.BLOB)
    create_datetime = Column(t.DateTime)

    def __repr__(self):
        return "<LearnData(%s,%s,%s,%s,%s,%s)>" % (self.id, self.name, self.generation, self.num_in,
                                                   self.num_out, self.num_row)

class NNMachine(Base):
    __tablename__ = "nnmachine"
    
    id = Column(t.Integer, Sequence('nnmachine_id_seq'), primary_key=True)
    name = Column(t.String(256))
    generation = Column(t.Integer)
    num_in = Column(t.Integer)
    num_out = Column(t.Integer)
    nnconfig = Column(t.String(4096))
    score = Column(t.Float)
    data = Column(t.BLOB)
    create_datetime = Column(t.DateTime)
    
    def __repr__(self):
        return "<NNMachine(%s,%s,%s,%s,%s,%s)>:%s" % (self.id, self.name, self.generation, self.num_in, 
                                                   self.num_out, self.score, self.nnconfig)

class NNEvaluate(Base):
    __tablename__ = "nneval"
    
    id = Column(t.Integer, Sequence('nneval_id_seq'), primary_key=True)
    name = Column(t.String(256))
    learn_data_id = Column(t.Integer, ForeignKey("learn_data.id"))
    create_datetime = Column(t.DateTime)
    
    def __repr__(self):
        return "<NNEvaluate(%s,%s)>" % (self.id, self.name)


class NNEvaluateResult(Base):
    __tablename__ = "nneval_result"
    
    id = Column(t.Integer, Sequence('nneval_result_id_seq'), primary_key=True)
    nneval_id = Column(t.Integer, ForeignKey("nneval.id"))
    nn_id = Column(t.Integer, ForeignKey("nnmachine.id"))
    score = Column(t.Float)
    create_datetime = Column(t.DateTime)
    # Relation
    nneval = relation(NNEvaluate, backref=backref("results"))
    nnmachine = relation(NNMachine)

    def __repr__(self):
        return "<NNEvaluateResult(%s,%s,%s,%s)>" % (self.id, self.nneval_id, self.nn_id, self.score)

