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
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            return HttpResponseRedirect('')
    else:
        error = "Please Sign in"
        return render_to_response("/category.html", {'error': error},context_instance= RequestContext(request))
    return render_to_response("/category.html", {},context_instance= RequestContext(request))

def categories(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('')
    else:
        return HttpResponseRedirect('')

def new_category(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('')
    else:
        return HttpResponseRedirect('')