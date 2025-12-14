from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    
    path('donate/', views.donate_options, name='donate_options'),
    path('donate/premade/', views.donate_premade, name='donate_premade'),
    path('donate/custom/', views.donate_custom, name='donate_custom'),
    path('payment/<uuid:donation_id>/', views.payment, name='payment'),
    path('donate/choose-community/<uuid:donation_id>/', views.choose_community, name='choose_community'),
    path('tracking/<uuid:donation_id>/', views.tracking, name='tracking'),
    path('my-donations/', views.my_donations, name='my_donations'),
    path('profile/', views.profile, name='profile'),
    path('sobre/', views.about, name='about'),
    path('natal-solidario/', views.natal_solidario, name='natal_solidario'),
    path('donate/christmas/', views.donate_christmas, name='donate_christmas'),

    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Manual Tracking
    path('admin/tracking/<uuid:donation_id>/', views.admin_tracking, name='admin_tracking'),
    path('api/update-location/<uuid:donation_id>/', views.update_location, name='update_location'),
    path('api/get-location/<uuid:donation_id>/', views.get_location, name='get_location'),

    # Feedback
    path('feedback/delete/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
]
