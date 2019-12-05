# -*- coding: utf-8 -*-
'''
@Description: Tensorflow test things
@Author: Li Yanzhe
@Date: 2019-12-05 17:26:13
@LastEditors: Li Yanzhe
@LastEditTime: 2019-12-05 17:38:05
@Copyright (c) 2019 Senses Intelligence
'''
import tensorflow as tf


def gpu():
    is_avaliable = tf.test.is_gpu_available()
    print("Is GPU avaliable? {}".format(is_avaliable))
    if is_avaliable:
        print("GPU device name: {}".format(tf.test.gpu_device_name()))
        print("Is built with CUDA? {}".format(tf.test.is_built_with_cuda()))
        print("Is built with GPU support? {}".format(
            tf.test.is_built_with_gpu_support()))
        print("Is built with ROCm? {}".format(tf.test.is_built_with_rocm()))