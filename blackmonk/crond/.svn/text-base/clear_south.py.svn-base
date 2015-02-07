#! /home/blackmonk/virtualenvs/bm/bin/python
import getsettings
import datetime,time
from south.models import MigrationHistory
from django.db import connection
SCHEMATA_DOMAINS = {
    '192.168.1.98': {
        'schema_name': 'onlinecalgarynet',
    },
    'onlinecalgary.com': {
        'schema_name': 'onlinecalgary',
    },
    'yourbondi.com.au': {
        'schema_name': 'yourbondi',
    },
    'bethesda.com': {
        'schema_name': 'bethesda',
    }
}
for domain in SCHEMATA_DOMAINS:
    connection.set_schemata_domain(domain)
    MigrationHistory.objects.all().delete()
