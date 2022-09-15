from django.conf import settings
from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse

from booking.models import Room, RoomBooking

from payment.forms import PaymentForm
from payment.models import Payment


def initiate_payment(request, *args, **kwargs):
    guest = request.user.guest

    hotel_slug = kwargs['hotel_slug']
    room_slug = kwargs['room_slug']
    room_type_slug = kwargs['room_type_slug']

    room = Room.objects.get(slug=room_slug, room_type__slug=room_type_slug, hotel__slug=hotel_slug)
    booking_information = RoomBooking.objects.filter(room_booked=room, guest=guest).first()
    amount = room.room_information.cost

    payment_object = Payment.objects.get(guest=request.user.guest, room_information=booking_information, amount=booking_information.cost)
    payment = model_to_dict(payment_object)
    payment['guest_email'] = payment_object.guest.email
    payment['paystack_public_key'] = settings.PAYSTACK_PUBLIC_KEY
    payment['amount_value'] = payment_object.amount_value()
    payment['redirect_url'] = f'verified/{payment_object.ref}'

    print(payment_object.amount_value())

    form = PaymentForm()

    if request.method == "POST":
        form = PaymentForm(request.POST)

    context = {
        'room': room,
        'form': form,
        'booking_info': booking_information,
        'payment': payment,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
    }

    return render(request, 'payment/initiate_payment.html', context)


def verified_payment(request, *args, **kwargs):
    ref = kwargs['ref']
    payment = get_object_or_404(Payment, ref=ref)
    payment.verified = True
    payment.save()

    return HttpResponse("<h1>The payment was verified</h1>")





# let currency = "NGN";
#             let ref = {{ payment.ref }}
#             let obj = {
#                 key = "{{ paystack_public_key }}",
#                 email = {{ payment.guest.email }},
#                 amount = {{ payment.amount }},
#                 ref = ref,
#                 callback = function(response) {
#                     window.location.href = {% url 'payment:verify_payment' payment.ref %}
#                 }
#             }
#             if (Boolean(currency)) {
#                 obj.currency = currency.toUpperCase();
#             }
#
#             var handler = PaystackPop.setup(obj);
#             handler.openIframe()