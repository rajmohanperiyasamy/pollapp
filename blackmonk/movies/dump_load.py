from movies.models import MovieType,MovieLanguage 
from common.dump_load_utils import common_dump_data,common_load_data

COMMON_TABLE_LIST=[
    {'file_name':'movie_MovieType.json','model':MovieType,'filter':{}},
    {'file_name':'movie_MovieLanguage.json','model':MovieLanguage,'filter':{}},
]

def dump_data():
    return common_dump_data(COMMON_TABLE_LIST)

def load_data():
    return common_load_data(COMMON_TABLE_LIST) 
    
