from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cart, CartItem
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address
import copy


def cart_detail_api_view(request):
    cart_obj,  new_obj = Cart.objects.new_or_get(request)

    cart_data  = {}
    products = [{}]
    for x in cart_obj.products.all():
        products = [
        {
        "id": x.id,
        "url":x.get_absolute_url(),
        "name": x.name,
        "price": x.price,
        }]
    cart_data = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}

    return JsonResponse(cart_data)

def cart_home(request):
    cart_obj,  new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart":cart_obj})


def cart_update(request):
    #Get ProductID from request
    product_id = request.POST.get('product_id') 

    #Set quantity to 0 -- Initialization
    quantity = 0
    remove = 0

    # if the quantity is given save it in a variable
    if request.POST.get('quantity') is not None:
        quantity = int(request.POST.get('quantity'))

    if request.POST.get('remove') is not None:
        remove = int(request.POST.get('remove'))

    # Initializing added variable
    added = False

    #If product_id is given
    if product_id is not None:
        
        #Try getting the product
        try: 
            product_obj = Product.objects.get(id=product_id)
        #if product does not exist
        except Product.DoesNotExist:
            print("Show message to user: Product is gone?")
            return redirect("carts:home")
        
        #if product does exist get user cart or create a new cart
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        #if cartItem containing product is found
        cart_item_coll = cart_obj.products.filter(item=product_obj)

        if cart_item_coll.count() > 0:
            #Get cartItem
            cart_item_obj = cart_item_coll.first()
            print("Cart Item In Cart: Updating Quantity")         

            #if quantity is 0 or remove pressed
            if quantity == 0 or remove > 0:
                print("removing from cat")
                added = remove_cart_item(cart_obj=cart_obj, cart_item_obj=cart_item_obj)
            # if quanity of the product is more than 0
            elif quantity > 0 :
                added = update_quantity(cart_item_obj=cart_item_obj, quantity=quantity)

            # product_obj.in_cart = added
            # product_obj.save()
        #if cartItem containing product is not found
        elif cart_item_coll.count() <= 0 and quantity == 1:
            cart_item , added = create_cart_item(product_obj=product_obj, cart_obj=cart_obj)
        
        #counter of the cart is on sum of cartItem quantities
        count = cart_obj.cart_item_count()
        request.session['cart_items'] = count
        # product_obj.in_cart = added
        # product_obj.save()
        cart_obj.save()

        if request.is_ajax():
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": count,
            }
            return JsonResponse(json_data, status=200)

    return redirect("carts:home")

def update_quantity(cart_item_obj, quantity):
    #update quantity
    try:
        cart_item_obj.quantity = quantity
        cart_item_obj.save()
        print("Quantity Update Success")
    except:
        print("Quantity Update failed")
        cart_item_obj.quantity = quantity
        cart_item_obj.save()
        print("Force Quantity Update")

    #product is added to cart
    added = True
    return added


def remove_cart_item(cart_obj, cart_item_obj):
    #remove cartItem from cart
    try: 
        print("Removing & Deleting Cart Item from Cart")
        cart_obj.products.remove(cart_item_obj)
        cart_item_obj.delete()
    except:
        print("Error Removing & Deleting Cart Item from Cart")
        cart_obj.products.remove(cart_item_obj)
        cart_item_obj.delete()
        print("Force Removing & Deleting Cart Item from Cart")
    
    #product is therefore removed from cart
    added = False

    return added


def create_cart_item(product_obj, cart_obj):
    #create cartItem containing product 
    try:
        print("Adding Item to Cart")
        cart_item, new_obj = CartItem.objects.new_or_get(item=product_obj)
        cart_obj.products.add(cart_item)
    except:
        print("Error Adding Item to Cart")
        cart_item, new_obj = CartItem.objects.new_or_get(item=product_obj)
        cart_obj.products.add(cart_item)
        print("Force Added Item to Cart")

    #product is added to cart            
    added = True
    return cart_item, added


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("carts:home")

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    
    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    has_card = False
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile=billing_profile, cart_obj=cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()
        has_card=billing_profile.has_card

    if request.method == "POST":
        "Check Order"
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, charge_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                request.session["cart_items"] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_cards_inactive()
                return redirect("cart:success")
            else:
                return redirect("cart:checkout")


    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
        "has_card": has_card
    }
    print(context)
    return render(request, "carts/checkout.html", context)


def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})
