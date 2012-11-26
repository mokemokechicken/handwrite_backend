# coding: utf8
'''
Created on 2012/11/26

@author: k_morishita
'''

class ExtAPIBase(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint
    

class HWDataAPI(ExtAPIBase):
    def get_data(self):
        data, info = self.fetch_data()
        