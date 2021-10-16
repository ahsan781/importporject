from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE  
# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, primary_key=True)
    email = models.EmailField()
 

class Vendor_profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="vendor_profile")
    name = models.CharField(max_length=100)


class Members(models.Model):
    vendor_profile = models.ForeignKey(Vendor_profile, on_delete=CASCADE, related_name="members")
    name = models.CharField(max_length=100)




class CsvSavedData(models.Model):
    #user = models.ForeignKey(Vendor_profile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    mobile = models.CharField(max_length=50,blank=True)
    address = models.TextField(blank=True)
    suburb = models.CharField(max_length=100,blank=True)
    state = models.TextField(blank=True)
    postal = models.IntegerField(blank=True)
    gender = models.CharField(max_length=20,blank=True)
    DOB = models.DateField()


