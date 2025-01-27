from django.contrib import admin
from .models import Cart, Category, Order, OrderItem, MenuItem

admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(MenuItem)
