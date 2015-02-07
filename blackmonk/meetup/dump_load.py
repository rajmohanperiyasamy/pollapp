from meetup.models import MeetupTopics
from common.dump_load_utils import common_dump_data,common_load_data

COMMON_TABLE_LIST=[{'file_name':'meetup_MeetupTopics.json','model':MeetupTopics,'filter':{}} ]

def dump_data():
    return common_dump_data(COMMON_TABLE_LIST)

def load_data():
    return common_load_data(COMMON_TABLE_LIST)
    