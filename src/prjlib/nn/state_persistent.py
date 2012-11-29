# coding: utf8
'''
Created on 2012/11/16

@author: k_morishita
'''


from cPickle import load, dump, HIGHEST_PROTOCOL
import os
import gzip


def load_params(filename):
    data = None
    if os.path.exists(filename):
        fin = gzip.open(filename, "rb")
        data = load(fin)
        fin.close()
    return data

def save_params(filename, machine):
    if isinstance(filename, (str,)):
        basedir = os.path.abspath(os.path.dirname(filename))
        if not os.path.isdir(basedir):
            os.makedirs(basedir)
        fout = gzip.open(filename, "wb")
    else:
        fout = gzip.GzipFile(fileobj=filename, mode="wb")
    dump(machine.serialize(), fout, protocol=HIGHEST_PROTOCOL)
    fout.close()

class StatePersistent(object):
    def deserialize(self, params, num):
        return [params.pop(0) for _ in range(num)]
    
    def serialize(self):
        return self.params
