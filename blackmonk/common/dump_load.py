from common.models import ApprovalSettings,Pages,AvailableModules,MiscAttribute,SeoSettings,AvailableApps
from common.dump_load_utils import common_dump_data,common_load_data

DUMP_COMMON_TABLE_LIST=COMMON_TABLE_LIST=[
        {'file_name':'common_ApprovalSettings.json','model':ApprovalSettings,'filter':{}},
        {'file_name':'common_Pages.json','model':Pages,'filter':{'is_static':True}},
        {'file_name':'common_AvailableModules.json','model':AvailableModules,'filter':{}},
        {'file_name':'common_MiscAttribute.json','model':MiscAttribute,'filter':{'attr_key':'ROBOT_TXT'}},
        {'file_name':'common_SeoSettings.json','model':SeoSettings,'filter':{}}
    ]

DUMP_COMMON_TABLE_LIST.append({'file_name':'common_AvailableApps.json','model':AvailableApps,'filter':{}})

def dump_data():
    return common_dump_data(DUMP_COMMON_TABLE_LIST)

def load_data():
    return common_load_data(COMMON_TABLE_LIST)
