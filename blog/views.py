from datetime import date, timedelta, datetime
from django.shortcuts import render, get_object_or_404
from .models import Hotel, Room
from .forms import HotelDatePickerForm


def hotel_detail(request, id):
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
            error_message = True
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

    return render(request, 'blog/hotel/detail.html',
            {'hotel': hotel, 'rooms': avl_rooms, 'error_message': error_message, 'form':form})


def check_room(rl, begin, end):
    avl_rooms = []
    for i in rl:
        temp = i.reserve_set.filter(beginDate__lt=begin, endDate__gt=begin)
        if temp.first() == None:
            temp = i.reserve_set.filter(beginDate__gt=begin)
            temp = temp.filter(beginDate__lt=end)
            if temp.first() == None:
                avl_rooms.append(i)

    return avl_rooms


