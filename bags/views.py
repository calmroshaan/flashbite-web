from django.shortcuts import render
from django.utils import timezone
from .models import SurpriseBag

def bag_list(request):
    current_time = timezone.localtime().time()
    query = request.GET.get('area', '').strip()

    bags = SurpriseBag.objects.filter(
        quantity_left__gt=0,
        pickup_end__gt=current_time,
        store__is_approved=True,
        store__is_active=True,
    ).order_by('-id')

    if query:
        bags = bags.filter(store__area=query)

    return render(request, 'bags/bag_list.html', {
        'bags': bags,
        'query': query,
    })