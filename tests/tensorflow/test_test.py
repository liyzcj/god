# -*- coding: utf-8 -*-
'''
@Description: Test Tensorflow test
@Author: Li Yanzhe
@Date: 2019-12-05 17:39:51
@LastEditors: Li Yanzhe
@LastEditTime: 2019-12-05 17:42:07
@Copyright (c) 2019 Senses Intelligence
'''
import unittest

from god.tensorflow import test


class TestTensorflowTest(unittest.TestCase):

    def test_gpu(self):
        test.gpu()
