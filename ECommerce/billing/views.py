from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url
from .models import BillingProfile, Card


def payment_method_view(request):
	
	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

	if not billing_profile:
		return redirect("/cart")

	next_url = None
	next_ = request.GET.get("next")
  
	if is_safe_url(next_, request.get_host()):
		next_url = next_
	return render(request, 'billing/payment-method.html', { "next_url": next_url })


def payment_method_createview(request):
	if request.method == "POST" and request.is_ajax():

		print(request.POST)
		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

		if not billing_profile:
			return HttpResponse({"message": "Cannot find user."}, status_code=401)
		customer = billing_profile.customer_id
		#Get Card Info
		card_info = ({
			"card_id": customer,
			"cardHolder": request.POST.get("cardHolder"),
			"brand": request.POST.get("brand"),
			"country": request.POST.get("country"),
			"expMonth": request.POST.get("expM"), 
			"expYear": request.POST.get("expY"),
			"last4": request.POST.get("last4")
			})
		#Create Card Object 
		new_card=Card.objects.add_new(billing_profile, card_info)
		return JsonResponse({"message":"Success! You card was added!"})
	raise HttpResponse("error", status_code=401)