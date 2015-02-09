from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from article.models import Document
from article.forms import DocumentForm
# Create your views here.
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic.base import TemplateView
from django.template import Context
import random, re, os, datetime, time, urllib
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from article.models import Clients
#from article.models import Person,Group,Membership
#from article.models import Author
#from article.models import AuthorForm
#from article.forms import ArticleForm
#from article.forms import ContactForm
from article.models import ClientsData
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


def home(request,template='article/add_article.html'):
    #data={'First_name':Fname,'last_name':Lname,'designation':Designation}
    author = 'author'
    article = 'article'
    image ='images'
    video = 'videos'
    contact ='contacts'
    data={'author':author,'article':article,'images':image,'videos':video,'contacts':contact}
    return render_to_response('home.html',data,context_instance=RequestContext(request))
def hello(request):
    name = 'raj'
    html = "<Html><body bgcolor='skyblue'>HI %s , This seems to worked <body></Html>" % name
    return HttpResponse(html)

def hello_template(request):
    name = "mike"
    t = get_template('hello.html')
    html = t.render(Context({'name':name}))
    return HttpResponse(html)

def Test(request):
    t = get_template('jq.html')
    html = t.render(Context({}))
    return HttpResponse(html)


class HelloTemplate(TemplateView):
    template_name = 'hello_class.html'
    
    def get_context_data(self, **kwargs):
        context = super(HelloTemplate, self).get_context_data(**kwargs)
        context['name'] = 'rajmohan'
        return context
    
    
#def add_author(request):
#    name1 = "Rajmohannn"
#    print name1
#    x = Article.objects.all().order_by('-id')[0]
#    print x
#    
#
#    f = AuthorForm()
#
#    print f 
#    return render_to_response('add_article.html',{'name': name1,'x': x,'form':f },context_instance=RequestContext(request))

def add_author(request,pk=0,template='article/add_author.html'):
    data={}
    author_object=None
    try:
        author_object = Author.objects.get(id = pk)
        form=AuthorForm(instance=author_object)
        print'trrrrrrrrrrrrrrrrr'
    except:
        print'exceeeeeeeeeeept'
        form = AuthorForm()
    if request.POST:
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            print'second'
            print form
            author = Author.objects.all().order_by('-id')[0]
            all_authors = Author.objects.all()
            time = datetime.now()
            return render_to_response('success.html',{'form':form,'author':author,'time':time,'all_authors':all_authors},context_instance=RequestContext(request))
           
    return render_to_response('add_author.html',{'form':form },context_instance=RequestContext(request))


def add_article(request):
    x = ArticleForm()
    print x
    if request.POST:
        x = ArticleForm(request.POST)
        if x.is_valid():
            x.save()
            print'second'
            print x
            article = Article.objects.all().order_by('-id')[0]
            time = datetime.now()
            return render_to_response('success.html',{'form':x,'author':article,'time':time},context_instance=RequestContext(request))
           
    return render_to_response('add_article.html',{'form':x },context_instance=RequestContext(request))


def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['rajmohan@doublespring.com']
            if cc_myself:
                recipients.append(sender)

            from django.core.mail import send_mail
            send_mail(subject, message, sender, recipients)
            return render_to_response('success_mail.html',context_instance=RequestContext(request))
    else:
        form = ContactForm() # An unbound form

    return render(request, 'contact.html', {
        'form': form,
    })
@login_required(login_url='/admin/')
def calculate(request):
    data={}
    client = Clients.objects.all()
    print client
    data['client'] = client
    return render_to_response('calculate.html',data,context_instance=RequestContext(request))

@login_required(login_url='/admin/') 
def clients_data(request,pk=0):
    data = {}
    
#    object=Clients.objects.prefetch_related('album_photos').filter(created_by__profile_slug=username).order_by('-id')
#    article = Article.objects.prefetch_related('tags').select_related('category','created_by').get(slug=slug,status='P')
#    cat = model.objects.filter(id__in=id)
    print"primary_key",pk
    name = Clients.objects.distinct().get(id=pk)
    print"ggg",name
    list = []
    accounts = ClientsData.objects.filter(name_id=pk).select_related('accounts')
    for x in accounts:
        list.append(x.name)
        print x.name
        
#    articles = Article.objects.defer('content','summary').filter(created_by=request.user).select_related('category','created_by').order_by('-created_on')
#    print accounts.pending
    
    
#    for x in accounts.all:
#        print x
#    client1 = ClientsData.objects.get(id=pk)
#    print"pending",client1.pending
#    print"name",client1.name
#    print"completed",client1.completed
#    print"status",client1.status
#    print"added_date",client1.added_date
#    print"account",client1.account
    
    
    data['client'] = accounts
    data['list'] = list
    data['name'] = name
    return render_to_response('clients_data.html',data,context_instance=RequestContext(request))  
    
def report(request):
    print"status",request.POST['select_client']
    
    status = request.POST['select_client']
    
    if status == '0':
        print "inside if"
        date=request.POST['date']
        data = {}
        cleint_rep_data = ClientsData.objects.filter(added_date=date)
        data['cleint_rep_data'] = cleint_rep_data
        return render_to_response('clients_report.html',data,context_instance=RequestContext(request))
    else:
        print "elseeeee"
        date=request.POST['date']
        data = {}
        cleint_rep_data = ClientsData.objects.filter(added_date=date,name_id=status)
        data['cleint_rep_data'] = cleint_rep_data
        
        return render_to_response('clients_report.html',data,context_instance=RequestContext(request))
    
def date(request):
    data = {}
    clients = Clients.objects.all()
    for x in clients:
        print x.id
        print x.first_name
    
    data['clients'] =clients
    return render_to_response('date_picker.html',data,context_instance=RequestContext(request))
    
def fetch_images(request):
    data = {}
    clients = Clients.objects.all()
    for x in clients:
        print x.id
        print x.first_name
    
    data['clients'] =clients
    return render_to_response('fetch_images.html',data,context_instance=RequestContext(request))
  
def get_img_url(site, url):
    prefixes = [ "http://", "https://" ]
    if True in [ prefix in url for prefix in prefixes ]: return url
    else: return '%s/%s' % ([ prefix + (site.split(prefix)[1]).split('/')[0] for prefix in prefixes if prefix in site ][0], url)
      
def fetch(request):
    source_url=request.POST['bmname']
    source_url = source_url.replace(' ', '+')
    source_html = urllib2.urlopen(source_url)
    soup = BeautifulSoup(source_html)
    for title in soup.title:
            b_title = title.string[:200]
            b_seo_description = title
    
    img_urls = []
    img_urls_rem = []        
    try:
        for img in soup.find_all("img"):
            print"inside for"
            Image_url = get_img_url(source_url, img['src'])
            print"Image_url",Image_url
            if (True in [img_ext in Image_url for img_ext in ['.jpg', '.jpeg', '.png']]) and ('captcha' not in Image_url):
                img_urls.append(Image_url)
        for img in soup.find_all(lambda tag: tag.name == "img" and tag.has_key("width") and int(filter_number(tag["width"])) < 80):
            img_urls_rem.append(get_img_url(source_url, img['src']))
    except:
        pass
    data = {}
    data['img_url_list'] = list(set(img_urls) - set(img_urls_rem))
    return render_to_response('fetch.html',data,context_instance=RequestContext(request))
    

from reportlab.pdfgen import canvas
from django.http import HttpResponse

def download(request,pk=0):
    doc = Document.objects.distinct().get(id=pk)
    fname=doc.docfile.name
    print"SSSSSSsssss",fname
    import urllib;   
    url ="http://192.168.1.59:8005/media/"+fname
    print"url",url
    opener = urllib.urlopen(url);  
    mimetype = "application/octet-stream"
    response = HttpResponse(opener.read(), mimetype=mimetype)
    response["Content-Disposition"]= "attachment; filename=aktel.pdf"
    return response 
#    doc = Document.objects.distinct().get(id=pk)
#    fname=doc.docfile.name
#    print"f namme",doc.docfile
#    # Create the HttpResponse object with the appropriate PDF headers.
#    response = HttpResponse(content_type='application/pdf')
#    response['Content-Disposition'] = 'attachment; filename=tutorials.pdf'
#
#    # Create the PDF object, using the response object as its "file."
#    p = canvas.Canvas(response)
#
#    # Draw things on the PDF. Here's where the PDF generation happens.
#    # See the ReportLab documentation for the full list of functionality.
#    p.drawString(100, 100, "Hello world.")
#
#    # Close the PDF object cleanly, and we're done.
#    p.showPage()
#    p.save()
#    return response
#def download_file(request,pk=0):
#    global dump
#    fname=doc.docfile.name
##    url = "http://randomsite.com/file.gz"
#    url ="http://192.168.1.59:8005/media/"+fname
#    file = requests.get(url, stream=True)
#    dump = file.raw



def list(request):
    # Handle file upload
    print"fffffff"
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('article.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )