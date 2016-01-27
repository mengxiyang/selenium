# -*- coding: utf-8 -*-
import platform
import subprocess
from com.ericsson.xn.commons import test_logger


def pre_test_case(file_name, sub_dir):
    # set the system codec to 'utf-8'
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    test_logger.init(file_name, sub_dir)


def post_test_case():
    test_logger.finish()
    cmd = ''
    if 'Windows' == platform.system():
        cmd = 'TASKKILL /IM chromedriver.exe /F'
    elif 'Darwin' == platform.system():
        cmd = 'pkill chromedriver'
    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        p.kill()
    finally:
        pass
