# coding: utf8
'''
Created on 2012/12/05

@author: k_morishita
'''

from __future__ import absolute_import

import json

from unittest.case import TestCase

from ...db import NNDatabase
from ...models import LearnData, NNEvaluate, NNMachine, NNEvaluateResult
from ...repositories import NNMachineRepository
from ..nnserver import InferServiceHandler

from ymlib.unittest.misc import relative_package

from mock import patch

import sys

class InferServiceHandlerTest(TestCase):
    def setUp(self):
        self.db = NNDatabase(connection="sqlite://")
        for m in [LearnData, NNMachine, NNEvaluate, NNEvaluateResult]:
            self.db.create_table(m)
        self.m_repo = NNMachineRepository(self.db)
    
    def tearDown(self):
        self.db.close()

    @patch(relative_package("..nnserver.NNInfer", __package__))
    def create_handler(self, m_class):
        self.nnconfig = {"hiddens": [30,30], "type": "rbm"}
        model = NNMachine(name="hoge", num_in=20, num_out=100, nnconfig=json.dumps(self.nnconfig), score=0.002)
        self.m_repo.add(model)
        # Patching NNInfer Instance
        instance = m_class.return_value
        instance.setup_nnmachine.return_value = instance
        instance.model = model
        #
        handler = InferServiceHandler(nn_id=model.id, database=self.db)
        return handler
    
    def test_version(self):
        obj = self.create_handler()
        r = json.loads(obj.version())
        self.assertEquals("hoge", r["typename"])
        self.assertEquals(20, r["in"])
        self.assertEquals(100, r["out"])
        self.assertEquals([30,30], r["hiddens"])
        self.assertEquals("rbm", r["nntype"])
    
    @patch("sys.exit", return_value=True)
    def test_halt(self, mock_exit):
        obj = self.create_handler()
        obj.halt()
        mock_exit.assert_called_with(0)
        
    
    def test_infer(self):
        obj = self.create_handler()
        obj.service_obj.infer.return_value = ([0.1], [0.2])
        xs = [0] * obj.service_obj.model.num_in
        ys = obj.infer(xs)
        self.assertEquals([0.2], ys)
        obj.service_obj.infer.assert_called_with(xs)
    
    @patch("logging.warn", return_value="called")
    def test_infer_checkerror(self, warn_mock):
        obj = self.create_handler()
        self.assertEquals([], obj.infer([1]))
        self.assertEquals(True, warn_mock.called)

    def test_ping(self):
        obj = self.create_handler()
        self.assertEquals(True, obj.ping())