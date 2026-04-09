from django import forms
from django.forms import ModelForm


class RetrieveInfoForm(forms.Form):
    surname = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'e.g. Smith'
        })
    )
    
    dob_day = forms.CharField(
        max_length=2,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'date-input',
            'placeholder': 'DD',
            'maxlength': '2'
        })
    )
    
    dob_month = forms.CharField(
        max_length=2,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'date-input',
            'placeholder': 'MM',
            'maxlength': '2'
        })
    )
    
    dob_year = forms.CharField(
        max_length=4,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'date-input',
            'placeholder': 'YYYY',
            'maxlength': '4'
        })
    )
    
    postcode = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'e.g. AB1 2CD'
        })
    )


class EmailForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'type': 'email',
            'id': 'email',
            'name': 'email',
            'placeholder': 'Email',
            'class': 'email-input'
        })
    )


class VerificationCodeForm(forms.Form):
    verification_code = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'verificationCode',
            'placeholder': '',
            'class': 'verification-input'
        })
    )


class OTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'otp',
            'name': 'otp',
            'placeholder': '',
            'maxlength': '6',
            'inputmode': 'numeric',
            'class': 'otp-input'
        })
    )