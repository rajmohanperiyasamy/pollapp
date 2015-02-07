#! /home/blackmonk/virtualenvs/bm/bin/python
import os, sys
sys.path.append(os.pardir)
import getsettings
from django.core import serializers
from django.utils.html import escape

app_name = "deal"     #Give App name and run

class XMLWriter:
    def __init__(self, pretty=True):
        self.output = ""
        self.stack = []
        self.pretty = pretty
        
    def open(self, tag):
        self.stack.append(tag)
        if self.pretty:
            self.output += "  "*(len(self.stack) - 1);
        self.output += "<" + tag + ">"
        if self.pretty:
            self.output += "\n"
        
    def close(self):
        if self.pretty:
            self.output += "\n" + "  "*(len(self.stack) - 1);
        tag = self.stack.pop()
        self.output += "</" + tag + ">"
        if self.pretty:
            self.output += "\n"
        
    def closeAll(self):
        while len(self.stack) > 0:
            self.close()
        
    def content(self, text):
        try:txt = text.encode("ascii","ignore")
        except:txt=text
        data = escape(txt)
        if self.pretty:
            self.output += "  "*len(self.stack);
        self.output += unicode(data)

    def save(self, filename):
        self.closeAll()
        fp = open(filename, "w")
        fp.write(self.output)
        fp.close()
    
    

import django.db.models 

writer = XMLWriter(pretty=False)
writer.output+="<?xml version=\"1.0\"?>"
writer.open("djangoexport_"+app_name)
app = django.db.models.get_app(app_name)
models = django.db.models.get_models(app)
for model in models:
    writer.open(model._meta.object_name+"s")
    for item in model.objects.all():
        writer.open(model._meta.object_name)
        for field in item._meta.fields:
            writer.open(field.name)
            value = getattr(item, field.name)
            if value != None:
                if isinstance(value, django.db.models.base.Model):
                    pk_name = value._meta.pk.name
                    pk_value = getattr(value, pk_name)
                    writer.content(pk_value)
                else:
                    writer.content(value)
            writer.close()
        writer.close()
    writer.close() 
writer.close()        
writer.save("export_db.xml")


