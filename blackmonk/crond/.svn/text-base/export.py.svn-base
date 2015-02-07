#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Warning: This python script is designed for Django 0.96.

It exports data from models quite like the `dumpdata` command, and throws the
data to the standard output.


It fixes glitches with unicode/ascii characters. It looked like the 0.96
handles very badly unicode characters, unless you specify an argument that is
not available via the command line. The simple usage is:

    $ python export_models.py -a <application1> [application2, application3...]

As a plus, it allows you to export only one or several models inside your
application, and not all of them:

    $ python export_models.py application1.MyModelStuff application1.MyOtherModel

Of course, you can specify the output format (serializer) with the -f
(--format) option.

    $ python export_models.py --format=xml application1.MyModel

"""
import sys
import os
from optparse import OptionParser
import getsettings
from django.db import connection


from django.conf import settings



from django.core import serializers
from django.db.models import get_app, get_apps, get_models, get_model
#connection.set_schemata_domain('bethesda.com')
def get_options():
    "defines options and arguments"
    usage = """usage: %prog [-d] [-f format] app1.model1 app2.model2...
    or
    %prog -a app1 app2
    """
    parser = OptionParser(usage)
    parser.add_option("-f", "--format", dest="format",
        action="store", type="string", default="json",
        help="format may be 'yaml' or 'json'. Default is 'json'")
    parser.add_option("-d", "--debug", dest="debug",
        action="store_true", default=False,
        help="prints debug information")
    parser.add_option("-a", "--all", dest="all",
        action="store_true", default=False,
        help='serialises every model available in the given applications'
    )
    return parser.parse_args()

def main():
    "main program"
    data = open('/home/renjith/workspace/blackmonk/crond/article.json')
    print data
    for deserialized_object in serializers.deserialize("json", data):
        if deserialized_object:
            print deserialized_object
        else:
            print "error"    

if __name__ == '__main__':

    main()

# EOF