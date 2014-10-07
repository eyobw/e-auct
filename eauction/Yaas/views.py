from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.template import loader, Context
from django.http import HttpResponse
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponseRedirect
import datetime

# Create your views here.

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('')
    else:
        return HttpResponseRedirect('')

