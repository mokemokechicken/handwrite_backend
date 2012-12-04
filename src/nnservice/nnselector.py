# coding: utf8
'''
Created on 2012/12/04

@author: k_morishita
'''
from nnservice.repositories import NNMachineRepository
from nnservice.db import NNDatabase

class NNSelector(object):
    def __init__(self):
        self.db = NNDatabase()
        
    def select_and_launch_nnmachine(self, typename, candidate_num=5):
        repo = NNMachineRepository(self.db)
        
        


if __name__ == "__main__":
    pass

