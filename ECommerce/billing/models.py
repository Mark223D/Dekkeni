from accounts.models import GuestEmail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_save
from datetime import datetime
from django.urls import reverse

User = get_user_model()


class BillingProfileManager(models.Manager):
      def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('new_guest_email_id')
        created = False
        obj = None
        if user.is_authenticated:
            'logged in user checkout; remember payment stuff'
            obj, created = self.model.objects.get_or_create(
                            user=user, email=user.email)
        elif guest_email_id is not None:
            'guest user checkout; auto reloads payment stuff'
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                                            email=guest_email_obj.email)
        else:
            pass
        return obj, created




class BillingProfile(models.Model):
    user        = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True, blank=True)

    objects = BillingProfileManager()

    def __str__(self):
        return str(self.email)

    def __unicode__(self):
        return self.email

    def charge(self, order_obj, card=None):
        return Charge.objects.do(self, order_obj, card)
    

    def get_payment_method_url(self):
        return reverse('billing-payment-method')

    def get_cards(self):
        return self.card_set.all()
    @property
    def has_card(self):
        card_qs = self.get_cards()
        return card_qs.exists()

    @property
    def default_card(self):
        default_cards = self.get_cards().filter(active=True, default=True)
        if default_cards.exists():
            return default_cards.first()
        return None

    def set_cards_inactive(self):
        card_qs = self.get_cards()
        card_qs.update(active=False)
        return card_qs.filter(active=True).count()

    



def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if instance.customer_id and instance.email:
        print(" API REQUEST: Send To Payment Method Handler")
        #Generate Customer ID
        instance.customer_id = instance.email+"-"+timestamp

pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)



def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender= User)


class CardManager(models.Manager):
    def all(self, *args, **kwargs):
        return self.get_queryset().filter(active=True)



    def add_new(self, billing_profile, card_info):
        if card_info:
            print(card_info)
            new_card=self.model(
                billing_profile=billing_profile,
                card_id = card_info['card_id'],
                card_holder_name = card_info['cardHolder'],
                brand = card_info['brand'],
                country = card_info['country'],
                exp_month = card_info['expMonth'],
                exp_year = card_info['expYear'],
                last4 = card_info['last4'],
                )
            new_card.save()
            return new_card
        return None


class Card(models.Model):
    card_id = models.CharField(max_length=120, null=True, blank=True)
    card_holder_name = models.CharField(max_length=200, default='')
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.DO_NOTHING)
    brand = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    last4 = models.CharField(max_length=30, null=True, blank=True)
    default      = models.BooleanField(default=True)
    active      = models.BooleanField(default=True)
    timestamp      = models.DateTimeField(auto_now_add=True)


    objects = CardManager()

    def __str__(self):
        return "{} {}".format(self.brand, self.last4)


def new_card_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.default:
        billing_profile = instance.billing_profile
        qs = Card.objects.filter(billing_profile=billing_profile).exclude(pk=instance.pk)

        qs.update(default=False)

post_save.connect(new_card_post_save_receiver, sender=Card)



class ChargeManager(models.Manager):
    def do(self, billing_profile, order_obj, card=None):
        card_obj = card
        if card_obj is None:
            cards = billing_profile.card_set.filter(default=True)
            if cards.exists():
                card_obj = cards.first()
        if card_obj is None:
            return False, "No Cards available"
        customer_id = billing_profile.email+"-"+str(datetime.now())
        print(customer_id)
        c = ({
            "amount":int(order_obj.total *100),
            "currency": "USD",
            "customer" : customer_id,
            "source": card_obj.card_id,
            "description":"Charge for -@-.com",
            "paid":True,
            "refunded":False,
            "outcome": "outcome",
            "outcome_type": "outcome_type1",
            "seller_message": "seller_message1",
            "risk_level": "risk_level",
            "metadata":{"order_id": order_obj.order_id},
            })

        new_charge_obj = self.model(
            billing_profile=billing_profile,
            customer_id=customer_id,
            paid=c['paid'],
            refunded=c['refunded'],
            outcome=c['outcome'],
            outcome_type=c['outcome_type'],
            seller_message=c['seller_message'],
            risk_level=c['risk_level'],
        )
        new_charge_obj.save()
        return new_charge_obj.paid, new_charge_obj.seller_message 


class Charge(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.DO_NOTHING)
    customer_id = models.CharField(max_length=120)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    outcome = models.TextField(null=True, blank=True)
    outcome_type = models.CharField(max_length=120, null=True, blank=True)
    seller_message = models.CharField(max_length=120, null=True, blank=True)
    risk_level = models.CharField(max_length=120, null=True, blank=True)

    objects = ChargeManager()



