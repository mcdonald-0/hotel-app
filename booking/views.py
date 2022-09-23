from datetime import timedelta, date

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from booking.models import RoomBooking, Room, RoomType
from booking.forms import BookingARoomForm, CheckInARoomForm

from authentication.models import User

from registration.models import Hotel

from payment.models import Payment


def book_a_room(request, *args, **kwargs):
    hotel_slug = kwargs['hotel_slug']
    room_type_slug = kwargs['room_type_slug']

    hotel = Hotel.objects.get(slug=hotel_slug)
    room_type = RoomType.objects.get(hotel=hotel, slug=room_type_slug)

    for i in range(room_type.number_of_rooms):
        Room.objects.get_or_create(hotel=hotel, room_number=i + 1, room_type=room_type)

    room_type.number_of_booked_rooms = Room.objects.filter(hotel__slug=hotel_slug, room_type__slug=room_type_slug,
                                                           is_booked=True).count()
    room_type.save()

    form = BookingARoomForm(hotel_slug=hotel_slug, room_type_slug=room_type_slug)

    # This here checks if the user is an anonymous user
    if not request.user.is_authenticated:
        messages.warning(request, 'Before you proceed, we would need a few details about you!')
        messages.info(request, 'We need this so we can relate to you personally and also for your safety!')
        return redirect(f'/create/guest/?next={request.path}')

    # This checks if the user already has a user profile but no guest profile
    try:
        request.user.guest
    except User.guest.RelatedObjectDoesNotExist:
        messages.warning(request, 'Before you proceed, we would need a few details about you!')
        messages.warning(request, 'It seems you are a user but you are not yet a guest')
        messages.info(request, 'We need this so we can relate to you personally and also for your safety!')
        return redirect(f'/create/guest/?next={request.path}')

    if request.method == 'POST':

        form = BookingARoomForm(request.POST, hotel_slug=hotel_slug, room_type_slug=room_type_slug)

        if form.is_valid():

            # This makes sure that the date a user wants to check in comes before the date a user wants to check out
            if form.cleaned_data['date_to_check_out'] - form.cleaned_data['date_to_check_in'] < timedelta(days=1):
                messages.error(request, 'Improperly configured dates')
                messages.info(request,
                              'Check the date you want to check in, make sure it is before the date you want to check out')
                return redirect('booking:book_a_room', hotel_slug=hotel_slug, room_type_slug=room_type_slug)

            # This make sure that if a user books a room and still tries to book that same room within the same time range, it redirects the user to the booked room
            try:
                booking = RoomBooking.objects.get(hotel=hotel, guest=request.user.guest, room_type=room_type,
                                                  **form.cleaned_data)
                if booking:
                    # Todo: I need to redirect the users to the specific room booking url
                    # room = Room.objects.get(room_information=booking, hotel=hotel, room_type__slug=room_type_slug, is_booked=True)
                    messages.warning(request, 'You have already booked this room with the same dates')
                    return redirect('registration:activity_log', user_id=booking.guest.id)

            except RoomBooking.DoesNotExist:
                RoomBooking.objects.create(hotel=hotel, guest=request.user.guest, room_type=room_type,
                                           **form.cleaned_data)

            # This gets the room booked and updates the room information to the room booking object created above
            room_booking = RoomBooking.objects.get(hotel=hotel, guest=request.user.guest, room_type=room_type,
                                                   **form.cleaned_data)
            room_number = room_booking.room_booked.room_number

            # This creates a payment object from the information above
            Payment.objects.create(guest=request.user.guest, room_information=room_booking, amount=room_booking.cost)

            Room.objects.filter(room_number=room_number, room_type__slug=room_type_slug, hotel=hotel).update(
                room_information=room_booking, is_booked=True)

            room = Room.objects.get(room_number=room_number, room_type__slug=room_type_slug, hotel=hotel)

            return redirect('payment:initiate_payment', hotel_slug=hotel_slug, room_type_slug=room_type_slug,
                            room_slug=room.slug)

    context = {
        'hotel': hotel,
        'form': form,
        'room_type': room_type,
        'room_type_slug': room_type_slug,
    }
    return render(request, 'booking/booking.html', context)


def check_in(request, *args, **kwargs):
    hotel_slug = kwargs['hotel_slug']
    room_slug = kwargs['room_slug']
    room_type_slug = kwargs['room_type_slug']
    room = Room.objects.get(slug=room_slug, room_type__slug=room_type_slug, hotel__slug=hotel_slug)

    amount = room.room_information.cost

    form = CheckInARoomForm

    if request.method == 'POST':
        form = CheckInARoomForm(request.POST)
        if form.is_valid():
            room.checked_in = True
            room.save()

            return HttpResponse('<h1>Yeey! you checked into a room🎇</h1>')

    context = {
        'room': room,
        'form': form,
        'room_type_slug': room_type_slug,
        'room_slug': room_slug,
        'cost': amount
    }

    return render(request, 'booking/check_in.html', context)


def check_out(request, *args, **kwargs):
    room = Room.objects.get(slug=kwargs['room_slug'], hotel__slug=kwargs['hotel_slug'])

    room.checked_in = False
    room.is_booked = False
    room.save()

    return HttpResponse('<h1>Thank you for lodging with us... come back again</h1>')


def view_rooms(request, *args, **kwargs):
    hotel_slug = kwargs['hotel_slug']
    hotel = Hotel.objects.get(slug=hotel_slug)
    hotel_room_types = hotel.room_types.all()

    today = date.today()

    # This makes sure that if the date is less than today, is_booked and is_checked equals false
    for item in RoomBooking.objects.filter(date_to_check_out__lt=today):
        try:
            room = Room.objects.get(room_information=item)
            room.is_booked = False
            room.checked_in = False
            room.save()
        except Room.DoesNotExist:
            pass

    context = {
        'hotel': hotel,
        'room_types': hotel_room_types,
    }
    return render(request, 'booking/view_rooms.html', context)


# Todo: i need to create a more robust models and a slimmer views and put all the minor stuffs in the models
# Todo: i need to create a decorator that if a room is completely booked, it cannot be accessed from its url

