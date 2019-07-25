from products.models import Category
from carts.models import Cart
categories = Category.objects.all()


def sections_processor(request):
	cart, new = Cart.objects.new_or_get(request)
	return {'categories': categories,'cart': cart}