# -*- coding: utf-8 -*-
###
# Description: Test import_utils.py
# Author: Li Yanzhe
# Date: 2019-12-05 20:27:08
# LastEditors: Li Yanzhe
# LastEditTime: 2019-12-14 21:19:36
# Copyright (c) 2019
###
import os
import unittest

from god.utils import import_utils


class TestImportUtils(unittest.TestCase):

    def testImportFuncFromFile(self):
        folder = os.path.join(os.path.dirname(__file__), 'testdata')
        testfile = os.path.join(folder, 'import_file.py')
        fn = import_utils.import_func_from_file(testfile, 'import_fn')
        self.assertEqual(10, fn([1, 2, 3, 4]))

    def testImportFuncFromFileMissingFile(self):
        folder = os.path.join(os.path.dirname(__file__), 'testdata')
        testfile = os.path.join(folder, 'not_exist_file.py')
        with self.assertRaises(ImportError):
            import_utils.import_func_from_file(testfile, 'import_fn')

    def testImportFuncFromFileMissingFunction(self):
        folder = os.path.join(os.path.dirname(__file__), 'testdata')
        testfile = os.path.join(folder, 'import_file.py')
        with self.assertRaises(AttributeError):
            import_utils.import_func_from_file(testfile, 'not_exist_fn')
