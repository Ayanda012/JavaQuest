# path -> listings/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm as AuthForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class AuthenticationForm(AuthForm):
    username = forms.CharField(max_length=254, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)   

class DonationForm(forms.Form):
    amount = forms.DecimalField(label='Donation Amount', max_digits=10, decimal_places=2)
    payment_method = forms.ChoiceField(
        label='Payment Method',
        choices=[
            ('paystack', 'Paystack'),
            ('paypal', 'PayPal'),
            ('bank_transfer', 'Bank Transfer'),
        ],
        widget=forms.RadioSelect
    )

