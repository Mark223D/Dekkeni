from django.shortcuts import render
from django.http import JsonResponse

from products.models import Product, Category
from accounts.models import User
from carts.models import Cart, CartItem
from carts.views import create_cart_item, remove_cart_item, update_quantity
from .serializers import ProductSerializer, UserSerializer, CartItemSerializer, CartSerializer

from rest_framework import generics, permissions
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from allauth.account.views import ConfirmEmailView

from django.core import serializers


for user in User.objects.all():
    Token.objects.get_or_create(user=user)




# Create your views here.
def api_home(request):
	return JsonResponse({"Hello": "World!"})





class ProductsList(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	pagination_class = PageNumberPagination
	
	def get(self, request):
		if "id" in request.data:
			product_id = request.data["id"]
			return Response(self.send_item(item=product_id))
		elif "category_id" in request.data:
			category_id = request.data["category_id"] 
			return Response(self.send_category(category=category_id))
		else:
			return Response(self.send_queryset())

	def send_queryset(self):
		products = self.get_queryset()
		serializer = ProductSerializer(products, many=True)
		return serializer.data

	def send_category(self, category):
		category_items = Product.objects.get_by_category(category_id=category)
		serializer = ProductSerializer(category_items, many=True)
		return serializer.data
	
	def send_item(self, item):
		product = Product.objects.get(pk=item)
		serializer = ProductSerializer(product, many=False)
		return serializer.data


class UserList(ListAPIView):
	serializer_class = UserSerializer

	def get(self, request):
		if "email" in request.data:
			user_email = request.data["email"]
			user = User.objects.filter(email=user_email).first()
			serializer = UserSerializer(user, many=False)
			return Response(serializer.data)
		else:
			users = User.objects.all()
			serializer = UserSerializer(users, many=True)
			return Response(serializer.data)


class LoginView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        content = {'status': 'success'}
        return Response(content)

class RegisterView(generics.CreateAPIView):
	permissions_classes = (AllowAny,)

	def post(self, request, *args, **kwargs):
		if "email" in request.data and "password" in request.data:
			email = request.data["email"]
			password = request.data["password"]
			user = User.objects.create_user(email=email, password=password)
			token, created = Token.objects.get_or_create(user=user)
			return Response({'token': token.key })


		

class VerifyEmailView(APIView, ConfirmEmailView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)



class CartView(generics.CreateAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = ProductSerializer

	def post(self, request, *args, **kwargs):
		if "cart" in request.data and "quantity" in request.data:
			cart_raw = request.data["cart"]
			quantity = request.data["quantity"]
			cart = Cart.objects.new()
			for item in cart_raw:
				product_id = item["product_id"]
				product = Product.objects.get(pk=product_id)
				cart_item, added = create_cart_item(product_obj=product, cart_obj=cart)
				update_quantity(cart_item_obj=cart_item, quantity=cart.quantity)

			serializer = CartSerializer(cart, many=False)
			return Response({'cart': serializer.data,})
		else:
			return Response({'status': ' failed'})
