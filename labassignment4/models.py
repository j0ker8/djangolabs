from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
        
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100, validators=[MinValueValidator(0),MaxValueValidator(1000)])
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True,default='')
    interested = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name
        
    def refill(self):
        self.stock = self.stock+100
        return self.stock
    
class Client(User): 
    PROVINCE_CHOICES = [('AB', 'Alberta'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec')]
    company = models.CharField(max_length=50, blank=True, default='')
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20,default='Windsor')
    province=models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)
    
    def __str__(self):
        return self.username
    
class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    client = models.ForeignKey(Client,on_delete=models.PROTECT)
    num_units = models.PositiveIntegerField()
    ORDER_CHOICES = [(0,'Order Cancelled'),(1,'Order Placed'),(2,'Order Shipped'),(3,'Order Delivered')]
    order_status = models.IntegerField(choices=ORDER_CHOICES, default=1)
    status_date = models.DateField(default=date.today)
    
    def __str__(self):
        return "For "+str(self.num_units)+" "+str(self.product)+"(s) by "+str(self.client)
    
    def total_cost(self):
        return self.num_units*self.product.price