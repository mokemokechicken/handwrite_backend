# coding: utf8
'''
Created on 2012/11/26

@author: k_morishita
'''

from __future__ import with_statement
import csv
import gzip
from tempfile import NamedTemporaryFile

import extapi
from prjlib.dataset.class_sampling import ClassSampling
import numpy
from cPickle import load, dump, HIGHEST_PROTOCOL
from nnservice.models import LearnData
from nnservice.repositories import LearnDataRepository
from nnservice.db import NNDatabase

class ImportHWData(object):
    """Web IF からデータを受信して、Theano用にフォーマット変更して保存する

    YについてのClassSampling が必要かもなぁ。
    ( (TrainX,TrainY), (ValidateX, ValidateY), (TestX,TestY) ) に分割して,
    Pickle -> Gzip -> DB
    """
    multiply = None       # データの水増し廖
    noise_range = None    # わざとブレさせる倍率幅。 [0.5,2] などのように範囲で指定。
    
    def run(self):
        try:
            self.api = extapi.HWDataAPI()
            body, info = self.api.get_data(multiply=self.multiply, noise_range=self.noise_range)
            reader = csv.reader(body)
            range_x = (1, info["num_in"]+1)
            index_y = info["num_in"]+1
            with ClassSampling() as cs:
                trainset, validateset, testset = cs.sampling(reader, [8,1,1], (index_y, index_y+1))
                out_array = []
                self.serialize(out_array, trainset, range_x, index_y)
                self.serialize(out_array, validateset, range_x, index_y)
                self.serialize(out_array, testset, range_x, index_y)
                #
                tmpfile = NamedTemporaryFile()
                iostream = gzip.GzipFile(fileobj=tmpfile, mode="ab")
                dump(out_array, iostream, protocol=HIGHEST_PROTOCOL)
                iostream.close()
                #
                tmpfile.seek(0)
                self.store_dataset(tmpfile, info)
            return info
        
        except IOError, e:
            print repr(e)
    
    def serialize(self, out_array, dataset, range_x, index_y):
        """
        
        @param iostream: output stream object. 
        @param dataset: csv.reader object
        @param range_x: 2-tuple. range(range_x[0], range_x[1]) means indeies of X cols. 
        @param index-y: int. index of Y col.
        """
        xarray = []
        yarray = []
        for row in dataset:
            x = [float(v) for v in row[range_x[0]:range_x[1]]]
            xarray.append(x)
            yarray.append(row[index_y])
        #xs = theano.shared(numpy.asarray(xarray, dtype=T.dscalar), borrow=True)
        #ys = theano.shared(numpy.asarray(yarray, dtype=T.dscalar), borrow=True)
        out_array.append((xarray,yarray))

    def store_dataset(self, fileobj, info):
        """store into database"""
        repo = LearnDataRepository(NNDatabase())
        model = LearnData()
        model.name = self.api.typename
        model.generation = repo.count_number_of_name(model.name) + 1
        model.num_in = info["num_in"]
        model.num_out = info["num_out"]
        model.num_row = info["num_row"]
        model.data = fileobj.read()
        repo.add(model)

if __name__ == "__main__":
    ip = ImportHWData()
    ip.multiply = 30
    ip.noise_range = [0.5, 2]
    print "Imported %s" % ip.run()
