from django.conf import settings

from django.contrib import messages
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
from authentication.utils import token_generator, send_activation_email


def create_guest(request, *args, **kwargs):
    form = GuestForm()

    if request.method == 'POST':
        form = GuestForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(email=form.cleaned_data.get('email'))

            send_activation_email(request, user, form.cleaned_data.get('first_name'), request.POST.get('next'))

            Guest.objects.create(id=user.id, user=user, **form.cleaned_data)

            messages.success(request, 'An activation link has been sent to your mail')
            messages.info(request, 'Check your mail, click the link to continue')
            return render(request, 'authentication/mail_sent.html', {'first_name': form.cleaned_data.get('first_name')})

    context = {
        'form': form,
    }

    return render(request, 'authentication/create_guest.html', context)


def authenticate_guest(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_email_verified = True
        user.save()

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        messages.success(request, 'Your email has been verified!')

        destination = request.GET.get('next')
        if destination:
            return redirect(destination)

        return redirect(reverse('registration:homepage'))

    return render(request, 'authentication/activate_failed.html', {'user': user})
