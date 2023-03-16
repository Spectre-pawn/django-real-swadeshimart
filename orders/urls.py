from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('my_orders',views.my_orders,name="my_orders"),
    path('order_details',views.order_details,name='order_details'),
    path('cancle_order',views.cancle_order,name='cancle_order'),
 

]   
