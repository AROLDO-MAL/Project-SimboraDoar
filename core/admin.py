from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Donation, Tracking, Feedback, Community

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'cpf', 'phone', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Extras', {'fields': ('cpf', 'phone')}),
    )

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'total_value', 'status', 'created_at')
    list_filter = ('status', 'type', 'created_at')
    search_fields = ('user__username', 'id')

@admin.register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    list_display = ('donation', 'current_status', 'latitude', 'longitude', 'last_update')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('created_at',)

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')
    search_fields = ('name',)

