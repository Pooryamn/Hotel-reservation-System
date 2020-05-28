from datetime import date, timedelta, datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Hotel, Room, Reserve
from .forms import HotelDatePickerForm


def hotel_reserve(request, id):
    error_message = False
    if request.method == "POST":
        # begin = request.POST['begin']
        # end = request.POST['end']
        # # Check if dates are valid
        # begin_test = begin.split('-')
        # end_test = end.split('-')
        # beginDate = datetime(int(begin_test[0]), int(begin_test[1]), int(begin_test[2]))
        # endDate = datetime(int(end_test[0]), int(end_test[1]), int(end_test[2]))
        # if beginDate >= endDate:
        #     error_message = 'تاریخ ها نامعتبر هستند.'
        form = HotelDatePickerForm(request.POST)
        if form.is_valid():
            begin = form.cleaned_data.get('begin')
            end = form.cleaned_data.get('end')
        else:
            begin = ''
            end = ''
            error_message = 'خظا'
    else:
        begin = date.today()
        end = date.today() + timedelta(days=3)
        form = HotelDatePickerForm(initial={'begin': begin, 'end':end})

    hotel = get_object_or_404(Hotel, id=id)
    if error_message == False:
        # print(begin, end)
        room_list = Room.objects.filter(hotel__id=id)
        avl_rooms = check_room(room_list, begin, end)
    # print(avl_rooms)
    else:
        avl_rooms = []

    return render(request, 'blog/hotel/reserve.html',
            {'hotel': hotel, 'rooms': avl_rooms,
             'error_message': error_message, 'form':form,
             'begin': begin, 'end': end})


def check_room(rl, begin, end):
    print(begin, end)
    avl_rooms = []
    for i in rl:
        temp = i.reserve_set.filter(beginDate__lte=begin, endDate__gt=begin)
        if temp.first() == None:
            temp = i.reserve_set.filter(beginDate__gt=begin)
            temp = temp.filter(beginDate__lt=end)
            if temp.first() == None:
                avl_rooms.append(i)

    return avl_rooms


@login_required
@require_http_methods(["POST"])
def complete_reserve(request):
    checked_rooms = request.POST.getlist('checked_rooms')
    hotel_id = request.POST['hotel_id']
    
    if checked_rooms:
        # print(checked_rooms)
        begin = request.POST['begin']
        end = request.POST['end']

        begin_test = begin.split('-')
        end_test = end.split('-')
        beginDate = datetime(int(begin_test[0]), int(begin_test[1]), int(begin_test[2]))
        endDate = datetime(int(end_test[0]), int(end_test[1]), int(end_test[2]))

        days = (endDate - beginDate).days
        # print(type(result.days), begin, end)
        # print(checked_rooms)
        total_price = 0
        room_list = []
        for room_id in checked_rooms:
            room = Room.objects.filter(id=room_id)[0]
            room_list.append(room)
            # print(room.price)
            total_price += room.price
        
        total_price = total_price*days
        # print(total_price)

        reserve = Reserve.objects.create(user=request.user, beginDate=beginDate,
                                         endDate=endDate, totalPrice=total_price)
        reserve.room.set(room_list)
        reserve.save()

        # print(reserve.trackingCode, reserve.room.all(), reserve.totalPrice)

        return HttpResponseRedirect(reverse('blog:reserve_factor', args=(reserve.trackingCode,)))

    else:
        return HttpResponseRedirect(reverse('blog:hotel_reserve', args=(hotel_id,)))


@login_required
def reserve_factor(request, tracking_code):
    reserve = get_object_or_404(Reserve, trackingCode=tracking_code)
    return render(request, 'blog/hotel/reserve_factor.html',
                 {'reserve': reserve})
