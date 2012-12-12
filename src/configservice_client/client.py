# coding: utf8
'''
Created on 2012/12/12

@author: k_morishita
'''
import urllib
import urllib2
import json

class ConfigClient(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.timeout = 60
    
    def _fetch_data(self, name, params=None):
        """
        
        @return 2-tuple.
            1: String of HTTP Body.
            2: urllib2 Header Object.
        """
        endpoint = "%s/%s" % (self.endpoint, name)
        if params is not None and len(params) > 0:
            endpoint += "?" + urllib.urlencode(params.items())
        request = urllib2.Request(endpoint)
        res = urllib2.urlopen(request, timeout=self.timeout)
        headers = res.headers
        return res.read(), headers
    
    def get_config(self, typename):
        body, _headers = self._fetch_data(typename)
        response = json.loads(body)
        return response["config"]

