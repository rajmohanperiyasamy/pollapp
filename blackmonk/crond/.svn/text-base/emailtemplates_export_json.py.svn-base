import getsettings
import json
from django.core import serializers

from usermgmt.models import EmailTemplates

allapps=EmailTemplates.objects.all().order_by('name')
json_serializer = serializers.get_serializer("json")()
data=json_serializer.serialize(allapps, ensure_ascii=False)
write_file = open("emailtemplate.json", "w")
write_file.write(data)
