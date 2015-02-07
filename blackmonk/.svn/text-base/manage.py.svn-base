#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    try:
        if sys.argv[2]=='192.168.1.21:8889':
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blackmonk.ybsettings")
        else:os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blackmonk.settings")
    except:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blackmonk.settings")
    
    
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)