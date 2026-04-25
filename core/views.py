from django.shortcuts import render
from stores.models import Store
from django.contrib.auth.decorators import login_required
from reservations.models import Reservation

def home(request):
    # Only show approved and active stores on the homepage
    stores = Store.objects.filter(is_approved=True, is_active=True)[:6]
    return render(request, 'core/home.html', {'stores': stores})

@login_required
def dashboard(request):
    # Fetch all reservations for the logged-in user, newest first
    my_orders = Reservation.objects.filter(customer=request.user).order_by('-id')
    return render(request, 'core/dashboard.html', {'orders': my_orders})

def partner(request):
    return render(request, 'core/partner.html')