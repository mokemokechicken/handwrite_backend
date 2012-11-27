# coding: utf8
'''
Created on 2012/11/26

@author: k_morishita
'''

import urllib2
import gzip
import logging
from nnservice import settings

class ExtAPIBase(object):
    def __init__(self, endpoint, timeout=7200):
        self.endpoint = endpoint
        self.timeout = timeout
    
    def _fetch_data(self):
        """
        
        @return 2-tuple.
            1: File-Like Object of HTTP Body.
            2: urllib2 Header Object.
        """
        request = urllib2.Request(self.endpoint, headers={"Accept-Encoding": "gzip"})
        res = urllib2.urlopen(request, timeout=self.timeout)
        headers = res.headers
        if headers.get('content-encoding') == "gzip":
            res = gzip.GzipFile(fileobj=res, mode="r")
        return res, headers

class HWDataAPI(ExtAPIBase):
    def __init__(self, **kw):
        super(HWDataAPI, self).__init__(settings.ENDPOINTS["hw_numbers"], **kw)
        
    def get_data(self):
        """
        
        @return 2-tuple.
            1: File-Like Object of HTTP Body.
            2: dict of metadata.
        """
        try:
            body_filelike, headers = self._fetch_data()
            return body_filelike, {
                          "numin":  int(headers['x-learndata-innodeqty']),
                          "numout": int(headers['x-learndata-outnodeqty']),
                          "numrow": int(headers['x-learndata-rowqty'])
                          }
        except IOError, e:
            logging.error(repr(e))
