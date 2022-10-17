import json 

from django.conf import settings

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import EmailMessage

from django.http import HttpResponse, JsonResponse

from django.shortcuts import render, redirect

from django.urls import reverse

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.views.decorators.csrf import csrf_exempt

from authentication.models import Guest, User
from authentication.forms import GuestForm
from authentication.utils import token_generator, send_activation_email


def validate_first_name(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        first_name = data['first_name']

        if not str(first_name).isalnum():
            return JsonResponse({'name_error': 'First name should only contain alphabets or numbers!'}, status=400)
        if len(first_name) > 20:
            return JsonResponse({'name_error': 'First name is too long!'}, status=400)

        return JsonResponse({'name_valid': True})

def validate_last_name(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        last_name = data['last_name']

        if not str(last_name).isalnum():
            return JsonResponse({'name_error': 'Last name should only contain alphabets or numbers!'}, status=400)
        if len(last_name) > 20:
            return JsonResponse({'name_error': 'Last name is too long!'}, status=400)

        return JsonResponse({'name_valid': True})

def validate_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']

        if User.objects.filter(email=email).exists():
            return JsonResponse({'mail_error': 'Someone with this email already exists. Try another...!'}, status=409)

        return JsonResponse({'mail_valid': True})

def validate_phone_number(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone_number = data['phone_number']

        if Guest.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({'phone_number_error': 'Someone with this phone number already exists. Try another...!'}, status=409)
        if len(phone_number) != 11 and len(phone_number) != 14:
            current_length_of_phone_number = str(len(phone_number))
            return JsonResponse({'phone_number_error': 'Phone number should be either 11 characters long \'08012345678\' or 14 characters long \'+2348012345678\' ', 
                'length_of_string': f'You currently have {current_length_of_phone_number} characters'}, status=400)

        return JsonResponse({'phone_number_valid': True})


def create_guest(request, *args, **kwargs):
    form = GuestForm()

    data = {}

    if request.method == 'POST':
        form = GuestForm(request.POST)
        
        if request.is_ajax():
            if form.is_valid():
                user = User.objects.create_user(email=form.cleaned_data.get('email'))

                send_activation_email(request, user, form.cleaned_data.get('first_name'), request.POST.get('next'))

                data['name'] = form.cleaned_data.get('first_name')
                data['status'] = 'Ok'

                Guest.objects.create(id=user.id, user=user, **form.cleaned_data)

                messages.success(request, 'An activation link has been sent to your mail')
                messages.info(request, 'Check your mail, click the link to continue')
                # return JsonResponse(data)
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
    
        messages.success(request, f'Hello {request.user.guest.first_name}, Thank you for beign our guest')        
        messages.success(request, 'Your email has been verified!')

        destination = request.GET.get('next')
        if destination:
            return redirect(destination)

        return redirect(reverse('registration:homepage'))

    return render(request, 'authentication/activate_failed.html', {'user': user})


# Python3 code to remove whitespace
def remove(string):
    return string.replace(" ", "")
    
# Driver Program
string = ' g e e k '
print(remove(string))

