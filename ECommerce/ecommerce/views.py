from django.contrib.auth import authenticate, login, get_user_model
from django.http import  HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import ContactForm
from products.models import Product



def home_page(request):
    context = {
        "title": "eCommerce",
        "content": "Welcome to eCommerce",
    }
    if request.user.is_authenticated:
        context["premiumContent"] = "Welcome !"

    products = Product.objects.all()
    context['object_list'] = products
    return render(request, "home_page.html", context)

def about_page(request):
    context = {
        "title" : "About Page",
        "content" : "Welcome to About Page"

    }
    return render(request, "home_page.html",context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title"   : "Contact Page",
        "content" : "Welcome to Contact Page.",
        "form"    : contact_form,
    }
    
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({"message": "Thank you for your submission."})
    if contact_form.errors:
        print(contact_form.cleaned_data)
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')
    
    return render(request, "contact/view.html", context)
