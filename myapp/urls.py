from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('about/', views.author, name='author'),
    path('store/', views.shop, name='shop'),
    path('catalog/',views.product_list,name = 'catalog'),
    path('catalog/<int:pk>/',views.item,name = 'item'),
    path('cart/add/<int:item_id>/',views.cart_add,name = 'cart_add'),
    path('cart/update/<int:item_id>/',views.cart_update,name = 'cart_update'),
    path('cart/remove/<int:item_id>/',views.cart_remove,name = 'cart_remove'),
    path('cart/', views.cart_view, name='cart_view'),
]