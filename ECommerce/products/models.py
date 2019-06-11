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
    # print(instance)
    # print(filename)
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
        return self.filter(active=True)

    def search(self, query):
        
        lookups= (Q(title__contains=query) )

        return self.filter(lookups).distinct()

class SubcategoryQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def search(self, query):
        
        lookups= (Q(title__contains=query))

        return self.filter(lookups).distinct()

class SubsubQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def search(self, query):
        
        lookups= (Q(title__contains=query))

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
    def search(self, query):
        return self.get_queryset().active().search(query)

class CategoryManager(models.Manager):

    def all(self):
        return self.get_queryset().active() 
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None
    def search(self, query):
        return self.get_queryset().active().search(query)

class SubcategoryManager(models.Manager):

    def all(self):
        return self.get_queryset().active() 
    def get_queryset(self):
        return SubcategoryQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None
    def search(self, query):
        return self.get_queryset().active().search(query)

class SubsubcategoryManager(models.Manager):

    def all(self):
        return self.get_queryset().active() 
    def get_queryset(self):
        return SubsubcategoryQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None
    def search(self, query):
        return self.get_queryset().active().search(query)


class Category(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True, unique=True)


    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title
    def get_absolute_url(self):
        return reverse("products:categories", kwargs={"slug":self.slug})


class Subcategory(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True, unique=True)
    category    = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True)   

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title
    def get_absolute_url(self):
        return reverse("products:subcategories",  kwargs={"category": self.category.slug, "slug":self.slug})

class Subsubcategory(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True, unique=True)
    subcategory    = models.ForeignKey(Subcategory, on_delete=models.DO_NOTHING, null=True)   

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title

    def get_absolute_url(self):
        return reverse("products:subsubcategories",  kwargs={"category": self.subcategory.category.slug,"subcategory": self.subcategory.slug, "slug":self.slug})

class Product(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price       = models.DecimalField(decimal_places=2, max_digits=10, default=39.99)
    image       = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured    = models.BooleanField(default=False)
    hot_deals    = models.BooleanField(default=False)
    new_arrivals    = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True)   
    subcategory = models.ForeignKey(Subcategory, on_delete=models.DO_NOTHING, null=True, blank=True) 
    subsubcategory = models.ForeignKey(Subsubcategory, on_delete=models.DO_NOTHING, null=True, blank=True)   
  
    

    objects = ProductManager()

    def get_absolute_url(self):
        print(self.category)
        if not self.subsubcategory:
            return reverse("products:detail-no-subsub", kwargs={"category": self.category.slug,"subcategory": self.subcategory.slug, "slug":self.slug})
        else:            
            return reverse("products:detail", kwargs={"category": self.category.slug,"subcategory": self.subcategory.slug,"subsubcategory": self.subsubcategory.slug, "slug":self.slug})

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

def subcategory_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(subcategory_pre_save_receiver, sender=Subcategory)

def subsubcategory_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(subsubcategory_pre_save_receiver, sender=Subsubcategory)