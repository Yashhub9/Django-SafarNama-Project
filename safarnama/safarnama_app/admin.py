from django.contrib import admin
from .models import product, cart, orders, Itinerary
from django.contrib import admin
from .models import Contact

# Inline for Itinerary
class ItineraryInline(admin.TabularInline):
    model = Itinerary
    extra = 1  # Number of blank itinerary rows to display

# Product Admin with Itinerary Inline
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'original_price', 'price', 'pdetails', 'duration', 'is_active', 'notes']
    inlines = [ItineraryInline]

# Cart Admin
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'uid', 'pid']

# Order Admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'uid', 'pid']

# Register models
admin.site.register(cart, CartAdmin)
admin.site.register(product, ProductAdmin)  # Use combined ProductAdmin
admin.site.register(orders, OrderAdmin)


# admin.py


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at')
    search_fields = ('name', 'email')
    list_filter = ('submitted_at',)

