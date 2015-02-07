from django.core import serializers
from django.conf import settings as my_settings
from django.contrib.auth import get_user_model
User = get_user_model()

from common.utils import get_global_settings
from common.constant_replace import REPLACE_TUPLE

JSON_PATH=my_settings.PROJECT_PATH+'/common/dumped_data/'

def common_dump_data(table_list):
    json_serializer = serializers.get_serializer("json")()
    
    for table in table_list:
        try:data_obj=table['model'].objects.filter(**table['filter']).order_by(table['order_by'])
        except:data_obj=table['model'].objects.filter(**table['filter'])
        with open(JSON_PATH+table['file_name'], "w") as out:
            json_serializer.serialize(data_obj, ensure_ascii=True,stream=out)
    return ""

def common_load_data(table_list):
    user=User.objects.filter(is_superuser=True).order_by('id')[0]
    for table in table_list:
        data = open(JSON_PATH+table['file_name']).read()
        if REPLACE_TUPLE:
            for key,value in REPLACE_TUPLE:
                data=data.replace(key,value)
        for obj in serializers.deserialize("json", data):
            djobj = obj.object
            try:
                djobj.created_by=user
                djobj.modified_by=user
            except:pass
            djobj.save()
    return ""

def common_load_availableapps(table_list):
    for table in table_list:
        data = open(JSON_PATH+table['file_name']).read()
        for obj in serializers.deserialize("json", data):
            djobj = obj.object
            djobj.save()
    return ""

