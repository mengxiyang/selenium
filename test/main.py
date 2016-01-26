# -*- coding: utf-8 -*-
from com.ericsson.xn.commons import test_logger
import Mod

if __name__ == '__main__':
    test_logger.init('pm_main', 'pm')
    test_logger.info('This is info testing.')
    Mod.foo()
    test_logger.finish()