from . import views
from django.urls import include, path

urlpatterns = [
    path('',views.index,name="index" ),
    path('store', views.store, name='store'),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("cart/", views.cart, name="cart"),
    path("login_register",views.login_register,name="login_register"),#page
    path("cust_registration",views.cust_registration,name="Cust_registration"),
    path("login_customer",views.customer_login_attempt,name="customer_login"),
    path("logout_cust",views.logout_cust,name="logout_cust"),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.productView, name='productView'),
    path('search/', views.search, name='search'),
    path('checkout/', views.checkout, name='checkout'),
    path('account_settings', views.account_settings, name="custaccount_settings"),
]