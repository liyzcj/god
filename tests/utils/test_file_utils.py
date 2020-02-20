# -*- coding: utf-8 -*-
"""Test of filt_utils.py"""

import unittest
from pathlib import Path

from god.utils import file_utils


class TestFileUtils(unittest.TestCase):

    def testTempDirCleanup(self):
        tmp = file_utils.TempDir()
        p = tmp.name
        self.assertTrue(p.exists())
        tmp.cleanup()
        self.assertFalse(p.exists())

    def testTempDirChangeDir(self):
        current = Path.cwd()
        with file_utils.TempDir(cd=True) as tmp:
            intmp = Path.cwd()
            self.assertEqual(intmp, tmp)
        self.assertEqual(current, Path.cwd())
