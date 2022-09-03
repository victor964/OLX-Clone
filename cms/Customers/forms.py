from cProfile import label
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomerForm(ModelForm):
    class Meta():
        model = Customer
        fields = ['id_no','name','phone_no','gender','residence']
        label = {
            'id_no':'id number'
        }
        widgets = {
            'id_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID_No'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone_No.'}),
            'gender': forms.Select(attrs={'class': 'select'}),
            'residence': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Residence'}),
        }

class ProductForm(ModelForm):
    class Meta():
        model = Product
        fields = ['customer','product_id','product_name','state','price','product_image']
        widgets = {
            # 'customer': forms.Select(attrs={'class': 'select'}),
            'product_id': forms.TextInput(attrs={'class': 'form-control'}),
            'product_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Product Name'}),
            # 'state': forms.Select(attrs={'class':'select'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
        }

class BuyerUserForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['username','email','password1','password2']

class BuyerForm(ModelForm):
    class Meta():
        model = Buyer
        fields = '__all__'
        exclude = ['user']