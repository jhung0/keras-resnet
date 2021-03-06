# -*- coding: utf-8 -*-

"""

keras_resnet.blocks._time_distributed_2d
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements a number of popular time distributed two-dimensional residual blocks.

"""

import keras.layers
import keras.regularizers

parameters = {
    "kernel_initializer": "he_normal"
}


def time_distributed_basic_2d(filters, stage=0, block=0, kernel_size=3, numerical_name=False, stride=None):
    """

    A time distributed two-dimensional basic block.

    :param filters: the output’s feature space

    :param stage: int representing the stage of this block (starting from 0)

    :param block: int representing this block (starting from 0)

    :param kernel_size: size of the kernel

    :param numerical_name: if true, uses numbers to represent blocks instead of chars (ResNet{101, 152, 200})

    :param stride: int representing the stride used in the shortcut and the first conv layer, default derives stride from block id

    Usage:

        >>> import keras_resnet.blocks

        >>> keras_resnet.blocks.time_distributed_basic_2d(64)

    """
    if stride is None:
        if block != 0 or stage == 0:
            stride = 1
        else:
            stride = 2

    if keras.backend.image_data_format() == "channels_last":
        axis = 3
    else:
        axis = 1

    if block > 0 and numerical_name:
        block_identifier = "b{}".format(block)
    else:
        block_identifier = chr(ord('a') + block)

    stage_identifier = str(stage + 2)

    def f(x):
        y = keras.layers.TimeDistributed(keras.layers.Conv2D(filters, kernel_size, strides=stride, padding="same", **parameters), name="res{}{}_branch2a".format(stage_identifier, block_identifier))(x)
        y = keras.layers.TimeDistributed(keras.layers.BatchNormalization(axis=axis), name="bn{}{}_branch2a".format(stage_identifier, block_identifier))(y)
        y = keras.layers.TimeDistributed(keras.layers.Activation("relu"), name="res{}{}_branch2a_relu".format(stage_identifier, block_identifier))(y)

        y = keras.layers.TimeDistributed(keras.layers.Conv2D(filters, kernel_size, padding="same", **parameters), name="res{}{}_branch2b".format(stage_identifier, block_identifier))(y)
        y = keras.layers.TimeDistributed(keras.layers.BatchNormalization(axis=axis), name="bn{}{}_branch2b".format(stage_identifier, block_identifier))(y)

        if block == 0:
            shortcut = keras.layers.TimeDistributed(keras.layers.Conv2D(filters, (1, 1), strides=stride, padding="same", **parameters), name="res{}{}_branch1".format(stage_identifier, block_identifier))(x)
            shortcut = keras.layers.TimeDistributed(keras.layers.BatchNormalization(axis=axis), name="bn{}{}_branch1".format(stage_identifier, block_identifier))(shortcut)
        else:
            shortcut = x

        y = keras.layers.Add(name="res{}{}".format(stage_identifier, block_identifier))([y, shortcut])
        y = keras.layers.TimeDistributed(keras.layers.Activation("relu"), name="res{}{}_relu".format(stage_identifier, block_identifier))(y)

        return y

    return f


def time_distributed_bottleneck_2d(filters, stage=0, block=0, kernel_size=3, numerical_name=False, stride=None):
    """

    A time distributed two-dimensional bottleneck block.

    :param filters: the output’s feature space

    :param stage: int representing the stage of this block (starting from 0)

    :param block: int representing this block (starting from 0)

    :param kernel_size: size of the kernel

    :param numerical_name: if true, uses numbers to represent blocks instead of chars (ResNet{101, 152, 200})

    :param stride: int representing the stride used in the shortcut and the first conv layer, default derives stride from block id

    Usage:

        >>> import keras_resnet.blocks

        >>> keras_resnet.blocks.time_distributed_bottleneck_2d(64)

    """
    if stride is None:
        if block != 0 or stage == 0:
            stride = 1
        else:
            stride = 2

    if keras.backend.image_data_format() == "channels_last":
        axis = 3
    else:
        axis = 1

    if block > 0 and numerical_name:
        block_identifier = "b{}".format(block)
    else:
        block_identifier = chr(ord('a') + block)

    stage_identifier = str(stage + 2)

    def f(x):
        y = keras.layers.TimeDistributed(keras.layers.Conv2D(filters, (1, 1), strides=stride, padding="same", **parameters), name="res{}{}_branch2a".format(stage_identifier, block_identifier))(x)
        y = keras.layers.TimeDistributed(keras.layers.BatchNormalization(axis=axis), name="bn{}{}_branch2a".format(stage_identifier, block_identifier))(y)
        y = keras.layers.TimeDistributed(keras.layers.Activation("relu"), name="res{}{}_branch2a_relu".format(stage_identifier, block_identifier))(y)

        y = keras.layers.TimeDistributed(keras.layers.Conv2D(filters, kernel_size, padding="same", **parameters), name="res{}{}_branch2b".format(stage_identifier, block_identifier))(y)
        y = keras.layers.TimeDistributed(keras.layers.BatchNormalization(axis=axis), name="bn{}{}_branch2b".format(stage_identifier, block_identifier))(y)
        y = keras.layers.TimeDistributed(keras.layers.Activation("relu"), name="res{}{}_branch2b_relu".format(stage_identifier, block_identifier))(y)

        y = keras.layers.TimeDistributed(keras.layers.Conv2D(filters * 4, (1, 1), padding="same", **parameters), name="res{}{}_branch2c".format(stage_identifier, block_identifier))(y)
        y = keras.layers.TimeDistributed(keras.layers.BatchNormalization(axis=axis), name="bn{}{}_branch2c".format(stage_identifier, block_identifier))(y)

        if block == 0:
            shortcut = keras.layers.TimeDistributed(keras.layers.Conv2D(filters * 4, (1, 1), strides=stride, **parameters), name="res{}{}_branch1".format(stage_identifier, block_identifier))(x)
            shortcut = keras.layers.TimeDistributed(keras.layers.BatchNormalization(axis=axis), name="bn{}{}_branch1".format(stage_identifier, block_identifier))(shortcut)
        else:
            shortcut = x

        y = keras.layers.Add(name="res{}{}".format(stage_identifier, block_identifier))([y, shortcut])
        y = keras.layers.TimeDistributed(keras.layers.Activation("relu"), name="res{}{}_relu".format(stage_identifier, block_identifier))(y)

        return y

    return f
