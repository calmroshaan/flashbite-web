from django.contrib import admin
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'category', 'is_approved', 'is_active')
    list_filter = ('is_approved', 'is_active', 'category')
    search_fields = ('name', 'city')
    prepopulated_fields = {'slug': ('name',)}