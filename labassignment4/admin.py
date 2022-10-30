from django.contrib import admin
from .models import Category, Product, Client, Order
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Order)