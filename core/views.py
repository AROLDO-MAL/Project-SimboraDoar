from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .forms import CustomUserCreationForm, FeedbackForm
from .models import Donation, Tracking, Feedback, Community
import json

def index(request):
    # Feedback Submission
    if request.method == 'POST' and 'feedback_submit' in request.POST:
        if request.user.is_authenticated:
            feedback_form = FeedbackForm(request.POST)
            if feedback_form.is_valid():
                feedback = feedback_form.save(commit=False)
                feedback.user = request.user
                feedback.save()
                return redirect('index') # Prevent resubmission
        else:
            return redirect('login')
    else:
        feedback_form = FeedbackForm()

    # Data for Homepage
    total_donations = Donation.objects.filter(status__in=['PAID', 'DELIVERED']).count()
    display_count = total_donations if total_donations > 0 else 142
    
    feedbacks = Feedback.objects.all()[:6] # Show 6 latest

    context = {
        'total_donations': display_count,
        'feedbacks': feedbacks,
        'feedback_form': feedback_form
    }
    return render(request, 'core/index.html', context)

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
        # Alimentos Básicos
        {'id': 'arroz', 'name': 'Arroz 5kg', 'price': 20},
        {'id': 'feijao', 'name': 'Feijão 1kg', 'price': 8},
        {'id': 'oleo', 'name': 'Óleo', 'price': 5},
        {'id': 'macarrao', 'name': 'Macarrão', 'price': 4},
        {'id': 'acucar', 'name': 'Açúcar', 'price': 3},
        {'id': 'café', 'name': 'Café 250g', 'price': 12},
        {'id': 'leite', 'name': 'Leite em Pó 400g', 'price': 15},
        
        # Enlatados
        {'id': 'sardinha', 'name': 'Sardinha (Lata)', 'price': 6},
        {'id': 'milho', 'name': 'Milho Verde (Lata)', 'price': 4},
        {'id': 'goiabada', 'name': 'Doce de Goiaba 300g', 'price': 5},

        # Higiene Pessoal
        {'id': 'sabonete', 'name': 'Sabonete', 'price': 2.50},
        {'id': 'creme_dental', 'name': 'Creme Dental', 'price': 4},
        {'id': 'shampoo', 'name': 'Shampoo', 'price': 12},
        {'id': 'papel_higienico', 'name': 'Papel Higiênico (4un)', 'price': 5},
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
            latitude=-5.6622, # Apodi RN coordinates (Sede)
            longitude=-37.7989,
            current_status="Pagamento confirmado! Cesta em separação."
        )
        
        # Redirect to choose community
        return redirect('choose_community', donation_id=donation.id)
        
    return render(request, 'core/payment.html', {'donation': donation})

@login_required
def choose_community(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id, user=request.user)
    
    if request.method == 'POST':
        community_id = request.POST.get('community')
        if community_id:
            community = get_object_or_404(Community, id=community_id)
            donation.community = community
            donation.save()
            return redirect('tracking', donation_id=donation.id)
            
    communities = Community.objects.all()
    return render(request, 'core/choose_community.html', {
        'donation': donation,
        'communities': communities
    })

@login_required
def tracking(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id, user=request.user)
    
    # Enforce Community Selection
    if not donation.community:
        return redirect('choose_community', donation_id=donation.id)

    try:
        tracking = donation.tracking
    except Tracking.DoesNotExist:
        tracking = None
    
    # Coordinates for Sede (Apodi, RN)
    sede_coords = {
        'lat': -5.6622,
        'lng': -37.7989
    }
    
    context = {
        'donation': donation,
        'tracking': tracking,
        'sede_coords': sede_coords,
        'GOOGLE_MAPS_API_KEY': 'YOUR_GOOGLE_MAPS_API_KEY' # Placeholder
    }
    return render(request, 'core/tracking.html', context)

@login_required
def my_donations(request):
    donations = Donation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/my_donations.html', {'donations': donations})

@login_required
def profile(request):
    # Fetch summary data
    donations = Donation.objects.filter(user=request.user)
    total_donations = donations.count()
    last_donation = donations.order_by('created_at').last()
    
    context = {
        'total_donations': total_donations,
        'last_donation': last_donation,
    }
    return render(request, 'core/profile.html', context)

def about(request):
    return render(request, 'core/about.html')

def natal_solidario(request):
    """Landing page for the Natal Solidário campaign."""
    return render(request, 'core/natal_solidario.html')

@login_required
def donate_christmas(request):
    """Handle the specific Christmas Basket donation."""
    if request.method == 'POST':
        # Fixed value and items for the campaign
        value = 149.99
        items = [
            "Cesta Básica Completa",
            "Panetone/Bolo Natalino",
            "Caixa de Bombom",
            "Ave Natalina (Vale-Frango)"
        ]
        
        donation = Donation.objects.create(
            user=request.user,
            type='CHRISTMAS', # Keeping type distinct if model allows, or use PREMADE/CUSTOM
            items=items,
            total_value=value,
            status='PENDING'
        )
        return redirect('payment', donation_id=donation.id)
    
    # If GET, redirect to the landing page
    return redirect('natal_solidario')

# --- Manual Tracking Control ---

@user_passes_test(lambda u: u.is_staff)
def admin_tracking(request, donation_id):
    """Admin view to manually control truck location."""
    donation = get_object_or_404(Donation, id=donation_id)
    try:
        tracking = donation.tracking
    except Tracking.DoesNotExist:
        # Create default tracking if not exists
        tracking = Tracking.objects.create(
            donation=donation, 
            latitude=-5.6622, # Sede
            longitude=-37.7989
        )
    
    context = {
        'donation': donation,
        'tracking': tracking,
        'sede_coords': {'lat': -5.6622, 'lng': -37.7989}
    }
    return render(request, 'core/admin_tracking.html', context)

@require_POST
@user_passes_test(lambda u: u.is_staff)
def update_location(request, donation_id):
    """API to update truck location."""
    import json
    donation = get_object_or_404(Donation, id=donation_id)
    
    try:
        data = json.loads(request.body)
        lat = data.get('lat')
        lng = data.get('lng')
        
        if lat is None or lng is None:
            return JsonResponse({'success': False, 'error': 'Missing coordinates'}, status=400)

        tracking, created = Tracking.objects.get_or_create(donation=donation, defaults={
            'latitude': lat,
            'longitude': lng
        })
        
        tracking.latitude = lat
        tracking.longitude = lng
        tracking.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def get_location(request, donation_id):
    """API for user frontend to get current location."""
    donation = get_object_or_404(Donation, id=donation_id)
    try:
        tracking = donation.tracking
        return JsonResponse({
            'lat': tracking.latitude,
            'lng': tracking.longitude,
            'last_update': tracking.last_update.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Tracking.DoesNotExist:
        return JsonResponse({'error': 'Tracking not found'}, status=404)

@user_passes_test(lambda u: u.is_staff)
def delete_feedback(request, feedback_id):
    """Allow admins to delete specific feedback."""
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.delete()
    return redirect('index')
