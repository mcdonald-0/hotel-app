from django.conf import settings

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import EmailMessage

from django.template.loader import render_to_string

from django.urls import reverse

from django.utils.encoding import force_bytes, force_text, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from six import text_type


class GuestTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return text_type(user.email) + text_type(user.is_email_verified) + text_type(user.pk) + text_type(timestamp)


token_generator = GuestTokenGenerator()


def send_activation_email(request, user, first_name, next_path):
    current_site = get_current_site(request).domain
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    link = reverse('authentication:authenticate_guest', kwargs={'uidb64': uidb64, 'token': token})

    if next_path is not '':
        next_path = f'http://{current_site}{link}?next={next_path}'
    else:
        next_path = f'http://{current_site}{link}'

    mail_subject = 'Activate your account and become our Guest'
    mail_body = render_to_string('authentication/activate_guest_account.html', {
        'user': user,
        'first_name': first_name,
        'domain': current_site,
        'uidb64': uidb64,
        'token': token,
        'link': link,
        'activate_url': next_path,
    })

    mail_from = 'activte_guest@hotelapp.com'

    if settings.DEBUG:
        mail_to = ['admin@example.com']
    else:
        mail_to = [user.email]

    mail = EmailMessage(mail_subject, mail_body, mail_from, mail_to)

    mail.send()
