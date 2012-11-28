# coding: utf8
'''
Created on 2012/11/26

@author: k_morishita
'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column, Sequence
import sqlalchemy.types as t

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


