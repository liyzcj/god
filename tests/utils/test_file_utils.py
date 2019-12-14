# -*- coding: utf-8 -*-
###
# Description: Test file_utils.py
# Author: Li Yanzhe
# Date: 2019-12-14 01:07:03
# LastEditors: Li Yanzhe
# LastEditTime: 2019-12-14 21:18:39
# Copyright (c) 2019
###

import os
import unittest

from god.utils import file_utils


class TestFileUtils(unittest.TestCase):

    def testTempDirNotClean(self):
        with file_utils.TempDir(remove_on_exit=False) as tmp:
            self.assertTrue(os.path.exists(tmp.path()))
        self.assertTrue(os.path.exists(tmp.path()))

    def testTempDirClean(self):
        with file_utils.TempDir() as tmp:
            self.assertTrue(os.path.exists(tmp.path()))
        self.assertFalse(os.path.exists(tmp.path()))

    def testTempDirChdr(self):
        current = os.path.abspath(os.getcwd())
        with file_utils.TempDir(chdr=True) as tmp:
            intmp = os.path.abspath(os.getcwd())
            self.assertEqual(intmp, os.path.abspath(tmp.path()))
        self.assertEqual(current, os.getcwd())

    def testTempDirPath(self):
        with file_utils.TempDir(chdr=True) as tmp:
            self.assertEqual(os.path.abspath(tmp.path()),
                             os.path.abspath(os.getcwd()))

    def testTempDirPathFile(self):
        with file_utils.TempDir() as tmp:
            self.assertEqual(tmp.path('hello.txt'),
                             os.path.join(tmp.path(), 'hello.txt'))
