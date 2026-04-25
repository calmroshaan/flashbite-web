from django.shortcuts import render, redirect
from stores.models import Store
from django.contrib.auth.decorators import login_required
from reservations.models import Reservation
from stores.forms import StoreApplicationForm

def home(request):
    # Only show approved and active stores on the homepage
    stores = Store.objects.filter(is_approved=True, is_active=True)[:6]
    return render(request, 'core/home.html', {'stores': stores})

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
            return redirect('stores:owner_dashboard')
    else:
        form = StoreApplicationForm()

    return render(request, 'core/partner.html', {'form': form})
# --- REPLACED PARTNER VIEW TO HANDLE FORM SUBMISSION END ---