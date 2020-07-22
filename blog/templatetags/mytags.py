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