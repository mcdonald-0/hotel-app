from datetime import timedelta, date

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from booking.models import RoomBooking, Room, RoomType
from booking.forms import BookingARoomForm, CheckInARoomForm

from authentication.forms import GuestForm
from authentication.models import Guest, User

from registration.models import Hotel


def book_a_room(request, *args, **kwargs):
    hotel_slug = kwargs['hotel_slug']
    room_type_slug = kwargs['room_type_slug']
    hotel = Hotel.objects.get(slug=hotel_slug)

    # This logic makes sure the number of rooms the hotel has is equal to the number of rooms available in the dropdown
    if hotel.number_of_rooms == Room.objects.filter(hotel__name=hotel.name).count():
        pass
    else:
        # Room.objects.filter(hotel__name=hotel.name).delete()
        for i in range(hotel.number_of_rooms):
            Room.objects.get_or_create(hotel=hotel, room_number=i + 1)

    # This makes sure that if the number of booked room equals the number of rooms, no_rooms_available would be equals to True
    hotel.number_of_booked_rooms = Room.objects.filter(hotel__slug=hotel_slug, is_booked=True).count()
    if hotel.number_of_rooms == hotel.number_of_booked_rooms:
        hotel.no_rooms_available = True
    hotel.save()

    form = BookingARoomForm(slug=hotel_slug)

    if request.method == 'POST':

        form = BookingARoomForm(request.POST, slug=hotel_slug)

        if form.is_valid():

            if not request.user.is_authenticated:
                messages.warning(request, 'For you to book a room, we would need a few details about you!')
                return redirect(f'/create/guest/?next={request.path}')

            # This makes sure that the date a user wants to check in comes before the date a user wants to check out
            if form.cleaned_data['date_to_check_out'] - form.cleaned_data['date_to_check_in'] < timedelta(days=1):
                messages.error(request, 'Improperly configured dates')
                messages.info(request,
                              'Check the date you want to check in, make sure it is before the date you want to check out')
                return redirect('booking:book_a_room', hotel_slug=hotel_slug, room_type_slug=room_type_slug)

            # The entire logic here checks if the hotel has available rooms, if it does not, a hotel is not booked. if it does a hotel is booked and the number of rooms is incremented by one.
            if hotel.number_of_booked_rooms < hotel.number_of_rooms:
                hotel.no_rooms_available = False
                if hotel.no_rooms_available == False:
                    hotel.number_of_booked_rooms += 1
                    hotel.save()
                    # This creates a room booking object then get the room a user books and updates the room_information
                    RoomBooking.objects.create(hotel=hotel, guest=request.user, **form.cleaned_data)
                    try:
                        RoomBooking.objects.get(hotel=hotel, guest=request.user, **form.cleaned_data)
                    except RoomBooking.MultipleObjectsReturned:
                        messages.error(request, 'You already booked this room!')

                    room_booking = RoomBooking.objects.get(hotel=hotel, guest=request.user, **form.cleaned_data)
                    room_number = room_booking.room_booked.room_number
                    Room.objects.filter(room_number=room_number, hotel=hotel).update(room_information=room_booking,
                                                                                     is_booked=True)

                    room = Room.objects.get(room_number=room_number, hotel__name=hotel)
                    return redirect('booking:check_in', hotel_slug=hotel_slug, room_type_slug=room_type_slug,
                                    room_slug=room.slug)

            else:
                hotel.no_rooms_available = True
                hotel.number_of_booked_rooms = hotel.number_of_rooms
                hotel.save()
                if hotel.no_rooms_available == True:
                    return HttpResponse('<h1>This hotel is maximally booked...</h1>')

    context = {
        'hotel': hotel,
        'form': form,
        'room_type_slug': room_type_slug,
    }

    return render(request, 'booking/booking.html', context)


def check_in(request, *args, **kwargs):
    hotel_slug = kwargs['hotel_slug']
    room_slug = kwargs['room_slug']
    room_type_slug = kwargs['room_type_slug']
    room = Room.objects.get(slug=room_slug, room_type__slug=room_type_slug, hotel__slug=hotel_slug)

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
        'room_slug': room_slug
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
    for i in RoomBooking.objects.filter(date_to_check_out__lt=today):
        room = Room.objects.get(room_information=i)
        room.is_booked = False
        room.checked_in = False
        room.save()

    context = {
        'hotel': hotel,
        'room_types': hotel_room_types,
    }
    return render(request, 'booking/view_rooms.html', context)


def specific_room_booking(request, *args, **kwargs):
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
        messages.warning(request, 'It seems you have created a profile before but some error occurred')
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
                    # Todo: i need to create a user platform where a user can see list of their booked hotels then i would redirect them there from here
                    # room = Room.objects.get(room_information=booking, hotel=hotel, room_type__slug=room_type_slug, is_booked=True)
                    messages.warning(request, 'You have already booked this room with this same dates')
                    return redirect('booking:book_a_room', hotel_slug=hotel_slug, room_type_slug=room_type_slug)

            except RoomBooking.DoesNotExist:
                RoomBooking.objects.create(hotel=hotel, guest=request.user.guest, room_type=room_type,
                                           **form.cleaned_data)

            # This gets the room booked and updates the room information to the room booking object created above
            room_booking = RoomBooking.objects.get(hotel=hotel, guest=request.user.guest, room_type=room_type,
                                                   **form.cleaned_data)
            room_number = room_booking.room_booked.room_number
            Room.objects.filter(room_number=room_number, room_type__slug=room_type_slug, hotel=hotel).update(
                room_information=room_booking, is_booked=True)

            room = Room.objects.get(room_number=room_number, room_type__slug=room_type_slug, hotel=hotel)
            return redirect('booking:check_in', hotel_slug=hotel_slug, room_type_slug=room_type_slug,
                            room_slug=room.slug)

    context = {
        'hotel': hotel,
        'form': form,
        'room_type_slug': room_type_slug,
    }
    return render(request, 'booking/booking.html', context)

# Todo: I need to create a view that shows all the rooms i have booked and i have checked into.
