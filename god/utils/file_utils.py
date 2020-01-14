# -*- coding: utf-8 -*-
###
# Description: file utils
# Author: Li Yanzhe
# Date: 2019-12-14 00:31:13
# LastEditors: Li Yanzhe
# LastEditTime: 2019-12-14 21:16:38
# Copyright (c) 2019
###

import os
import tempfile
import shutil


class TempDir(object):
    """ Temporary directory """

    def __init__(self, chdr=False, remove_on_exit=True):
        """
        Construct TempDir as a context.

        Parameters
        ----------
        chdr : bool, optional
            change dir to temporary path, by default False
        remove_on_exit : bool, optional
            remove the tempdir when exiting, by default True
        """
        self._dir = None  # keep current dir if chdr
        self._path = None  # tempdir path
        self._chdr = chdr
        self._remove = remove_on_exit

    def __enter__(self):
        self._path = os.path.abspath(tempfile.mkdtemp())
        assert os.path.exists(self._path)
        if self._chdr:
            self._dir = os.path.abspath(os.getcwd())
            os.chdir(self._path)
        return self

    def __exit__(self, tp, val, traceback):
        if self._chdr and self._dir:
            os.chdir(self._dir)
            self._dir = None
        if self._remove and os.path.exists(self._path):
            shutil.rmtree(self._path)

        assert not self._remove or not os.path.exists(self._path)
        assert os.path.exists(os.getcwd())

    def path(self, *path):
        return os.path.join("./", *path) \
            if self._chdr else os.path.join(self._path, *path)
