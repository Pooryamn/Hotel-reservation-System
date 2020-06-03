from django.db import models
from django.conf import settings
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15,blank=False)
    national_id = models.CharField(max_length=10,blank=False)

    def __str__(self):
        return self.national_id