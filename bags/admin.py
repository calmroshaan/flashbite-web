from django.contrib import admin
from .models import SurpriseBag

@admin.register(SurpriseBag)
class SurpriseBagAdmin(admin.ModelAdmin):
    list_display = ('title', 'store', 'discounted_price', 'quantity_left', 'is_active')
    list_filter = ('is_active', 'store')