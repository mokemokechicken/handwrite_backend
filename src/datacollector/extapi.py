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

class ExtAPIBase(object):
    typename = None
    def __init__(self, endpoint = None, timeout=7200):
        self.endpoint = endpoint or settings.ENDPOINTS[self.typename]
        self.timeout = timeout
    
    def _fetch_data(self):
        """
        
        @return 2-tuple.
            1: File-Like Object of HTTP Body.
            2: urllib2 Header Object.
        """
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
