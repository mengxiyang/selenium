# -*- coding: utf-8 -*-
import os
import subprocess

if __name__ == '__main__':
    py_path = os.path.normpath("C:\\Users\\EJLNOQC\\installed\\python27\\python.exe")
    pwd_dir = os.path.dirname(os.path.abspath(__file__))
    gui_case_file = os.path.normpath(pwd_dir + os.path.sep + 'case_main_imshss_pm_and_me.py')
    nbi_case_file = os.path.normpath(pwd_dir + os.path.sep + 'case_main_imshss_nbi.py')

    cmd_nbi = py_path + ' ' + nbi_case_file
    cmd_gui = py_path + ' ' + gui_case_file
    p_gui = subprocess.Popen(cmd_gui, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p_gui.wait()
    try:
        p_gui.kill()
    except Exception as e:
        pass

    p = subprocess.Popen(cmd_nbi, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    try:
        p.kill()
    except Exception as e:
        pass
