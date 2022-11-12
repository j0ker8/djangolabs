from django.urls import path
from labassignment4 import views

app_name = 'labassignment4'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'<int:cat_no>/', views.detail, name='detail'),
    path(r'products/',views.products,name='products'),
    path(r'placeorder/',views.place_order,name='placeorder'),
    path(r'products/<int:prod_id>/', views.productdetail, name='productdetail'),
    path(r'login/', views.user_login, name='login'),
    path(r'logout/', views.user_logout, name='logout')
    ]
    
    