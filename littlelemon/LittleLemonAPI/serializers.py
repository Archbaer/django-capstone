from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Cart, Category, Order, OrderItem, MenuItem
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta: 
        model = MenuItem
        fields = ["title", "price", "featured", "category"]

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"