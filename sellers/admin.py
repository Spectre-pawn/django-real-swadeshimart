from django.contrib import admin

from sellers.models import Choice, ReviewRating, Seller,Product, Variation
# Register your models here.
admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(Variation)
admin.site.register(ReviewRating)
admin.site.register(Choice)