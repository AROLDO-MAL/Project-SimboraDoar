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


from django import forms

class TrackingAdminForm(forms.ModelForm):
    donation_status = forms.ChoiceField(choices=Donation.STATUS_CHOICES, label="Status da Doação")

    class Meta:
        model = Tracking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Populate initial value from related Donation
            self.fields['donation_status'].initial = self.instance.donation.status

    def save(self, commit=True):
        tracking = super().save(commit=False)
        if commit:
            tracking.save()  # Tracking must exist before we can rely on .donation relationship fully if new? Actually OneToOne needs donation set.
        
        # Update related Donation status
        if tracking.donation:
            tracking.donation.status = self.cleaned_data['donation_status']
            tracking.donation.save()
            
        return tracking

@admin.register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    form = TrackingAdminForm
    list_display = ('donation', 'donation_status_display', 'current_status', 'last_update')
    
    def donation_status_display(self, obj):
        return obj.donation.get_status_display()
    donation_status_display.short_description = "Status da Doação"

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('created_at',)

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')
    search_fields = ('name',)

