from django.contrib import admin

# Register your models here.
from .models import (
    Category, Product, Client, Order, OrderDetail
)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(OrderDetail)