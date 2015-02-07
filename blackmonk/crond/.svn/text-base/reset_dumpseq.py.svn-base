import getsettings
from django.db import connection
from django.core import serializers
from django.core.management.color import no_style
from common.models import ApprovalSettings,Pages,AvailableModules,AvailableApps,MiscAttribute,SeoSettings
from community.models import Topic
from article.models import ArticleCategory,ArticlePrice
from attraction.models import AttractionCategory
from bookmarks.models import BookmarkCategory
from business.models import BusinessCategory,AttributeGroup,Attributes,AttributeValues,PaymentOptions,BusinessPrice
from buzz.models import Category
from classifieds.models import ClassifiedCategory,ClassifiedAttribute,ClassifiedPrice
from deal.models import DealCategory,Faqs,How
from events.models import EventCategory,EventPrice
#from forum.models import Category,Forum
from gallery.models import PhotoCategory
from usermgmt.models import EmailTemplates
from videos.models import VideoCategory
appmodels=[ApprovalSettings,Pages,AvailableModules,AvailableApps,MiscAttribute,SeoSettings,Topic,ArticleCategory,
ArticlePrice,AttractionCategory,BusinessCategory,AttributeGroup,Attributes,AttributeValues,PaymentOptions,BusinessPrice,
Category,ClassifiedCategory,ClassifiedAttribute,ClassifiedPrice,DealCategory,Faqs,How,EventCategory,EventPrice,Category,
PhotoCategory,EmailTemplates,VideoCategory]
sequence_sql = connection.ops.sequence_reset_sql(no_style(),appmodels)
if sequence_sql:
        print("Resetting sequence")
        cursor = connection.cursor()
        for command in sequence_sql:
            cursor.execute(command)

