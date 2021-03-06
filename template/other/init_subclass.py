"""
通过 ``__new__`` 方法判断输入并实例化不同的子类。
"""

import os
import re


class FileSystem(object):

    class NoAccess(Exception):
        pass

    class Unknown(Exception):
        pass

    # Regex for matching "xxx://" where x is any character except for ":".
    _PATH_PREFIX_PATTERN = re.compile(r'\s*([^:]+)://')

    @classmethod
    def _get_all_subclasses(cls):
        """ Recursive generator of all class' subclasses. """
        for subclass in cls.__subclasses__():
            yield subclass
            for subclass in subclass._get_all_subclasses():
                yield subclass

    @classmethod
    def _get_prefix(cls, s):
        """ Extract any file system prefix at beginning of string s and
            return a lowercase version of it or None when there isn't one.
        """
        match = cls._PATH_PREFIX_PATTERN.match(s)
        return match.group(1).lower() if match else None

    def __new__(cls, path):
        """ Create instance of appropriate subclass using path prefix. """
        path_prefix = cls._get_prefix(path)

        for subclass in cls._get_all_subclasses():
            if subclass.prefix == path_prefix:
                # Using "object" base class method avoids recursion here.
                return object.__new__(subclass)
        else:  # No subclass with matching prefix found (& no default defined)
            raise FileSystem.Unknown(
                'path "{}" has no known file system prefix'.format(path))

    def count_files(self):
        raise NotImplementedError


class Nfs(FileSystem):
    prefix = 'nfs'

    def __init__(self, path):
        pass

    def count_files(self):
        pass


class LocalDrive(FileSystem):
    prefix = None  # Default when no file system prefix is found.

    def __init__(self, path):
        if not os.access(path, os.R_OK):
            raise FileSystem.NoAccess('Cannot read directory')
        self.path = path

    def count_files(self):
        return sum(os.path.isfile(os.path.join(self.path, filename))
                   for filename in os.listdir(self.path))


data1 = FileSystem('nfs://192.168.1.18')
data2 = FileSystem('/tmp')  # Change as necessary for testing.

print(type(data1).__name__)  # -> Nfs
print(type(data2).__name__)  # -> LocalDrive
print(data2.count_files())  # -> <some number>


"""
在 Python 3.6 中，增加了一个 `__init_subclass__()` 方法，这个方法在创建子类时会被调用，
可以利用这个方法在基类中注册所有的子类。

"""


class FileSystem36(object):

    class NoAccess(Exception):
        pass

    class Unknown(Exception):
        pass

    # Regex for matching "xxx://" where x is any character except for ":".
    _PATH_PREFIX_PATTERN = re.compile(r'\s*([^:]+)://')
    _registry = {}  # Registered subclasses.

    @classmethod
    def __init_subclass__(cls, **kwargs):
        path_prefix = kwargs.pop('path_prefix', None)
        super().__init_subclass__(**kwargs)
        cls._registry[path_prefix] = cls  # Add class to registry.

    @classmethod
    def _get_prefix(cls, s):
        """ Extract any file system prefix at beginning of string s and
            return a lowercase version of it or None when there isn't one.
        """
        match = cls._PATH_PREFIX_PATTERN.match(s)
        return match.group(1).lower() if match else None

    def __new__(cls, path):
        """ Create instance of appropriate subclass. """
        path_prefix = cls._get_prefix(path)
        subclass = FileSystem36._registry.get(path_prefix)
        if subclass:
            return object.__new__(subclass)
        else:  # No subclass with matching prefix found (and no default).
            raise FileSystem.Unknown(
                f'path "{path}" has no known file system prefix')

    def count_files(self):
        raise NotImplementedError


class Nfs36(FileSystem36, path_prefix='nfs'):

    def __init__(self, path):
        pass

    def count_files(self):
        pass


class LocalDrive36(FileSystem36, path_prefix=None):  # Default file system.

    def __init__(self, path):
        if not os.access(path, os.R_OK):
            raise FileSystem.NoAccess('Cannot read directory')
        self.path = path

    def count_files(self):
        return sum(os.path.isfile(os.path.join(self.path, filename))
                   for filename in os.listdir(self.path))
