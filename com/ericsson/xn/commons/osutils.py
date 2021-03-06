# -*- coding: utf-8 -*-

import platform
from .PyProperties import TrimableProps


def get_os_type():
    """
    Get the type of the platform, basic Windows, Linux, Darwin are enough.
    :return: the type of the system paltform.
    """
    return platform.system()


def get_ne_info_from_cfg(cfg_path):
    return TrimableProps(cfg_path).dict_info()


def get_pm_counters_map(counter_directory):
    return TrimableProps(counter_directory).dict_info()


def get_me_types_map(me_types_cfg):
    return TrimableProps(me_types_cfg).dict_info()