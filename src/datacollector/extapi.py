# coding: utf8
'''
Created on 2012/11/26

@author: k_morishita
'''

import urllib2
import gzip
import logging
from nnservice import settings
import tempfile
import urllib

class ExtAPIBase(object):
    typename = None
    def __init__(self, endpoint = None, timeout=7200):
        self.endpoint = endpoint or settings.ENDPOINTS[self.typename]
        self.timeout = timeout
    
    def _fetch_data(self, params=None):
        """
        
        @return 2-tuple.
            1: File-Like Object of HTTP Body.
            2: urllib2 Header Object.
        """
        if params is not None and len(params) > 0:
            self.endpoint += "?" + urllib.urlencode(params.items())
        request = urllib2.Request(self.endpoint, headers={"Accept-Encoding": "gzip"})
        res = urllib2.urlopen(request, timeout=self.timeout)
        fileobj = tempfile.TemporaryFile()
        fileobj.write(res.read())
        fileobj.seek(0)
        headers = res.headers
        if headers.get('content-encoding') == "gzip":
            fileobj = gzip.GzipFile(fileobj=fileobj, mode="rb")
        return fileobj, headers

class HWDataAPI(ExtAPIBase):
    typename = "hw_numbers"

    def get_data(self, multiply=None, noise_range=None):
        """
        
        @return 2-tuple.
            1: File-Like Object of HTTP Body.
            2: dict of metadata.
        """
        params = {}
        if multiply:
            params["multiply"] = multiply
        if noise_range:
            params["noise_range"] = ",".join([str(x) for x in noise_range])
        body_filelike, headers = self._fetch_data(params=params)
        return body_filelike, {
                      "num_in":  int(headers['x-learndata-innodeqty']),
                      "num_out": int(headers['x-learndata-outnodeqty']),
                      "num_row": int(headers['x-learndata-rowqty'])
                      }
