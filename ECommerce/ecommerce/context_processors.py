from products.models import Category
categories = Category.objects.all()

def sections_processor(request):
	return {'categories': categories,}