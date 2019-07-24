from django.db import models
from django.conf import settings
from products.models import Product
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save, m2m_changed
from decimal import Decimal

User = get_user_model()

class CartManager(models.Manager):

    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count()==1 :
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj
    
    
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class CartItemManager(models.Manager):

    def new_or_get(self, item):
        qs = self.get_queryset().filter(item=item)
        if qs.count()==1 :
            new_obj = False
            cart_item = qs.first()
        else:
            cart_item = CartItem.objects.new(item=item)
            new_obj = True
        return cart_item, new_obj
    
    
    def new(self, item):
        return self.model.objects.create(item=item)


        


class CartItem(models.Model):
    item = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    objects = CartItemManager()

    @property
    def name(self):
        return self.item.name
    
    @property
    def price(self):
        return self.item.price 

    def get_absolute_url(self):
        return self.item.get_absolute_url()

    

    



class Cart(models.Model):
    user        = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    products    = models.ManyToManyField(CartItem, blank=True)
    subtotal    = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    total       = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    timestamp   = models.DateField(auto_now_add=True)
    updated     = models.DateField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    def cart_item_count(self):
        count = 0
        for item in self.products.all():
            count += item.quantity
        return count        

    def get_subtotal(self):
        cart_items = CartItem.objects.all()
        subtotal = 0
        for cart_item in cart_items:
            subtotal += cart_item.item.price * cart_item.quantity
        self.subtotal = subtotal
        return self.subtotal
    
    def get_total(self):
        subtotal = self.subtotal
        total = 0

        if self.subtotal > 0:
            total = Decimal(self.subtotal) * Decimal(1.08)
        else:
            total = 0.00

        self.total = total
        return total

def m2m_cart_receiver(sender, instance, action, *args, **kwargs):
    if action  == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for cart_item in products:
            price = cart_item.item.price
            total = price * cart_item.quantity

        if instance.subtotal != total:
                instance.subtotal = total
                instance.save()
       

m2m_changed.connect(m2m_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = Decimal(instance.subtotal) * Decimal(1.08)
    else:
        instance.total = 0.00

pre_save.connect(pre_save_cart_receiver, sender=Cart)