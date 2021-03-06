from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
import uuid


# Create your models here.
def track_code_generator():
    return str(uuid.uuid4())[:8]


def hotel_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/hotel_<name>/<filename>
    if instance.__class__.__name__ == 'Hotel':
        return 'hotel_{0}/{1}'.format(instance.name, filename)
    else:
        return 'hotel_{0}/{1}'.format(instance.hotel.name, filename)


class Hotel(models.Model):
    name = models.CharField(max_length=50)
    rating = models.SmallIntegerField()
    logo = models.ImageField(upload_to=hotel_directory_path, blank=True)
    address = models.TextField(max_length=255)
    description = models.TextField()
    phone = models.CharField(max_length=11)
    city = models.CharField(max_length=40)
    
    ordinary_rooms = models.IntegerField()
    ordinary_rooms_price = models.IntegerField()
    vip_rooms = models.IntegerField()
    vip_rooms_price = models.IntegerField()
    
    discount = models.IntegerField()

    def __str__(self):
        return  '{}'.format(self.name)

    def get_absolute_url(self):
        return reverse('blog:hotel_detail', args=[self.id])


def make_rooms(sender, **kwargs):
    if not Room.objects.filter(hotel=kwargs['instance']):
        ordinary_rooms          = kwargs['instance'].ordinary_rooms
        ordinary_rooms_price    = kwargs['instance'].ordinary_rooms_price
        vip_rooms               = kwargs['instance'].vip_rooms
        vip_rooms_price         = kwargs['instance'].vip_rooms_price

        for i in range(1, ordinary_rooms + vip_rooms + 1):
            if i<=ordinary_rooms:
                Room.objects.create(hotel=kwargs['instance'], room_number=i,
                                room_type='ordinary', price=ordinary_rooms_price)
            else:
                Room.objects.create(hotel=kwargs['instance'], room_number=i,
                                room_type='vip', price=vip_rooms_price)

post_save.connect(make_rooms, sender=Hotel)


class Room(models.Model):
    ROOM_TYPE_CHOICES = (
        ('vip', 'VIP'),
        ('ordinary', 'Ordinary'),
    )

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number = models.IntegerField()
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES, default='ordinary')
    price = models.IntegerField()

    def __str__(self):
        return  'Room {}-{}'.format(self.hotel.name, self.room_number)


class Reserve(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ManyToManyField(Room)
    beginDate       = models.DateField()
    endDate         = models.DateField()
    totalPrice      = models.IntegerField()
    trackingCode    = models.CharField(max_length=10, unique=True, default=track_code_generator)
    created         = models.DateTimeField(auto_now_add=True)
    status          = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')

    def __str__(self):
        return  '{}'.format(self.trackingCode)


class HotelPicture(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="hotel_pictures")
    picture = models.ImageField(upload_to=hotel_directory_path, null=False)

    def __str__(self):
        return  'Picture {}-{}'.format(self.hotel.name, self.id)


class Score(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    score = models.SmallIntegerField()
    description = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  'Score {1}-{0}'.format(self.hotel.name, self.user.username)

