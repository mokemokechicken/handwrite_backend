# coding: utf8
'''
Created on 2012/11/26

@author: k_morishita
'''

from sqlalchemy import create_engine
from nnservice import settings

def create_nnservice_engine(**kw):
    conf = settings.DATABASE
    
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
    constr = "%s://%s/%s" % (schema, user_pass_host, name)
    print constr
    return create_engine(constr, **kw)



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

