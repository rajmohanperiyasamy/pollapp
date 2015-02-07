from article.models import ArticleCategory,ArticlePrice
from common.dump_load_utils import common_dump_data,common_load_data

COMMON_TABLE_LIST=[
        {'file_name':'article_ArticleCategory.json','model':ArticleCategory,'filter':{}},
        {'file_name':'article_ArticlePrice.json','model':ArticlePrice,'filter':{}},
    ]

def dump_data():
    return common_dump_data(COMMON_TABLE_LIST)

def load_data():
    return common_load_data(COMMON_TABLE_LIST)