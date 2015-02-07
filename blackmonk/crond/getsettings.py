#! /home/blackmonk15/.virtualenv/bm/bin/python

import os, sys, re

server = True
if server:
    sys.path.insert(0,'/home/blackmonk15/webapps/moscowme')
    sys.path.append('/home/blackmonk15/webapps/moscowme/blackmonk')
    sys.path.append('/home/blackmonk15/webapps/moscowme/blackmonk/blackmonk')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
else:
    sys.path.insert(0,'/home/rajiv/ds_workspace/blackmonk3/')
    sys.path.append('/home/rajiv/ds_workspace/blackmonk3/')
    sys.path.append('/home/rajiv/ds_workspace/blackmonk3/blackmonk')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

