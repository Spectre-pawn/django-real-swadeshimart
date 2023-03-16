from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.sellers_register,name='sellers_register'),
    path('registration',views.sellers_registration,name="sellers_registration"),
    path('login_seller',views.sellers_login,name="sellers_login"),
    path('logout_seller',views.logout_seller,name='logout_seller'),
    path('dashboard',views.sellers_dashboard,name='dashboard'),
    path('orders', views.orderview, name='orders_views'),
    path('allproduct',views.allproduct,name='allproduct'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('addvariation',views.addvariation,name='addvariation'),
    path('delete_product',views.delete_product,name='deleteproduct'),
    path('edit_product',views.edit_product,name='editproduct'),
    path('account_settings', views.account_settings, name="account_settings"),
    path('manageorder', views.manageorder, name="manageorder"),
]
