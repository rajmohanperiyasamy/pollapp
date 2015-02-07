from django.http import HttpResponse, HttpResponseRedirect
from django.template import  Template,Context
from django.template.loader import render_to_string
from xml.dom import minidom
import urllib
from article.models import Article


def check_is_owner(article,user):
    if article.created_by != user:
        url = reverse('article_dash_board', args=[article.id])
        return HttpResponseRedirect(url)
    else:
        return True

def from_articleurl_to_object(articleurl):
    try:
        slug = articleurl.split('/article/')[1].split('/')[1].split('.html')[0]
        return Article.objects.get(slug=slug)
    except:
        try:
            slug = articleurl.split('/article/')[1].split('.html')[0]
            return Article.objects.get(slug=slug)
        except:
            return False
    
def template_image(article):
    if article.template_type:
        if article.template_type == 'temp1':return 1
        elif article.template_type == 'temp2':return 2
        else:return 1
    else:
        return 1    
