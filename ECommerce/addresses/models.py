from django.db import models
from billing.models import BillingProfile

ADDRESS_TYPES=(
    ('billing', 'Billing'), 
    ('shipping', 'Shipping'),
)

class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True)
    address_type    = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line_1  = models.CharField(max_length=120)
    address_line_2  = models.CharField(max_length=120, null=True, blank=True)
    city            = models.CharField(max_length=120)
    state           = models.CharField(max_length=120)
    postal_code     = models.CharField(max_length=120)
    country         = models.CharField(max_length=120, default="Lebanon")
    def __str__(self):
        return self.billing_profile.email
    
    def __unicode__(self):
        return self.billing_profile.email

    def get_address(self):
        return "{line1}\n{line2}\n{city}\n{state}, {postal_code} {country}".format(
            line1=self.address_line_1,
            line2=self.address_line_2 or "",
            city=self.city,
            state=self.state,
            postal_code=self.postal_code,
            country=self.country
        )