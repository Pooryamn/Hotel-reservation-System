from django.db import models
from django.conf import settings
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50,blank=False)
    lastname = models.CharField(max_length=70,blank=False)
    phone = models.CharField(max_length=15,blank=False)
    email = models.CharField(max_length=100,blank=False)
    national_id = models.CharField(max_length=10,blank=False)

    def __str__(self):
        return self.firstname + ' ' + self.lastname