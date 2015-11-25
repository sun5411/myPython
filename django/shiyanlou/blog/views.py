# Create your views here.
from django.http import Http404,HttpResponse
#from django.template import loader,Context
from django.shortcuts import render_to_response
import datetime
'''
def index(req):
    t = loader.get_template('index1.html')
    C = Context({})
    return HttpResponse(t.render(C))

def index(req):
    return render_to_response('index1.html',{})

def index(req):
    return render_to_response('index.html',{'title':'MySite','name':'Ning'})
'''
class Person(object):
    def __init__(self,name,age,sex):
        self.name = name
        self.age = age
        self.sex = sex

    def say(self):
        return "I'm " + self.name



def index(req):
    #user={'name':'Sun Ning','age':30,'sex':'male'}
    u = Person('SunNing',30,'male')
    lists=('python','php','java','C')
    return render_to_response('index.html',{'title':'MySite','user':u,'booklist':lists})

def hello(request):
    return HttpResponse("Hello world!")

def current_date(req):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>"%now
    return HttpResponse(html)

def hours_ahead(request, offset):
    try:
        offset = int(offset)
        print type(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)
