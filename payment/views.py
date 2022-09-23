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

    payment = Payment.objects.get(guest=request.user.guest, room_information=booking_information, amount=booking_information.cost)

    payment_data = dict()
    payment_data['ref'] = payment.ref
    payment_data['paystack_public_key'] = settings.PAYSTACK_PUBLIC_KEY
    payment_data['guest_email'] = payment.guest.email
    payment_data['amount_value'] = payment.amount_value()
    payment_data['authorization_url'] = payment.authorization_url
    print(payment_data)

    form = PaymentForm()

    if request.method == "POST":
        form = PaymentForm(request.POST)

    context = {
        'room': room,
        'form': form,
        'booking_info': booking_information,
        'payment_data': payment_data,
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