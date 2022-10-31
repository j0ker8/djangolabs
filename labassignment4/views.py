from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from .models import Category, Product, Client, Order
# Create your views here.

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    return render(request, 'labassignment4/index0.html', {'cat_list': cat_list})
    
def about(request):
    return render(request, 'labassignment4/about.html')
    
def detail(request,cat_no):
    #response = HttpResponse()
    cat_name = get_object_or_404(Category,pk=cat_no)
    catprods = Product.objects.filter(category=cat_no)
    return render(request, 'labassignment4/detail.html', {'cat_name': cat_name,'prod_list': catprods })
    