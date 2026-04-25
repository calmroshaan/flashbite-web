from django.shortcuts import render, get_object_or_404, redirect, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from bags.models import SurpriseBag
from .models import Reservation

@login_required
def reserve_bag(request, bag_id):
    # Find the specific bag the user clicked
    bag = get_object_or_404(SurpriseBag, id=bag_id, is_active=True)

    # Security check: Make sure there are actually bags left!
    if bag.quantity_left > 0:
        # 1. Create the reservation ticket
        reservation = Reservation.objects.create(
            customer=request.user,
            bag=bag,
            store=bag.store,
            quantity=1,
            total_price=bag.discounted_price,
            pickup_date=timezone.now().date()
        )
        
        # 2. Decrease the store's inventory by 1
        bag.quantity_left -= 1
        bag.save()

        # 3. Send them to their digital ticket
        messages.success(request, "Surprise Bag reserved successfully!")
        return redirect('reservations:ticket', pk=reservation.pk)
    
    else:
        messages.error(request, "Sorry, someone just bought the last one!")
        return redirect('stores:store_detail', slug=bag.store.slug)

@login_required
def reservation_ticket(request, pk):
    # Show the digital receipt and QR code, but ONLY if it belongs to this logged-in user
    reservation = get_object_or_404(Reservation, pk=pk, customer=request.user)
    return render(request, 'reservations/ticket.html', {'reservation': reservation})

@login_required
def confirm_pickup(request, pk):
    # Find the reservation, but strictly ensure it belongs to a store THIS user owns!
    reservation = get_object_or_404(Reservation, pk=pk, store__owner=request.user)
    
    # Change the status
    reservation.status = 'picked_up'
    reservation.save()
    
    messages.success(request, f"Order {reservation.reservation_code} marked as Picked Up!")
    return redirect('stores:owner_dashboard')