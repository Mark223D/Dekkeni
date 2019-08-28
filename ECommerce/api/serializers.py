from django.contrib.auth.models import User, Group
from rest_framework import serializers
from products.models import Product
from accounts.models import User
from carts.models import CartItem, Cart
# from rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from rest_auth.serializers import UserDetailsSerializer


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ('title','slug','description','price','image','featured','hot_deals',
			'new_arrivals','active','timestamp','category',)
       


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('email','full_name')

class UserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        fields = ('email', 'full_name',)
        read_only_fields = ('',)

class CartItemSerializer(serializers.ModelSerializer):
	item = ProductSerializer()
	class Meta:
		model = CartItem
		fields = ('item',)

class CartSerializer(serializers.ModelSerializer):
	products = CartItemSerializer(many=True)

	class Meta:
		model = Cart
		fields = ('products',) 
		

# class RegisterSerializer(RegisterSerializer):
#     first_name = serializers.CharField(required=True, write_only=True)
#     last_name = serializers.CharField(required=True, write_only=True)

#     def get_cleaned_data(self):
#         return {
#             'first_name': self.validated_data.get('first_name', ''),
#             'last_name': self.validated_data.get('last_name', ''),
#             'password1': self.validated_data.get('password', ''),
#             'email': self.validated_data.get('email', ''),
#         }

#     def save(self, request):
#         # adapter = get_adapter()
#         # user = adapter.new_user(request)
#         # self.cleaned_data = self.get_cleaned_data()
#         # adapter.save_user(request, user, self)
#         # # setup_user_email(request, user, [])
#         # user.save()
#         print(request)
#         # return user