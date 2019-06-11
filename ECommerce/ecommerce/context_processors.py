from products.models import Category, Subcategory, Subsubcategory

def sections_processor(request):
	categories = Category.objects.all()
	subcategories = Subcategory.objects.all()
	subsubcategories = Subsubcategory.objects.all()
	return {'categories': categories, 'subcategories': subcategories, 'subsubcategories': subsubcategories}