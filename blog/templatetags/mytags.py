from django import template

register = template.Library()

@register.filter
def room_numbers(reserve):
    rooms = reserve.room.values_list('room_number', flat=True)
    return ' - '.join(str(x) for x in rooms)


@register.filter
def myrange(number):
    number = int(number)
    return list(range(number))


@register.filter
def hotelstar(number):
    number = int(number)
    star = []

    for i in range(1, 6):
        if i <= number:
            star.append(1)
        else:
            star.append(0)

    return star

@register.simple_tag
def cal_discount(price, discount):
    return (price * (100 - discount)) / 100


@register.filter
def hotel_picture(hotel):
    return hotel.hotel_pictures.first().picture.url

