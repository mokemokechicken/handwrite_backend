# coding: utf8
'''
Created on 2012/11/27

@author: k_morishita
'''


class ClassSampling(object):
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        
    def close(self):
        pass
    
    def sampling(self, csv_reader, ratio_list, classify_fields):
        pass
