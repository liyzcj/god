# -*- coding: utf-8 -*-
'''
@Description: Import Utils
@Author: Li Yanzhe
@Date: 2019-12-04 20:53:04
@LastEditors: Li Yanzhe
@LastEditTime: 2019-12-05 11:40:57
@Copyright (c) 2019 Senses Intelligence
'''
import importlib.util
from typing import Text, Callable


def import_func_from_file(file_path: Text, func_name: Text) -> Callable:

    try:
        spec = importlib.util.spec_from_file_location('user_module', file_path)

        if not spec:
            raise ImportError()

        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)
        return getattr(user_module, func_name)

    except IOError:
        raise ImportError("{} in {} not found in import_func_from_file"
                          .format(func_name, file_path))
