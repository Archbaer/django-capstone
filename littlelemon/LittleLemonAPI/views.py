from django.shortcuts import get_object_or_404, render
from .models import Cart, Category, Order, OrderItem, MenuItem
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    CartSerializer,
    OrderSerializer,
    MenuItemSerializer,
    UserSerializer,
)

from rest_framework import status


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def MenuItemView(request):
    if request.method == "GET":
        queryset = MenuItem.objects.all()
        serialzed_data = MenuItemSerializer(queryset, many=True)
        return Response(serialzed_data.data, status=status.HTTP_200_OK)

    if request.user.groups.filter(name="Manager").exists():
        data = request.data
        serialzed_data = MenuItemSerializer(data=data)
        if serialzed_data.is_valid():
            serialzed_data.save()
            return Response(serialzed_data.data, status=status.HTTP_201_CREATED)
        return Response(serialzed_data.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {"message": "You dont have permission for the operation"},
        status=status.HTTP_403_FORBIDDEN,
    )


@api_view(["GET", "PATCH", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def SingleMenuItemView(request, pk):
    if request.method == "GET":
        try:
            menuitem = MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            return Response(
                {"error": "MenuItem not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serialzed_data = MenuItemSerializer(menuitem)
        return Response(serialzed_data.data, status=status.HTTP_200_OK)

    if request.user.groups.filter(name="Manager").exists():
        try:
            menuitem = MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            return Response(
                {"error": "MenuItem not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if request.method in ["PUT", "PATCH"]:
            data = request.data
            serialzed_data = MenuItemSerializer(
                menuitem, data=data, partial=(request.method == "PATCH")
            )
            if serialzed_data.is_valid():
                serialzed_data.save()
                return Response(serialzed_data.data, status=status.HTTP_200_OK)
            return Response(serialzed_data.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.method == "DELETE":
            menuitem.delete()
            return Response({"success": "Deleted"}, status=status.HTTP_200_OK)

    return Response(
        {"message": "You dont have permission for the operation"},
        status=status.HTTP_403_FORBIDDEN,
    )


from django.contrib.auth.models import User, Group


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def ManagerView(request):
    if request.user.groups.filter(name="Manager").exists():
        if request.method == "GET":
            managers = User.objects.filter(groups__name="Manager")
            serialzed_data = UserSerializer(managers, many=True)
            return Response(serialzed_data.data, status=status.HTTP_200_OK)

        username = request.data.get("username")
        if not username:
            return Response(
                {"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        managers.user_set.add(user)
        return Response({"Message": "OK Added"}, status=status.HTTP_201_CREATED)

    return Response(
        {"message": "You dont have permission for the operation"},
        status=status.HTTP_403_FORBIDDEN,
    )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def DeleteManagerView(request, username):
    if request.user.groups.filter(name="Manager").exists():
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        managers.user_set.remove(user)
        return Response({"Message": "OK Removed"}, status=status.HTTP_200_OK)

    return Response(
        {"message": "You dont have permission for the operation"},
        status=status.HTTP_403_FORBIDDEN,
    )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def DeliveryCrewView(request):
    if request.user.groups.filter(name="Manager").exists():
        if request.method == "GET":
            managers = User.objects.filter(groups__name="Delivery_Crew")
            serialzed_data = UserSerializer(managers, many=True)
            return Response(serialzed_data.data, status=status.HTTP_200_OK)
        username = request.data.get("username")
        if not username:
            return Response(
                {"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Delivery_Crew")
        managers.user_set.add(user)
        return Response({"Message": "OK Added"}, status=status.HTTP_201_CREATED)

    return Response(
        {"message": "You dont have permission for the operation"},
        status=status.HTTP_403_FORBIDDEN,
    )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def DeleteDeliveryCrewView(request, username):
    if request.user.groups.filter(name="Manager").exists():
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Delivery_Crew")
        managers.user_set.remove(user)
        return Response({"Message": "OK Removed"}, status=status.HTTP_200_OK)

    return Response(
        {"message": "You dont have permission for the operation"},
        status=status.HTTP_403_FORBIDDEN,
    )


@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated])
def CartView(request):
    if (
        request.user.groups.filter(name="Manager").exists()
        or request.user.groups.filter(name="Delivery_Crew").exists()
    ):
        return Response(
            {"Message": "Only customers may have cart"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "GET":
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
            serialized_cart = CartSerializer(cart)
            return Response(serialized_cart.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response(
                {"Message": "Cart does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
    if request.method == "POST":
        data = request.data
        serialized_cart = CartSerializer(data=data)
        if serialized_cart.is_valid():
            serialized_cart.save()
            return Response(
                {"message": "added to cart"}, status=status.HTTP_201_CREATED
            )

        return Response(serialized_cart.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        cart = Cart.objects.get(user=request.user)
        cart.delete()
        return Response({"Message": "Cart Deleted"}, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response(
            {"Message": "Cart does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def OrderView(request):
    if request.method == "GET":
        if request.user.groups.filter(name="Manager").exists():
            orders = Order.objects.all()
            serialized_orders = OrderSerializer(orders, many=True)
            return Response(serialized_orders.data, status=status.HTTP_200_OK)
        if request.user.groups.filter(name="Delivery_Crew").exists():
            orders = Order.objects.filter(delivery_crew=request.user)
            serialized_orders = OrderSerializer(orders, many=True)
            return Response(serialized_orders.data, status=status.HTTP_200_OK)

        orders = Order.objects.filter(user=request.user)
        serialized_orders = OrderSerializer(orders, many=True)
        return Response(serialized_orders.data, status=status.HTTP_200_OK)

    if (
        request.user.groups.filter(name="Manager").exists()
        or request.user.groups.filter(name="Delivery_Crew").exists()
    ):
        return Response(
            {"Message": "Only customers can POST orders"},
            status=status.HTTP_403_FORBIDDEN,
        )

    order_data = request.data
    serialized_data = OrderSerializer(data=order_data)
    if serialized_data.is_valid():
        serialized_data.save()
        return Response(serialized_data.data, status=status.HTTP_201_CREATED)

    return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def SingleOrderView(request, pk):
    if request.method == "GET":
        if (
            request.user.groups.filter(name="Manager").exists()
            or request.user.groups.filter(name="Delivery_Crew").exists()
        ):
            return Response(
                {"Message": "Only customers can POST orders"},
                status=status.HTTP_403_FORBIDDEN,
            )
        menu_item = OrderItem.objects.get(order=pk).menuitem
        serialized_menu_item = MenuItemSerializer(menu_item)
        return Response(serialized_menu_item.data, status=status.HTTP_200_OK)

    if request.user.groups.filter(name="Manager").exists():
        try:
            order = Order.objects.get(pk=pk)
            order.delete()
            return Response({"message ": "Order Deleted"}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(
                {"message ": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )
    return Response({"message ": "Not Permitted"}, status=status.HTTP_403_FORBIDDEN)
