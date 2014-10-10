from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.template import loader, Context
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponseRedirect
from Yaas.models import Auction, AuctionState, AuctionCategory
from Yaas.forms import RegistrationForm, AuctionForm, AuctionCategoryForm
import datetime

# Create your views here.

def index(request):
    auction_list = Auction.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            message = 'Hello: '+username
            return render_to_response("index.html", {'message': message, 'auction_list':auction_list},context_instance= RequestContext(request))
        else:
            error = "Username or Password is wrong"
            return render_to_response("index.html", {'message': error},context_instance= RequestContext(request))
    return render_to_response("index.html", {'auction_list': auction_list, },context_instance= RequestContext(request))

def item(request, e_id):
    item = Auction.objects.get(id=e_id)

    if request.user.is_authenticated():
        return render_to_response("item.html", {'item':item} ,context_instance= RequestContext(request))
    else:
        return render_to_response("item.html", {'item':item} ,context_instance= RequestContext(request))

def new_auction(request):
    if request.user.is_authenticated():
        if request.POST:
            form = AuctionForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/myblog')
        else:
            form = AuctionForm()
            args = {}
            args.update(csrf(request))
            args['form'] = form
            return render_to_response('MyBlog/addblog.html',args)
    else:
        return HttpResponseRedirect('')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            message = "You have successfully registered!"
            return render_to_response('index.html', {'message':message}, context_instance= RequestContext(request))
    form = RegistrationForm()
    args = {}
    args.update(csrf(request))
    args['form']=form
    return render_to_response('register.html', args,context_instance= RequestContext(request) )


