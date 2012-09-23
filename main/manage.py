#!/usr/bin/env python
import os
#Add pydevd to the PYTHONPATH (may be skipped if that path is already added in the PyDev configurations)
import sys
sys.path.append(r'D:/eclipse/plugins/org.python.pydev_2.6.0.2012062818/pysrc')

import pydevd
pydevd.patch_django_autoreload(
patch_remote_debugger=True, #Connect to the remote debugger.
patch_show_console=True
)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
