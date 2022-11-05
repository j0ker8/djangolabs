from django.shortcuts import render
from datetime import date
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from .models import Category, Product, Client, Order
from .forms import OrderForm
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
    prodlist = Product.objects.all().order_by('id')[:10]
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
        
De