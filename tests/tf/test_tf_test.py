# -*- coding: utf-8 -*-
###
# Description: test tensorflow/test.py
# Author: Li Yanzhe
# Date: 2019-12-05 20:27:08
# LastEditors: Li Yanzhe
# LastEditTime: 2019-12-14 21:19:56
# Copyright (c) 2019
###

import unittest

from god.tensorflow import test


class TestTensorflowTest(unittest.TestCase):

    def test_gpu(self):
        test.gpu()
