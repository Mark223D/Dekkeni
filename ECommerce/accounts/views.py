from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user_model
from django.http import  HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, GuestForm
from django.utils.http import is_safe_url
from .models import GuestEmail
from django.views.generic import CreateView, FormView
from .signals import user_logged_in

def guest_register_view(request):
    form =  GuestForm(request.POST or None)

    context = {
        "form" : form 
    }     
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None

    if form.is_valid():
        email= form.cleaned_data['email']
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['new_guest_email_id'] = new_guest_email.id

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            redirect('/register/')

    return redirect('/register/')


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = '/'
    
    def form_valid(self, form):
        request=self.request
        if request.GET.get("next"):
            next_ = request.GET.get("next")
        else: 
            next_ = "/"

        if request.POST.get("next"):
            next_post = request.POST.get("next")
        else: 
            next_post = "/"

        redirect_path = next_ or next_post or None

        email= form.cleaned_data['email']
        password= form.cleaned_data['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            try:
                del request.session['guest_email_id']
            except:
                pass
            print(redirect_path)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                redirect('/')
        return super(LoginView, self).form_invalid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'

# User = get_user_model()

# def register_page(request):
#     form =  RegisterForm(request.POST or None)
#     context = {
#         "form" : form 
#     }  

#     if form.is_valid():
#         form.save()

#     return render(request, "accounts/register.html", context)