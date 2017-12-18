# -*- coding: utf-8 -*-

import os


def get_keys():
    with open(os.path.join(get_config_dir(), "keys.txt"), "r") as keys_file:
        keys = keys_file.readlines()
        keys[0] = keys[0][:-1]

    return keys


def get_main_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def get_config_dir():
    return os.path.join(get_main_dir(), "configs")


def get_data_dir2():
    # todo: refact this
    return os.path.join(get_main_dir(), "data/")


def get_data_dir(exchanger):
    return os.path.join(get_main_dir(), "data/{}.database".format(exchanger))


print get_config_dir()
