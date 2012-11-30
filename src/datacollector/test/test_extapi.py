# coding: utf8
'''
Created on 2012/11/29

@author: k_morishita
'''

from unittest.case import TestCase
from mock import patch


from ..extapi import HWDataAPI
from _pyio import StringIO
import json

class HWDataAPITest(TestCase):
    def setUp(self):
        self.api = HWDataAPI("numbers")
    
    def test_get_data_with_params(self):
        r = {
             'x-learndata-innodeqty': 2,
             'x-learndata-outnodeqty': 3,
             'x-learndata-rowqty': 4,
             }

        with patch.object(self.api, "_fetch_data", return_value=[None, r]) as api:
            f,d = self.api.get_data()
            api.assert_called_with("dataset", params={})
        
        with patch.object(self.api, "_fetch_data", return_value=[None, r]) as api:
            f,d = self.api.get_data(multiply=3)
            api.assert_called_with("dataset", params={"multiply": 3})
        
        with patch.object(self.api, "_fetch_data", return_value=[None, r]) as api:
            f,d = self.api.get_data(noise_range=[0.5, 2])
            api.assert_called_with("dataset", params={"noise_range": "0.5,2"})

        with patch.object(self.api, "_fetch_data", return_value=[None, r]) as api:
            f,d = self.api.get_data(noise_range=[0.5, 2], multiply=3)
            api.assert_called_with("dataset", params={"multiply":3, "noise_range":"0.5,2"})

    def test_get_info_with_params(self):
        filelike = StringIO(json.dumps({"hoge": 1}))
        with patch.object(self.api, "_fetch_data", return_value=[filelike, None]) as api:
            f = self.api.get_info()
            api.assert_called_with("datainfo", params={})
            self.assertEquals({"hoge":1}, f)
        
        filelike.seek(0)
        with patch.object(self.api, "_fetch_data", return_value=[filelike, None]) as api:
            f = self.api.get_info(multiply=3)
            api.assert_called_with("datainfo", params={"multiply": 3})
            self.assertEquals({"hoge":1}, f)
        
        