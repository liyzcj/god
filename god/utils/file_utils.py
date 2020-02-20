"""A Module about file utilities."""

import os
from pathlib import Path
from tempfile import TemporaryDirectory


class TempDir(object):
    """
    Similar with TemporaryDirectory, except:

    * May chdir when use `with` statement
    * yield variable is a Path object when use `with` statement
    * `name` attribute return a Path object

    """

    def __init__(self, cd=False):
        """
        Create an temporary directory.

        :param cd: change to temporay dir or not, defaults to False
        :type cd: bool, optional
        """
        self._dir = None  # keep current dir if chdr
        self._tmp_obj = TemporaryDirectory()
        self._cd = cd
        self.name = Path(self._tmp_obj.name).absolute()

    def __enter__(self):
        if self._cd:
            self._dir = Path.cwd().absolute()
            os.chdir(self.name)
            return Path('./').absolute()
        return self.name

    def __exit__(self, tp, val, traceback):
        if self._cd:
            os.chdir(self._dir)

    def cleanup(self):
        """
        Remove the temporary director.
        """
        self._tmp_obj.cleanup()
