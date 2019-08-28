import random
from django.db import models
import os
from ecommerce.utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.urls import reverse
from django.db.models import Q

def get_file_name_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 123456789)
    name, ext = get_file_name_ext(filename)
    final_filename = f'{new_filename}{ext}'#.format(new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
            new_filename=new_filename, 
            final_filename=final_filename
            )


class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)


    def featured(self):
        return self.filter(featured=True)

    def hot_deals(self):
        return self.filter(hot_deals=True)

    def new_arrivals(self):
        return self.filter(new_arrivals=True)

    def search(self, query):
        
        lookups= (Q(title__contains=query) | 
                  Q(description__icontains=query) |
                  Q(price__icontains=query) |
                  Q(tag__title__icontains=query))

        return self.filter(lookups).distinct()

class CategoryQuerySet(models.QuerySet):
    def active(self):
        return self

    def search(self, query):
        lookups = (Q(name__contains=query) )
        return self.filter(lookups).distinct()



class ProductManager(models.Manager):

    def all(self):
        return self.get_queryset().active() 

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get_by_category(self, category_id):
        category = Category.objects.get_by_id(id=category_id)
        qs = self.get_queryset().filter(category=category)
        return qs

    def search(self, query):
        return self.get_queryset().active().search(query)

class CategoryManager(models.Manager):

    def all(self):
        return self.get_queryset() 
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    

    def search(self, query):
        return self.get_queryset().search(query)

class Category(models.Model):
        name = models.CharField(max_length=200, default='')
        slug = models.SlugField(default='category-name')
        parent = models.ForeignKey('self', blank=True, null=True, related_name='child', on_delete=models.CASCADE)
        description = models.TextField(blank=True,help_text="Optional")
        
        objects = CategoryManager()

        class Admin:
                list_display = ('name', '_parents_repr')
                search_fields = ('Category__parent_name', 'Category__parent_slug')
        
        def __str__(self):
                p_list = self._recurse_for_parents(self)
                p_list.append(self.name)
                return self.get_separator().join(p_list)

        def __unicode__(self):
            return self.title

        @property
        def title(self):
            return self.name

        def get_absolute_url(self):
                if self.parent_id:
                        return reverse("products:subcategories", kwargs={"parent_slug": self.parent.slug, "slug":self.slug})
                else:
                        return reverse("products:categories", kwargs={"slug":self.slug})
        
        def _recurse_for_parents(self, cat_obj):
                p_list = []
                if cat_obj.parent_id:
                        p = cat_obj.parent
                        p_list.append(p.name)
                        more = self._recurse_for_parents(p)
                        p_list.extend(more)
                if cat_obj == self and p_list:
                        p_list.reverse()
                return p_list
                
        def get_separator(self):
                return ' - '
        
        def _parents_repr(self):
                p_list = self._recurse_for_parents(self)
                return self.get_separator().join(p_list)

        _parents_repr.short_description = "Tag parents"
        
        def save(self):
                p_list = self._recurse_for_parents(self)
                if self.name in p_list:
                        raise validators.ValidationError("You must not save a category in itself!")
                super(Category, self).save()




class Product(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True, unique=True)
    description = models.TextField(verbose_name='Product Details')
    price       = models.DecimalField(decimal_places=2, max_digits=10, default=39.99)
    image       = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured    = models.BooleanField(default=False)
    hot_deals    = models.BooleanField(default=False)
    new_arrivals    = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True)   
    in_cart         = models.BooleanField(default=False)

    objects = ProductManager()

    def get_absolute_url(self):
        if not self.category.parent.parent:
            return reverse("products:detail-no-subsub", kwargs={"category": self.category.parent.slug,"subcategory": self.category.slug, "slug":self.slug})
        else:            
            return reverse("products:detail", kwargs={"category": self.category.parent.slug,"subcategory": self.catgeory.parent.slug,"subsubcategory": self.category.parent.parent.slug, "slug":self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title
        
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)

def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(category_pre_save_receiver, sender=Category)