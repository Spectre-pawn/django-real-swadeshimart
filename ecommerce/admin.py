from django.contrib import admin

from ecommerce.models import CartItem, CustomerDetails,Cart


# Register your models here.
admin.site.register(CustomerDetails)
admin.site.register(Cart)
admin.site.register(CartItem)
