from django.contrib import admin
#from article.models import Article
#from article.models import Author
from article.models import ClientsData
from article.models import Accounts
from article.models import Clients
from task.models import Task
from task.models import Employees
from article.models import Document
#admin.site.register(Article)
#admin.site.register(Author)
admin.site.register(Task)
admin.site.register(Accounts)
admin.site.register(Clients)
admin.site.register(Employees)
admin.site.register(Document)
# Register your models here.