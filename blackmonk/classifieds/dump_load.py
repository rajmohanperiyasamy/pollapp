from classifieds.models import ClassifiedCategory,ClassifiedAttribute,ClassifiedPrice
from common.dump_load_utils import common_dump_data,common_load_data

COMMON_TABLE_LIST=[
    {'file_name':'classified_ClassifiedCategory.json','model':ClassifiedCategory,'filter':{},'order_by':'-parent'},
    {'file_name':'classified_ClassifiedAttribute.json','model':ClassifiedAttribute,'filter':{}},
    {'file_name':'classified_ClassifiedPrice.json','model':ClassifiedPrice,'filter':{}},
]

def dump_data():
    return common_dump_data(COMMON_TABLE_LIST)

def load_data():
    return common_load_data(COMMON_TABLE_LIST)