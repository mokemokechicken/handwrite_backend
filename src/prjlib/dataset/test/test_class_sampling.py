# coding: utf8
'''
Created on 2012/11/27

@author: k_morishita
'''

from __future__ import absolute_import

from unittest.case import TestCase

from ..class_sampling import ClassSampling
from cStringIO import StringIO
import csv

class ClassSamplingTest(TestCase):
    def setUp(self):
        self.N = 120
        self.reader = self.create_reader()
    
    def create_reader(self):
        b = StringIO()
        for row in self.gen_data(self.N):
            b.write(",".join([str(x) for x in row]) + "\r\n")
        self.data = StringIO(b.getvalue())
        b.close()
        return csv.reader(self.data)
    
    def tearDown(self):
        self.data.close()

    def gen_data(self, N):
        y1 = ["a","b","c"] 
        y2 = ["1","2"]
        x1 = range(500, 500+N)
        x2 = range(100, 100+N)
        data = zip(range(N), x1, x2, y1*(N/len(y1)), y2*(N/len(y2)))
        return data
    
    def test_sampling(self):
        N = self.N
        with ClassSampling() as cs:
            trainset, validateset, testset = cs.sampling(self.reader, [8,1,1], (3,5))
            d1 = list(trainset)
            d2 = list(validateset)
            d3 = list(testset)
            self.assertEquals(int(N*0.8), len(d1))
            self.assertEquals(int(N*0.1), len(d2))
            self.assertEquals(int(N*0.1), len(d3))
            self.assertEquals(5, len(d1[0]))
            self.assertEquals(5, len(d2[0]))
            self.assertEquals(5, len(d3[0]))
            self.check_classnums(d1, N*0.8)
            self.check_classnums(d2, N*0.1)
            self.check_classnums(d2, N*0.1)
        if True:
            print "\n".join([str(x) for x in d1])
            print "-" * 50
            print "\n".join([str(x) for x in d2])
            print "-" * 50
            print "\n".join([str(x) for x in d3])
   
    def check_classnums(self, d, n):
        self.assertEquals(int(n/6), len(filter(lambda x: x[3]+x[4]=="a1", d)))
        self.assertEquals(int(n/6), len(filter(lambda x: x[3]+x[4]=="b1", d)))
        self.assertEquals(int(n/6), len(filter(lambda x: x[3]+x[4]=="c1", d)))
        self.assertEquals(int(n/6), len(filter(lambda x: x[3]+x[4]=="a2", d)))
        self.assertEquals(int(n/6), len(filter(lambda x: x[3]+x[4]=="b2", d)))
        self.assertEquals(int(n/6), len(filter(lambda x: x[3]+x[4]=="c2", d)))
