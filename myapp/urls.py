from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('about/', views.author, name='author'),
    path('store/', views.shop, name='shop'),
]