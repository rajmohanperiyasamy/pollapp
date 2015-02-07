from events.models import EventCategory,EventPrice
from common.dump_load_utils import common_dump_data,common_load_data

COMMON_TABLE_LIST=[
    {'file_name':'event_EventCategory.json','model':EventCategory,'filter':{}},
    {'file_name':'event_EventPrice.json','model':EventPrice,'filter':{}},
]
        
def dump_data():
    return common_dump_data(COMMON_TABLE_LIST)

def load_data():
    return common_load_data(COMMON_TABLE_LIST)
