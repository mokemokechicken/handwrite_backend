# coding: utf8
'''
Created on 2012/11/26

@author: k_morishita
'''

from __future__ import with_statement
import csv
import gzip
from tempfile import NamedTemporaryFile

from . import extapi
from prjlib.dataset.class_sampling import ClassSampling

class ImportHWData(object):
    """Web IF からデータを受信して、Theano用にフォーマット変更して保存する

    YについてのClassSampling が必要かもなぁ。
    ( (TrainX,TrainY), (ValidateX, ValidateY), (TestX,TestY) ) に分割して,
    Pickle -> Gzip -> DB
    """
    def run(self):
        self.api = extapi.HWDataAPI()
        body, info = self.api.get_data()
        reader = csv.reader(body)
        range_x = (1, info["numin"]+1)
        range_y = (info["numin"]+1, info["numin"]+info["numout"]+1)
        with ClassSampling() as cs:
            trainset, validateset, testset = cs.sampling(reader, [8,1,1], range_y)
            tmpfile = NamedTemporaryFile()
            iostream = gzip.GzipFile(fileobj=tmpfile, mode="wb")
            self.serialize(iostream, trainset, range_x, range_y)
            self.serialize(iostream, validateset, range_x, range_y)
            self.serialize(iostream, testset, range_x, range_y)
            iostream.close()
            #
            tmpfile.seek(0)
            self.store_dataset(tmpfile)
    
    def serialize(self, iostream, dataset, range_x, range_y):
        pass


