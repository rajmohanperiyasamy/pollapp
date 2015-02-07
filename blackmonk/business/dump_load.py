from business.models import BusinessCategory,AttributeGroup,Attributes,AttributeValues,PaymentOptions,BusinessPrice
from common.dump_load_utils import common_dump_data,common_load_data

COMMON_TABLE_LIST=[
    {'file_name':'business_BusinessCategorys.json','model':BusinessCategory,'filter':{},'order_by':'-parent_cat'},
    {'file_name':'business_AttributeGroup.json','model':AttributeGroup,'filter':{}},
    {'file_name':'business_Attributes.json','model':Attributes,'filter':{}},
    {'file_name':'business_AttributeValues.json','model':AttributeValues,'filter':{}},
    {'file_name':'business_PaymentOptions.json','model':PaymentOptions,'filter':{}},
    {'file_name':'business_BusinessPrice.json','model':BusinessPrice,'filter':{}},
]
        
def dump_data():
    return common_dump_data(COMMON_TABLE_LIST)

def load_data():
    return common_load_data(COMMON_TABLE_LIST)