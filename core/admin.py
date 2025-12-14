from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Donation, Tracking

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'cpf', 'phone', 'is_staff')
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
