import sys
import getsettings
from business.models import BusinessCategory,AttributeGroup,Attributes
from business.models import Business,AttributeValues,BizAttributes

def fix_attr(bus):
    attr=Attributes.objects.all()
    for atr in attr:
        try:
            buz=BizAttributes.objects.get(business=bus,key=atr)
            pass
        except BizAttributes.DoesNotExist:
            pass
        except:
            allbuz=BizAttributes.objects.filter(business=bus,key=atr)
            buztoadd=allbuz[0]
            for id,b in enumerate(allbuz):
                for x in b.value.all():
                    buztoadd.value.add(x)
                if id!=0:
                    b.delete()
            
for bus in Business.objects.all():
    fix_attr(bus)
    