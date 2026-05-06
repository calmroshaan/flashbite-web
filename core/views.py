from django.shortcuts import render, redirect
from stores.models import Store
from django.contrib.auth.decorators import login_required
from reservations.models import Reservation
from stores.forms import StoreApplicationForm
from bags.models import SurpriseBag
# --- ADDED: Import Django's timezone tool to check the clock ---
from django.utils import timezone

# --- MARKETPLACE UPGRADE: Fetch available bags instead of just stores ---
def home(request):
    # 1. Get the exact current time right now
    current_time = timezone.localtime().time()
    
    # 2. Filter: Quantity > 0 AND pickup_end hasn't happened yet today
    available_bags = SurpriseBag.objects.filter(
        quantity_left__gt=0,
        pickup_end__gt=current_time
    ).order_by('-id')

    hero_bg = '/static/background-image.jpeg'
    
    return render(request, 'core/home.html', {'bags': available_bags, 'hero_bg': hero_bg})

@login_required
def dashboard(request):
    # Fetch all reservations for the logged-in user, newest first
    my_orders = Reservation.objects.filter(customer=request.user).order_by('-id')
    return render(request, 'core/dashboard.html', {'orders': my_orders})

# --- REPLACED PARTNER VIEW TO HANDLE FORM SUBMISSION START ---
@login_required
def partner(request):
    # FIXED: Changed 'user' to 'owner'
    if Store.objects.filter(owner=request.user).exists():
        return redirect('stores:owner_dashboard')

    if request.method == 'POST':
        form = StoreApplicationForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            # FIXED: Changed 'user' to 'owner'
            store.owner = request.user
            store.is_approved = False
            store.save()
            # FIX: Promote user to store_owner so Vendor Dashboard appears in navbar
            request.user.role = 'store_owner'
            request.user.save()
            return redirect('stores:owner_dashboard')
    else:
        form = StoreApplicationForm()

    return render(request, 'core/partner.html', {'form': form})
# --- REPLACED PARTNER VIEW TO HANDLE FORM SUBMISSION END ---