from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('registration/', views.register, name='register'),
    path('login/', views.login_buyer, name='login'),
    path('logout/', views.logout_buyer, name='logout'),

    path('buyerdashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('accountsettings/', views.buyer_account_settings, name='buyer_account_settings'),

    path('addcustomer/', views.add_customer, name='addcustomer'),
    path('updatecustomer/<str:pk>/', views.update_customer, name='updatecustomer'),
    path('deletecustomer/<str:pk>/', views.delete_customer, name='deletecustomer'),

    path('customerpage/<str:pk>/', views.customer_page, name='customer_page'),
    path('room/<str:pk>/', views.room, name='room'),

    path('exportcsv/', views.export_csv, name='export_csv'),
    path('pdf_output/', views.export_pdf, name='pdf_output'),

    path('products/<str:pk>/', views.products, name='products'),
    path('updateproduct/<str:pk>/', views.update_product, name='update_product'),
    path('productpage/<str:pk>/', views.product_page, name='product_page')
]