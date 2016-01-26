# -*- coding: utf-8 -*-
from com.ericsson.xn.commons import test_logger as test


def foo():
    test.passed('This step passed.')
    # test.error('Error occured.')
    test.failed('This step failed.')