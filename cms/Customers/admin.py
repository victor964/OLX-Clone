from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Buyer)
admin.site.register(Message)
admin.site.register(PostMessage)

