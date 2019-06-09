from django import forms
from django.contrib.auth import get_user_model

class ContactForm(forms.Form):
    fullName    = forms.CharField(
                widget=forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "placeholder" : "Your Full Name",
                        }
                        )
                )

    email       = forms.EmailField(
                widget=forms.EmailInput(
                    attrs={
                    "class" : "form-control",
                    "placeholder" : "Your Email",
                    }
                    )
                )

    content     = forms.CharField(
                widget=forms.Textarea(
                    attrs={
                        "class" : "form-control",
                        "placeholder" : "Your Message",
                    }
                    )
                )

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if not "gmail.com" in email:
    #         raise forms.ValidationError("Email has to be gmail")
    #     return email

    # def clean_content(self):
    #     raise forms.ValidationError("Content is wrong.")