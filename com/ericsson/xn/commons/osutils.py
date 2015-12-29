# -*- coding: utf-8 -*-

import platform


def get_os_type():
    """
    Get the type of the platform, basic Windows, Linux, Darwin are enough.
    :return: the type of the system paltform.
    """
    return platform.system()