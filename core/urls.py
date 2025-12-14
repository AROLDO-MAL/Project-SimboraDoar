from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    
    path('donate/', views.donate_options, name='donate_options'),
    path('donate/premade/', views.donate_premade, name='donate_premade'),
    path('donate/custom/', views.donate_custom, name='donate_custom'),
    path('payment/<uuid:donation_id>/', views.payment, name='payment'),
    path('tracking/<uuid:donation_id>/', views.tracking, name='tracking'),
    path('my-donations/', views.my_donations, name='my_donations'),
]
