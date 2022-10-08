from django.conf import settings

from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import EmailMessage

from django.http import HttpResponse

from django.shortcuts import render, redirect

from django.urls import reverse

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


from authentication.models import Guest, User
from authentication.forms import GuestForm
from authentication.utils import token_generator


def create_guest(request, *args, **kwargs):
    form = GuestForm()

    if request.method == 'POST':
        form = GuestForm(request.POST)

        if form.is_valid():
            user = User.objects.get_or_create(email=form.cleaned_data['email'])
            user[0].is_active = False
            user[0].save()

            # This is the email validation to make the user active
            domain = get_current_site(request).domain

            uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
            token = token_generator.make_token(user[0])

            link = reverse('authentication:authenticate_guest', kwargs={'uidb64': uidb64, 'token': token})
            activate_url = f'http://{domain}{link}'

            mail_subject = 'Activate your account and become our Guest'

            first_name = form.cleaned_data.get('first_name')
            mail_body = f'Hello {first_name}, click this link to activate your account. {activate_url}'
            mail_from = 'noreply@hotelapp.com'

            if settings.DEBUG:
                mail_to = ['admin@example.com']
            else:
                mail_to = [form.cleaned_data['email']]

            mail = EmailMessage(mail_subject, mail_body, mail_from, mail_to)

            mail.send()

            login(request, user[0], backend='django.contrib.auth.backends.ModelBackend')
            Guest.objects.create(id=user[0].id, user=user[0], **form.cleaned_data)

            destination = request.POST.get('next')

            if destination:
                return redirect(destination)

            return HttpResponse('<h1>You Created a profile</h1>')

    context = {
        'form': form,
    }

    return render(request, 'authentication/create_guest.html', context)

def authenticate_guest(request, *args, **kwargs):
    return redirect('registration:homepage')
