from datetime import date, datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import F
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import InterestForm, OrderForm
from .models import Category, Client, Order, Product

# Create your views here.

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]

    if 'last_login' in request.session :
        logininfo = request.session['last_login']
    else :
        logininfo = 'Your last login was more than an hour ago'
    return render(request, 'labassignment4/index.html', {'cat_list': cat_list,'logininfo':logininfo})
    
def about(request):
    if 'about_visits' in request.session:
        last_visit = request.session['about_visits']
        request.session['about_visits']=last_visit+1
        request.session.set_expiry(10)        
    else :
        request.session['about_visits']=1
        last_visit=0
        request.session.set_expiry(300)
    return render(request, 'labassignment4/about.html',{'last_visit':last_visit})
    
def detail(request,cat_no):
    #response = HttpResponse()
    cat_name = get_object_or_404(Category,pk=cat_no)
    catprods = Product.objects.filter(category=cat_no)
    return render(request, 'labassignment4/detail.html', {'cat_name': cat_name,'prod_list': catprods })
    
def products(request):
    prodlist = Product.objects.all().order_by('id')
    return render(request,'labassignment4/products.html',{'prodlist':prodlist})

def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST' :
        form = OrderForm(request.POST,initial={'status_date':date.today(),'order_status':'Order Placed'})
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock :
                order.save()
                msg = 'Your order has been placed successfully'
            else:
                msg = 'We do not have sufficient sock to fill your order.'
            return render(request, 'labassignment4/order_response.html',{'msg':msg})
        
    else :
        form = OrderForm()
        return render(request, 'labassignment4/placeorder.html',{'form':form, 'msg':msg, 'prodlist':prodlist})
        
def productdetail(request, prod_id):
    prod = Product.objects.get(pk=prod_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['interested'] == 'Yes' :
                prod.interested = prod.interested + 1
                print(prod.id)
                prod.save()
                return redirect('/labassignment4/')
            else :
                return redirect('/labassignment4/')
    else :
        form = InterestForm()
        return render(request, 'labassignment4/productdetail.html',{'form':form,'prod':prod})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user :
            if user.is_active:
                if 'last_login' not in request.session :
                    request.session['last_login'] = str(datetime.now())
                    request.session.set_expiry(3600)
                login(request,user)
                return HttpResponseRedirect(reverse('labassignment4:index'))
            else:
                return HttpResponse('Your account is disabled')
        else :
            return HttpResponse('Invalid Login details')
    else :
        return render(request, 'labassignment4/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('labassignment4:index'))

def myorders(request):
    if request.user.is_authenticated :
        try :
            usobjid = Client.objects.get(pk=request.user.id)
            orderset = usobjid.order_set.all()
            #return HttpResponse(orderset)
        except: 
            return HttpResponse("This user name is not registered")
        
        return render(request, 'labassignment4/myorders.html',{'orderset':orderset})
    else :
        return HttpResponse("User not authenticated")
