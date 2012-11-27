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
import theano
import theano.tensor as T
from cPickle import load, dump, HIGHEST_PROTOCOL

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
            #trainset, validateset, testset = cs.sampling(reader, [8,1,1], range_y)
            trainset, validateset, testset = cs.sampling(reader, [8,1,1], None)
            out_array = []
            self.serialize(out_array, trainset, range_x, range_y)
            self.serialize(out_array, validateset, range_x, range_y)
            self.serialize(out_array, testset, range_x, range_y)
            #
            tmpfile = NamedTemporaryFile()
            iostream = gzip.GzipFile(fileobj=tmpfile, mode="ab")
            dump(out_array, iostream, protocol=HIGHEST_PROTOCOL)
            iostream.close()
            #
            tmpfile.seek(0)
            self.store_dataset(tmpfile)
    
    def serialize(self, out_array, dataset, range_x, range_y):
        """
        
        @param iostream: output stream object. 
        @param dataset: csv.reader object
        @param range_x: 2-tuple. range(range_x[0], range_x[1]) means indeies of X cols. 
        @param range_y: 2-tuple. range(range_y[0], range_y[1]) means indeies of Y cols. 
        """
        xarray = []
        yarray = []
        for row in dataset:
            print row
            x = [float(v) for v in row[range_x[0]:range_x[1]]]
            y = [float(v) for v in row[range_y[0]:range_y[1]]]
            xarray.append(x)
            yarray.append(y)
        xs = theano.shared(numpy.asarray(xarray, dtype=T.dscalar), borrow=True)
        ys = theano.shared(numpy.asarray(yarray, dtype=T.dscalar), borrow=True)
        out_array.append((xs,ys))

    def store_dataset(self, fileobj):
        """store into database"""
        open("/tmp/a.gz", "wb").write(fileobj.read())

if __name__ == "__main__":
    ImportHWData().run()
