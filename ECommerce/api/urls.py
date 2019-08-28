from django.conf.urls import url
from django.urls import path, include, re_path

from .views import api_home, ProductsList, UserList, LoginView, RegisterView, CartView

urlpatterns= [
	url(r'^cart/$', CartView.as_view(), name="cart"),
	url(r'^all/$', ProductsList.as_view(), name="get_all_products"),
	url(r'^item/$', ProductsList.as_view(), name="get_product"),
	url(r'^category/$', ProductsList.as_view(), name="get_products_by_category"),

	url(r'^user/$', UserList.as_view(), name="get_user"),
	url(r'^user/login/$', LoginView.as_view(), name="user_login"),
	url(r'^user/registration/$', RegisterView.as_view(), name="user_registration"),


]