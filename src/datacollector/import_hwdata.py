# coding: utf8
'''
Created on 2012/11/26

@author: k_morishita
'''


from datacollector import extapi
import csv
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
        classify_fields=range(info["numin"]+1, info["numin"]+info["numout"]+1)
        with ClassSampling() as cs:
            train, validate, test = cs.sampling(reader, [8,1,1], classify_fields)

