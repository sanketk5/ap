from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    refer_code = models.CharField(max_length=10, blank=True, null=True)
    contact_no = models.CharField(max_length=50,blank=True, null=True)
    refer_order = models.IntegerField(default=0, blank=True, null=True)
    total_order = models.IntegerField(default=0, blank=True, null=True)
    #added_books = models.IntegerField(default=0, blank=True, null=True)