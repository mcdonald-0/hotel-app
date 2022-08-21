from django.contrib.auth import authenticate, login

from django.http import HttpResponse

from django.shortcuts import render, redirect

from authentication.models import Guest, User
from authentication.forms import GuestForm


def create_guest(request, *args, **kwargs):
    form = GuestForm()

    if request.method == 'POST':
        form = GuestForm(request.POST)

        if form.is_valid():
            user = User.objects.get_or_create(email=form.cleaned_data['email'])
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
