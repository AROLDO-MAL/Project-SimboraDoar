from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Donation, Tracking
import json

def index(request):
    return render(request, 'core/index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'core/login.html'

@login_required
def donate_options(request):
    return render(request, 'core/donate_options.html')

@login_required
def donate_premade(request):
    if request.method == 'POST':
        size = request.POST.get('size')
        volume_map = {'small': 50, 'medium': 100, 'large': 200}
        value = volume_map.get(size, 0)
        
        donation = Donation.objects.create(
            user=request.user,
            type='PREMADE',
            items=[f"Cesta {size}"],
            total_value=value,
            status='PENDING'
        )
        return redirect('payment', donation_id=donation.id)
    return render(request, 'core/donate_premade.html')

@login_required
def donate_custom(request):
    items_available = [
        {'id': 'arroz', 'name': 'Arroz 5kg', 'price': 20},
        {'id': 'feijao', 'name': 'Feijão 1kg', 'price': 8},
        {'id': 'oleo', 'name': 'Óleo', 'price': 5},
        {'id': 'macarrao', 'name': 'Macarrão', 'price': 4},
        {'id': 'acucar', 'name': 'Açúcar', 'price': 3},
    ]
    
    if request.method == 'POST':
        selected_items = []
        total = 0
        for item in items_available:
            qty = int(request.POST.get(f"qty_{item['id']}", 0))
            if qty > 0:
                selected_items.append({'name': item['name'], 'qty': qty, 'price': item['price']})
                total += qty * item['price']
        
        if total > 0:
            donation = Donation.objects.create(
                user=request.user,
                type='CUSTOM',
                items=selected_items,
                total_value=total,
                status='PENDING'
            )
            return redirect('payment', donation_id=donation.id)
            
    return render(request, 'core/donate_custom.html', {'items': items_available})

@login_required
def payment(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id, user=request.user)
    if request.method == 'POST':
        # Simulate payment success
        donation.status = 'PAID'
        donation.save()
        
        # Create initial tracking
        Tracking.objects.create(
            donation=donation,
            latitude=-23.550520, # Mock SP coordinates
            longitude=-46.633308,
            current_status="Pagamento confirmado! Cesta em separação."
        )
        
        return redirect('tracking', donation_id=donation.id)
        
    return render(request, 'core/payment.html', {'donation': donation})

@login_required
def tracking(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id, user=request.user)
    # Ensure tracking exists (it should if paid)
    try:
        tracking_info = donation.tracking
    except Tracking.DoesNotExist:
        tracking_info = None
        
    return render(request, 'core/tracking.html', {'donation': donation, 'tracking': tracking_info})

@login_required
def my_donations(request):
    donations = Donation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/my_donations.html', {'donations': donations})
