from django.shortcuts import render, redirect
from datetime import date
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from .models import Category, Product, Client, Order
from .forms import OrderForm, InterestForm
from django.db.models import F
# Create your views here.

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    return render(request, 'labassignment4/index.html', {'cat_list': cat_list})
    
def about(request):
    return render(request, 'labassignment4/about.html')
    
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