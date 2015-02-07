from deal.models import DealCategory,Faqs,How
from common.dump_load_utils import common_dump_data,common_load_data

COMMON_TABLE_LIST=[
    {'file_name':'deal_DealCategory.json','model':DealCategory,'filter':{}},
    {'file_name':'deal_Faqs.json','model':Faqs,'filter':{}},
    {'file_name':'deal_How.json','model':How,'filter':{}}
]

def dump_data():
    return common_dump_data(COMMON_TABLE_LIST)

def load_data():
    return common_load_data(COMMON_TABLE_LIST)        