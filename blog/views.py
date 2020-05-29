from datetime import date, timedelta, datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
# from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Hotel, Room, Reserve
from .forms import HotelDatePickerForm


@login_required
def hotel_reserve(request, id):
    error_message = None
    if request.method == "POST":
        ### if request came from form1
        if request.POST['form_select'] == 'form1':
            form = HotelDatePickerForm(request.POST)
            if form.is_valid():
                begin = form.cleaned_data.get('begin')
                end = form.cleaned_data.get('end')
            else:
                begin = ''
                end = ''
                error_message = 1
        ### if request came from form2
        elif request.POST['form_select'] == 'form2':
            reserve, begin, end, error_message = make_reserve(request)
            if error_message == None:
                return HttpResponseRedirect(reverse('blog:reserve_factor', args=(reserve.trackingCode,)))
            else:
                form = HotelDatePickerForm(initial={'begin': begin, 'end':end})
    ### if GET request
    else:
        begin = date.today()
        end = date.today() + timedelta(days=3)
        form = HotelDatePickerForm(initial={'begin': begin, 'end':end})

    hotel = get_object_or_404(Hotel, id=id)
    ### if error is from form1 do not show available rooms
    avl_rooms = []
    if error_message != 1:
        room_list = Room.objects.filter(hotel__id=id)
        avl_rooms = check_room(room_list, begin, end)

    return render(request, 'blog/hotel/reserve.html',
            {'hotel': hotel, 'rooms': avl_rooms,
             'error_message': error_message, 'form':form,
             'begin': begin, 'end': end})


def check_room(rl, begin, end):
    avl_rooms = []
    for i in rl:
        temp = i.reserve_set.filter(beginDate__lte=begin, endDate__gt=begin)
        if temp.first() == None:
            temp = i.reserve_set.filter(beginDate__gt=begin)
            temp = temp.filter(beginDate__lt=end)
            if temp.first() == None:
                avl_rooms.append(i)

    return avl_rooms


def make_reserve(request):
    reserve = None
    error_message = None

    selected_rooms = request.POST.getlist('selected_rooms')
    hotel_id = request.POST['hotel_id']

    ### make date objects
    begin = request.POST['begin']
    end = request.POST['end']
    begin_test = begin.split('-')
    end_test = end.split('-')
    begin = datetime(int(begin_test[0]), int(begin_test[1]), int(begin_test[2]))
    end = datetime(int(end_test[0]), int(end_test[1]), int(end_test[2]))
    
    if selected_rooms:
        room_list = Room.objects.filter(hotel__id=hotel_id)
        avl_rooms = check_room(room_list, begin, end)
        avl_rooms = [str(i.id) for i in avl_rooms]
        ### Check if selected rooms still available or not
        if all(elem in avl_rooms  for elem in selected_rooms):
            ### Create Reserve
            days = (end - begin).days

            total_price = 0
            room_list = []
            for room_id in selected_rooms:
                room = Room.objects.filter(id=room_id)[0]
                room_list.append(room)
                total_price += room.price
            
            total_price = total_price*days

            ### calculate discount
            hotel = get_object_or_404(Hotel, id=hotel_id)
            total_price = (total_price*(100 - hotel.discount))/100

            reserve = Reserve.objects.create(user=request.user, beginDate=begin,
                                             endDate=end, totalPrice=total_price)
            reserve.room.set(room_list)
            reserve.save()
        else:
            ### if selected rooms are not available
            error_message = "اتاق های انتخابی در دسترس نمیباشد."

    else:
        ### if no rooms were selected
        error_message = "اتاقی انتخاب نشده است."

    return reserve, begin, end, error_message


@login_required
def reserve_factor(request, tracking_code):
    reserve = get_object_or_404(Reserve, trackingCode=tracking_code)
    return render(request, 'blog/hotel/reserve_factor.html',
                 {'reserve': reserve})
