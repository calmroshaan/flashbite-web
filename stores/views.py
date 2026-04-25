from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Store
from bags.models import SurpriseBag
from django.contrib.auth.decorators import login_required
from reservations.models import Reservation
from django.contrib import messages
from bags.forms import SurpriseBagForm

def store_detail(request, slug):
    # Fetch the store, but ONLY if it is approved and active
    store = get_object_or_404(Store, slug=slug, is_approved=True, is_active=True)
    
    # Get the exact current time in Pakistan
    current_time = timezone.localtime().time()
    
    # Fetch active bags, but ONLY if the pickup window hasn't ended yet
    bags = store.bags.filter(is_active=True, pickup_end__gte=current_time)
    
    return render(request, 'stores/store_detail.html', {
        'store': store, 
        'bags': bags
    })

from django.db.models import Q

def store_list(request):
    # Grab what they typed in the search bar
    query = request.GET.get('city', '')
    
    if query:
        # Search city OR address OR store name at the same time
        stores = Store.objects.filter(
            Q(city__icontains=query) | 
            Q(address__icontains=query) | 
            Q(name__icontains=query),
            is_approved=True, 
            is_active=True
        ).distinct()
    else:
        # If no search, just show all approved stores
        stores = Store.objects.filter(is_approved=True, is_active=True)
        
    return render(request, 'stores/store_list.html', {'stores': stores, 'query': query})

@login_required
def owner_dashboard(request):
    # FIXED: Changed 'user' to 'owner'
    store = Store.objects.filter(owner=request.user).first()

    # --- ADDED WAITING ROOM INTERCEPT LOGIC START ---
    if not store:
        return redirect('core:partner')

    if not store.is_approved:
        return render(request, 'stores/waiting_room.html')
    # --- ADDED WAITING ROOM INTERCEPT LOGIC END ---
        
    # Get all reservations for this store, newest first
    reservations = Reservation.objects.filter(store=store).order_by('-id')
    
    return render(request, 'stores/owner_dashboard.html', {
        'store': store,
        'reservations': reservations
    })

@login_required
def add_bag(request):
    # Verify the user actually owns a store
    store = Store.objects.filter(owner=request.user).first()
    if not store:
        messages.error(request, "Access Denied: You do not have an active vendor account.")
        return redirect('core:home')

    if request.method == 'POST':
        # request.FILES is required to capture the uploaded image!
        form = SurpriseBagForm(request.POST, request.FILES)
        if form.is_valid():
            bag = form.save(commit=False)
            bag.store = store # Link the bag to this specific vendor's store
            bag.quantity_available = bag.quantity_total
            bag.save()
            messages.success(request, "Your Surprise Bag is now live!")
            return redirect('stores:owner_dashboard')
    else:
        form = SurpriseBagForm()

    return render(request, 'stores/add_bag.html', {'form': form, 'store': store})

