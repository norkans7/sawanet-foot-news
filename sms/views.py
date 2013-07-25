from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from parser import Parser
import datetime
import urllib2
import urllib
import json
import re
from wiki import get_summary
from smartmin.views import *
from .models import *

class IndexView(SmartTemplateView):
    template_name = 'sms/index.html'


class SMSCRUDL(SmartCRUDL):
    model = SMS
    actions = ('create', 'list', 'read', 'update')


class TagCRUDL(SmartCRUDL):
    model = Tag
    actions = ('create', 'list', 'read', 'update')
        

def unescape(s):
    from htmlentitydefs import name2codepoint
    name2codepoint['#39'] = 39    
    return re.sub('&(%s);' % '|'.join(name2codepoint),
                  lambda m: unichr(name2codepoint[m.group(1)]), s)

def clean(data):
    p = re.compile(r'</?[^\W].{0,10}?>')
    stripped = p.sub('', data)

    p = re.compile(r'\s+')
    cleaned = p.sub(' ', stripped)

    return unescape(cleaned)

def lookup(keyword):
    messages = SMS.objects.filter(tags__name=keyword).order_by('?')

    if messages:
        return messages[0].text

    return None
    

# this is where we receive our SMS message
@csrf_exempt
def receive(request):
    # POST means we should process things
    if request.method == 'POST':
        parser = Parser(request.REQUEST['text'])

        # this just strips the first word, which is our keyword 'who'
        keyword = parser.next_word()

        
        # try to look up the item
        summary = lookup(keyword)

        if summary:
            return HttpResponse(summary)
        else:
            return HttpResponse("Sorry, there are no update for %s." % keyword)

    # this request is a GET, so we should display a form instead
    else:
        return render_to_response('sms/receive.html',
                                  dict(),
                                  context_instance=RequestContext(request))


