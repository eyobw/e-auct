from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.template import loader, Context
from django.http import HttpResponse
from django.contrib.auth import logout
from django.core.context_processors import csrf
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponseRedirect
from Yaas.models import Auction, AuctionState, AuctionCategory
from Yaas.forms import RegistrationForm, AuctionForm, AuctionCategoryForm, EditProfileForm
import datetime

# Create your views here.

def index(request):
    auction_list = Auction.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            message = 'Hello: '+username
            return render_to_response("index.html", {'message': message, 'auction_list':auction_list},context_instance= RequestContext(request))
        else:
            error = "Username or Password is wrong"
            return render_to_response("index.html", {'message': error, 'auction_list': auction_list},context_instance= RequestContext(request))
    return render_to_response("index.html", {'auction_list': auction_list,'user':request.user},context_instance= RequestContext(request))

def item(request, e_id):
    item = Auction.objects.get(id=e_id)

    if request.user.is_authenticated():
        return render_to_response("item.html", {'item':item} ,context_instance= RequestContext(request))
    else:
        return render_to_response("item.html", {'item':item, 'user': request.user} ,context_instance= RequestContext(request))
@login_required
def new_auction(request):
    user = request.user.id
    if request.method == 'POST':
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.owner_id = user
            form.save()
            message = "You have successfully created an auction!"
            return render_to_response('index.html', {'message':message}, context_instance= RequestContext(request))
    form = AuctionForm()
    args = {}
    args.update(csrf(request))
    args['form']=form
    args['user'] = user
    return render_to_response('create_auction.html', args,context_instance= RequestContext(request) )

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
    return render_to_response('register.html', args, context_instance= RequestContext(request) )

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            message = 'Hello: '+username
            return render_to_response("index.html", {'message': message, },context_instance=RequestContext(request))
        else:
            error = "Username or Password is wrong"
            return render_to_response("index.html", {'message': error},context_instance=RequestContext(request))
    return render_to_response("login.html", {'user':request.user },context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/auctions/')

@login_required
def bid_auction(request):
    return ''

def new_category(request):
    if request.method == 'POST':
        form = AuctionCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            message = "You have successfully created a category!"
            return render_to_response('index.html', {'message':message}, context_instance= RequestContext(request))
    form = AuctionCategoryForm()
    args = {}
    args.update(csrf(request))
    args['form']=form
    return render_to_response('new_category.html', args,context_instance= RequestContext(request) )

def edit_profile(request, e_id=1):
    if request.POST:
        form = EditProfileForm()
        if form.is_valid():
            form.save()
            message = "You have successfully edited your email!"
            return render_to_response('index.html', {'message':message}, context_instance= RequestContext(request))
    else:
        form = EditProfileForm()
        args = {}
        args.update(csrf(request))
        args ={'form': form, 'edit': Auction.objects.get(id=e_id)}
    return render_to_response('edit_profile.html',{'form': form,'edit': Auction.objects.get(id=e_id)}, context_instance=RequestContext(request))

def search(request):
    query = request.GET['search']
    search_result = Auction.objects.filter(auction_name__contains=query)

    return render_to_response('search_results.html',{'result': search_result},context_instance=RequestContext(request))
