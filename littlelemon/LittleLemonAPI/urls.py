from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', include("djoser.urls")),
    path('menu-items', views.MenuItemView, name='menu-items'),
    path('menu-items/<int:pk>', views.SingleMenuItemView, name='single-menu-item'),

    path('groups/manager/users', views.ManagerView, name="managers"),
    path('groups/manager/users/<str:username>', views.DeleteManagerView, name="delete-manager"),
    
    path('groups/delivery-crew/users', views.DeliveryCrewView, name="delivery-crews"),
    path('groups/delivery-crew/users/<str:username>', views.DeleteDeliveryCrewView, name="delete-delivery-crew"),

    path('cart/menu-items', views.CartView, name="cartview"),

    path("orders", views.OrderView, name="orders"),
    path("orders/<int:pk>", views.SingleOrderView, name="single-order"),
]