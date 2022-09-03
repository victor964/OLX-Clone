from email import message
import imp
from itertools import product
from multiprocessing import context
from operator import is_not
from urllib import response
from django.shortcuts import render, redirect
from .models import *
from .forms import *
import csv
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from .filter import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.decorators import login_required

# Create your views here.

@unauthenticated_user
def register(request):
    form = BuyerUserForm()
    if request.method == 'POST':
        form = BuyerUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
        
            group = Group.objects.get(name='Buyer')
            user.groups.add(group)

            Buyer.objects.create(user=user)

            messages.success(request, f'Buyer Account Successfully created for {username}')
            return redirect('/login')

    context = {'form':form}
    return render(request, 'registration.html', context)

@unauthenticated_user
def login_buyer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group == 'Customer':
                id = request.user.customer.id
                return redirect(f'/customerpage/{id}')
            if group == 'Admin':
                return redirect('/')
            else:
                return redirect('/buyerdashboard')
        else:
            messages.warning(request, f"Username or Password does not exist")

    context = {}
    return render(request, 'login.html', context)

@allowed_users(allowed_roles=['Buyer','Admin','Customer'])
def logout_buyer(request):
    logout(request)
    return redirect('/login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Buyer'])
def buyer_dashboard(request):
    product_pages = Product.objects.all()
    total_products = Product.objects.count()
    myfilter = ProductFilter(request.GET, queryset=product_pages)
    product_pages = myfilter.qs

    context = {'product_pages':product_pages, 'myfilter':myfilter, 'total_products':total_products}
    return render(request, 'buyer_dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Buyer'])
def buyer_account_settings(request):
    buyer = request.user.buyer
    form = BuyerForm(instance=buyer)
    if request.method == 'POST':
        form = BuyerForm(request.POST, request.FILES, instance=buyer)
        if form.is_valid():
            form.save()
            return redirect('/buyerdashboard')
    
    context = {'form':form}
    return render(request, 'buyer_account_settings.html', context)

def room(request, pk):
    customer = Customer.objects.get(id=pk)
    buyers = customer.buyers.all()
    for buyer in buyers:
        buyer_id = buyer.id
        buyer_name = buyer.name
    messages = Message.objects.get(id=buyer_id)
    all_messages = messages.sender.message_set.all()
    last_message = Message.objects.last()
    total_messages = Message.objects.count()
    # all_last_messages = last_message.sender.message_set.all()

    customer_message = PostMessage.objects.get(id=pk)
    post_messages = customer_message.sender.postmessage_set.all()
    if request.method == 'POST':
        message = PostMessage.objects.create(
            sender = request.user.customer,
            receiver = buyer_name,
            body = request.POST.get('body')
        )

    context = {'customer':customer, 'all_messages':all_messages, 'last_message':last_message,
    'total_messages':total_messages, 'post_messages':post_messages, 'buyers':buyers}
    return render(request, 'room.html', context)

@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()

    context = {'customers':customers}
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def add_customer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'add_customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Customer'])
def customer_page(request, pk):
    customer = Customer.objects.get(id=pk)
    products = customer.product_set.all()

    total_products = products.count()
    myfilter = ProductFilter(request.GET, queryset=products)
    products = myfilter.qs

    context = {'customer':customer, 'products':products, 'total_products':total_products, 'myfilter':myfilter}
    return render(request, 'customer_page.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def update_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form':form}
    return render(request, 'update_customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('/')

    context = {'customer':customer}
    return render(request, 'delete_customer.html', context)

def product_page(request, pk):
    product = Product.objects.get(id=pk)
    buyer_id = request.user.buyer.id
    messages = Message.objects.get(id=buyer_id)
    all_messages = messages.sender.message_set.all()
    if request.method == 'POST':
        message = Message.objects.create(
            sender = request.user.buyer,
            receiver = product.customer,
            body = request.POST.get('body')
        )
        return redirect('/buyerdashboard')

    context = {'product':product, 'all_messages':all_messages}
    return render(request, 'product_page.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def products(request, pk):
    customer = Customer.objects.get(id=pk)
    form = ProductForm(initial={'customer':customer})
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, initial={'customer':customer})
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'products.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'update_product.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def export_csv(request):
    current_date_time = datetime.now()
    response = HttpResponse(
        content_type = 'text/csv',
        headers = {'Content-Disposition': f'attachment; filename="customer_records {str(current_date_time)}.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['Id No.','Name','Phone No','Gender','Residence'])

    customers = Customer.objects.all()

    for customer in customers:
        writer.writerow([customer.id_no, customer.name, customer.phone_no, customer.gender, customer.residence])

    return response 

def export_pdf(request):
    return render(request, 'pdf_output.html')
