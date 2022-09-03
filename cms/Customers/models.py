from asyncio.windows_events import NULL
from email.policy import default
from select import select
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone_no = models.CharField(max_length=12, null=True)
    date_created =models.DateTimeField(auto_now_add=True, null=True)
    profile_pic = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ] 
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    buyers = models.ManyToManyField(Buyer, related_name='buyers', blank=True)
    id_no = models.CharField(null=True, max_length=10)
    name = models.CharField(max_length=50, null=True)
    phone_no = models.CharField(null=True, max_length=12)
    gender = models.CharField(choices=SEX_CHOICES, max_length=1, null=True)
    residence = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    STATE = [
        ('N', 'New'),
        ('U', 'Used'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product_id = models.CharField(null=True, max_length=10)
    product_name = models.CharField(null=True, max_length=20)
    state = models.CharField(null=True, choices=STATE, max_length=1)
    price = models.FloatField(null=True, max_length=15)
    product_image = models.ImageField(default='mdb-favicon.ico', null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.product_name

class Message(models.Model):
    sender = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Customer, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.sender

class PostMessage(models.Model):
    sender = models.ForeignKey(Customer, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
