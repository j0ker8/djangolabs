from django.urls import path
from labassignment4 import views

app_name = 'labassignment4'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'<int:cat_no>/', views.detail, name='detail'),
    ]
    
    