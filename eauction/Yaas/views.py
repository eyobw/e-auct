from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.template import loader, Context
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.core.mail import send_mail
from django.db.models import Max
from decimal import Decimal
from django.contrib.auth import logout
from django.core.context_processors import csrf
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONPRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from Yaas.models import Auction, AuctionState, AuctionCategory, Bidder
from Yaas.serializers import AuctionSerializer, BidSerializer
from Yaas.forms import RegistrationForm, AuctionForm, BidAuctionForm
from datetime import timedelta, datetime

siteLanguages = (('en', 'English'), ('fi', 'Finnish' ))

class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONPRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
# Create your views here.


def index(request):
    auction_list = Auction.objects.filter(end_date__gt=datetime.now()).order_by('end_date').filter(state_id=1)

    return render_to_response("index.html", {'auction_list': auction_list,'available_languages': ['en', 'fi']}, context_instance=RequestContext(request))


def item(request, e_id):
    try:
        product = Auction.objects.filter(state_id=1).get(id=e_id)
    except Auction.DoesNotExist:
        return HttpResponse(status=404)

    current_bid=''
    message = ''
    if request.user.is_authenticated():

        #Ban an auction
        if request.user.is_superuser:
            if request.POST.get('ban'):
                product.state_id=2
                product.save()
                bidders_email = Bidder.objects.filter(item=e_id)
                if bidders_email is not None:
                    for bidders in bidders_email:
                        email = bidders.bidder_name.email
                        send_mail('Banned','This auction has been banned!', request.user.email, [email], fail_silently=True)
                    message= 'Banned successfully'
                    return render_to_response("index.html", {'message': message}, context_instance=RequestContext(request))
        #End ban auction

        # Get the maximum bidding price if exists
        b_price = Bidder.objects.filter(item=e_id).aggregate(Max('price'))
        current_bid = b_price['price__max']
        #if current winning price does not exist compare with the starting price
        if b_price['price__max'] is None:
            if product.owner.id == request.user.id:
                message = 'you cannot bid on your item!'
            else:
                if request.GET:
                    price_val = Decimal(request.GET['price'])
                    #Check first if the bid price is greater than initial value
                    if price_val > product.price_min:
                        bid = Bidder(price=price_val, bidder_name_id=request.user.id, item_id=e_id)
                        bid.save()
                        #send email to the auction owner
                        send_mail('Auction created!','You have auctioned this product!','sender@yaas.com' , [request.user.email], fail_silently=True)
                        message = 'Maximum bid is ' + str(price_val)
                    else:
                        message = _('You should bid at least 0.01€ more than the initial value')
        else:
            current_bid = Bidder.objects.filter(item=e_id).get(price=Decimal(b_price['price__max']))

            if product.owner.id == request.user.id:
                message = 'You cannot bid your own item'
            else:
                if request.GET:
                    price_val = Decimal(request.GET['price'])
                    if Decimal(b_price['price__max']) < price_val:
                        #Check if user is bidding while he is winning
                        if current_bid.bidder_name.id == request.user.id:
                            message = _('You already bid, please wait until others bid')
                        else:
                            bid = Bidder(price=price_val, bidder_name_id=request.user.id, item_id=e_id)
                            bid.save()
                            send_mail('Someone has bid on the item you auctioned!','Someone has raised the bid!','sender@yaas.com' , [current_bid.bidder_name.email], fail_silently=True)
                            send_mail('Bidding has been made!','This bid has been created!','sender@yaas.com' , [request.user.email], fail_silently=True)
                            message = 'Maximum bid is ' + str(price_val)
                        return render_to_response("item.html",
                                                  {'item': product, 'user': request.user,'current': current_bid, 'message': message},
                                                  context_instance=RequestContext(request))

    return render_to_response("item.html",
                              {'item': product, 'user': request.user, 'current': current_bid, 'message': message},
                              context_instance=RequestContext(request))
#variable for new auction
new_auct=''

@login_required
def new_auction(request):
    auct = {}
    message = 'Auction'
    global new_auct
    form = AuctionForm()
    if request.POST.get('create'):
        form = AuctionForm(request.POST)
        #if form.is_valid():
        auct['auction_name'] = request.POST['auction_name']
        auct['auction_description'] = request.POST['auction_description']
        auct['price_min'] = request.POST['price_min']
        #auct['category'] = form.cleaned_data['category']
        auct['cat'] = request.POST['category']
        auct['end_date'] = request.POST['end_date']
        if (datetime.strptime(auct['end_date'], '%Y-%m-%d %H:%M:%S')- datetime.now()) > timedelta(hours=72):
            new_auct= Auction(auction_name=auct['auction_name'], auction_description=auct['auction_description'],
                     price_min=auct['price_min'], category_id=auct['cat'], end_date=auct['end_date'],owner_id=request.user.id)
            #form.save()
            auct['message'] = _("Are you sure you like to create this auction?")
            return render_to_response('confirm_auction.html', auct, context_instance=RequestContext(request))
        else:
            form = AuctionForm()
            args = {}
            args.update(csrf(request))
            args['form'] = form
            args['users'] = request.user.id
            args['message'] = _('Invalid input! Please fill the form again')
            return render_to_response('create_auction.html', args, context_instance=RequestContext(request))
    if request.POST.get('confirm'):
        new_auct.save()
        message = 'Auction created!!'
        send_mail('Auction created!','This auction has been created!','sender@yaas.com' , [request.user.email], fail_silently=True)
        return render_to_response('index.html', {'message': message}, context_instance=RequestContext(request))
    else:
        form = AuctionForm()
        args = {}
        args.update(csrf(request))
        args['form'] = form
        args['users'] = request.user.id
    return render_to_response('create_auction.html', args, context_instance=RequestContext(request))

def confirm(request):
    if request.POST:
        form = AuctionForm(request.POST)
    return render_to_response('confirm_auction.html')

def register(request):
    if request.user.is_anonymous():
        if request.POST:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                message = _("You have successfully registered!")
                return render_to_response('index.html', {'message': message}, context_instance=RequestContext(request))
        form = RegistrationForm()
        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render_to_response('register.html', args, context_instance=RequestContext(request))
    else:
        return render_to_response('index.html', context_instance=RequestContext(request))


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            message = _('Hello: ') + username
            return HttpResponseRedirect('/auctions/')
        else:
            error = "Username or Password is wrong"
            return render_to_response("index.html", {'message': error}, context_instance=RequestContext(request))
    return render_to_response("login.html", {'user': request.user}, context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/auctions/')


@login_required
def bid_auction(request):
    return ''


@login_required
def new_category(request):
    if request.method == 'POST':
        form = BidAuctionForm(request.POST)
        if form.is_valid():
            form.save()
            message =_("You have successfully created a category!")
            return render_to_response('index.html', {'message': message}, context_instance=RequestContext(request))
    form = BidAuctionForm()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('new_category.html', args, context_instance=RequestContext(request))


def edit_profile(request, e_id=1):
    if request.POST:
        form = ''
        if form.is_valid():
            form.save()
            message = _("You have successfully edited your email!")
            return render_to_response('index.html', {'message': message}, context_instance=RequestContext(request))
    else:
        form = AuctionForm()
        args = {}
        args.update(csrf(request))
        args = {'form': form, 'edit': Auction.objects.get(id=e_id)}
    return render_to_response('edit_profile.html', {'form': form, 'edit': Auction.objects.get(id=e_id)},
                              context_instance=RequestContext(request))


def search(request):
    query = request.GET['search']
    search_result = Auction.objects.filter(auction_name__contains=query).filter(state_id=1).filter(end_date__gt=datetime.today())
    return render_to_response('search_results.html', {'result': search_result},
                              context_instance=RequestContext(request))

def edit_auction(request, e_id=1):
    if request.POST:
        queryset = Auction.objects.get(id=e_id)
        form = AuctionForm(request.POST,instance=queryset)
        queryset.auction_description = request.POST['auction_description']
        queryset.save()
        return HttpResponseRedirect('/auctions/')
    else:
        queryset = Auction.objects.get(id=e_id)
        form = AuctionForm(instance=queryset)
        args = {}
        args.update(csrf(request))
        args = {'form': form, 'edit': Auction.objects.get(id=e_id)}
    return render_to_response('edit_auction.html', {'form': form, 'edit': Auction.objects.get(id=e_id)},
                              context_instance=RequestContext(request))



def my_profile(self):
    return ''

#Web service
@csrf_exempt
def auction_list(request):
    if request.method == 'GET':
        auction = Auction.objects.filter
        serializer = AuctionSerializer(auction, many=True)
        return JSONResponse(serializer.data)

@api_view(['GET'])
def list_detail(request, pk):
    try:
        auction = Auction.objects.get(pk=pk)
    except Auction.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AuctionSerializer(auction)
        return JSONResponse(serializer.data)


@login_required
@api_view(['POST'])
def bid_auction(request):
    if request.method == 'POST':
        serializer = BidSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.object.bidder_name = request.user
            b_price =Bidder.objects.filter(item=serializer.object.item.id).aggregate(Max('price'))
            if request.user == serializer.object.item.owner:
                return JSONResponse('You cannot bid on your own item', status=400)
            elif b_price['price__max'] is not None:
                current_bid = Bidder.objects.filter(item=serializer.object.item.id).get(price=Decimal(b_price['price__max']))
                if current_bid.bidder_name.id == request.user.id:
                    return JSONResponse('You cannot bid while you are winning', status=400)
            else:
                serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)