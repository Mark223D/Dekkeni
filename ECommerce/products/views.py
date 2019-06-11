from django.shortcuts import render, get_object_or_404
# from django.views import render
from django.http import Http404
from .models import Product
from django.views.generic.list import ListView
from django.views.generic.detail import  DetailView
from carts.models import Cart

# from analytics.mixins import ObjectViewedMixin

class ProductFeaturedListView(ListView):
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()

class ProductNewArrivalsListView(ListView):
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().new_arrivals()

class ProductHotDealsListView(ListView):
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().hot_deals()
# class ProductFeaturedDetailView(ObjectViewedMixin,DetailView):

class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.all().featured()
    template_name = "products/featured-detail.html"

# class ProductNewArrivalsDetailView(ObjectViewedMixin,DetailView):

class ProductNewArrivalsDetailView(DetailView):
    queryset = Product.objects.all().featured()
    template_name = "products/featured-detail.html"

# class ProductHotDealsDetailView(ObjectViewedMixin,DetailView):

class ProductHotDealsDetailView(DetailView):
    queryset = Product.objects.all().featured()
    template_name = "products/featured-detail.html"



def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)



'''
 -------------- CATEGORIES VIEWS------------
 
'''
class CategorytListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/category-list.html"


    def get_context_data(self, *args, **kwargs):
        context = super(CategorytListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        path_elem = self.request.path.split('/')
        try:
            cat = path_elem[2]
            context['category'] = cat
        except IndexError:
            print("No Category")

        try:
            sub = path_elem[3]
            context['subcategory'] = sub
        except IndexError:
            print("No SubCategory")
        
        try:
            subsub = path_elem[4]
            context['subsubcategory'] = subsub
        except IndexError:
            print("No Subsubcategory")

        try:
            product = path_elem[5]
            context['product'] = product
        except IndexError:
            print("No Product")

        return context


    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()

'''
 -------------- PRODUCTS VIEWS------------
 
'''

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context


    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()

''' FOR ANALYTICS'''
# class ProductDetailSlugView(ObjectViewedMixin, DetailView):

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context


    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get("slug")

        instance = get_object_or_404(Product, slug=slug, active=True)
        try: 
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not Found...")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except: 
            raise Http404("Uhhmmm....")                

        # object_view_signal.send(instance.__class__, instance=instance, request=request)
        return instance





'''
 -------------- TEMP VIEWS------------

'''


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context
    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get("pk")

        instance = Product.objects.get_by_id(pk)
        if instance is None :
            instance = qs.first()
        else:
            raise Http404("Product Doesn't Exist")
        return instance

def product_detail_view(request, pk=None, *args, **kwargs):

    instance = Product.objects.get_by_id(pk)
    if instance is None :
        instance = qs.first()
    else:
        raise Http404("Product Doesn't Exist")



    context = {
        'object_list': instance
    }
    return render(request, "products/detail.html", context)


