from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from .models import Category, Product, Client, Order
# Create your views here.

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    response = HttpResponse()
    heading1 = '<p>' + 'List of categories: '+'</p>'
    response.write(heading1)
    for category in cat_list:
        para = '<p>' + str(category.id) + ': ' + str(category) + '</p>'
        response.write(para)
    
    response.write('<br><br>')
    product_list = Product.objects.all().order_by('-price')[:5]
    product_heading = '<p>' + 'List of products: ' + '</p>'
    response.write(product_heading)
    for prod in product_list :
        para = '<p>' + str(prod.name) + ': ' + str(prod.price) + '</p>'
        response.write(para)
    return response
    
def about(request):
    response = HttpResponse("This is an Online Store APP.")
    return response
    
def detail(request,cat_no):
    response = HttpResponse()
    try :
        cat_names = Category.objects.all()[cat_no-1:cat_no]
        para = '<p>'+str(cat_names[0].name)+'</p>'
        response.write(para)
    except :
        raise Http404('Object not found')
    return response