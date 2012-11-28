# coding: utf8
'''
Created on 2012/11/26

@author: k_morishita
'''

from sqlalchemy import create_engine
from nnservice import settings
from sqlalchemy.schema import MetaData, Table
from sqlalchemy.orm.session import sessionmaker

def create_nnservice_engine(connection=None, **kw):
    conf = settings.DATABASE
    
    if connection is None:
        schema = conf["schema"]
        user_pass_host = conf["host"]
        name = conf["name"]
        if conf["user"] and len(conf["user"]) > 0:
            user_pass = conf["user"]
            if conf["pass"] and len(conf["pass"]) > 0:
                user_pass +=  ":" + conf["pass"]
            user_pass_host = "%s@%s" % (user_pass, user_pass_host)
        if schema == "sqlite":
            basedir = settings.DATABASE_FILE_DIR
            name = "%s/%s" % (basedir, name) 
        connection = "%s://%s/%s" % (schema, user_pass_host, name)
    return create_engine(connection, **kw)

class NNDatabase(object):
    engine = None
    metadata = None
    _conn = None
    _Session = None
    
    def __init__(self, **kw):
        self.engine = create_nnservice_engine(**kw)
        self.metadata = MetaData(bind=self.engine)
    
    def table(self, modelClass):
        if isinstance(modelClass, (str,)):
            return Table(modelClass, self.metadata)
        else:
            return modelClass.__table__
    
    def create_table(self, modelClass):
        self.table(modelClass).create(self.engine)
    
    def _get_connect(self):
        if self._conn is None:
            self._conn = self.engine.connect()
        return self._conn
    conn = property(_get_connect)
    
    def _get_Session(self):
        if self._Session is None:
            self._Session = sessionmaker(bind=self.engine)
        return self._Session
    Session = property(_get_Session)
    
    def close(self):
        pass
        
    

if __name__ == '__main__':
    def is_subclass(x, cls):
        return isinstance(x, (object.__class__,)) and issubclass(x, cls) and x != cls
    
    import sys
    from nnservice import models
    
    if len(sys.argv) > 1 and sys.argv[1] == "syncdb":
        print sys.argv[1]
        engine = create_nnservice_engine(echo=True)
        for model in models.__dict__.values():
            if is_subclass(model, models.Base):
                table = model.__table__
                table.create(engine, checkfirst=True)

