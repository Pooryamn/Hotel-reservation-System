from django.contrib import admin
from .models import Reserve, Hotel, HotelPicture, Room, Score

class ReserveAdmin(admin.ModelAdmin):
    list_display = ['trackingCode', 'beginDate', 'endDate', 'totalPrice', 'status']

class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'rooms', 'discount', 'phone']

class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'hotel', 'room_type', 'price']

class HotelPictureAdmin(admin.ModelAdmin):
    list_display = ['id', 'hotel']

class ScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'hotel', 'score']


admin.site.register(Hotel, HotelAdmin)
admin.site.register(Reserve, ReserveAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(HotelPicture, HotelPictureAdmin)
admin.site.register(Score, ScoreAdmin)
