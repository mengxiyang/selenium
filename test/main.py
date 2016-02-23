# -*- coding: utf-8 -*-

import os
import sys

root_dir = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
sys.path.insert(0, os.path.join(root_dir, 'libs' + os.path.sep + 'windows'))
import paramiko

if __name__ == '__main__':
    print paramiko.__version__