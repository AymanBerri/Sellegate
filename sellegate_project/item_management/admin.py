# item_management/admin.py

from django.contrib import admin
from .models import Item, Purchase, Bid, Payment

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'seller', 'evaluator', 'delegation_state', 'created_at', 'is_sold', 'is_visible')
    list_filter = ('delegation_state', 'seller', 'is_sold', 'is_visible')
    search_fields = ('title', 'description', 'seller__username')
    readonly_fields = ('id', 'created_at')  # `created_at` is read-only, set by the system
    
    fieldsets = (
        ('Item Details', {
            'fields': (
                'id',
                'title',
                'description',
                'price',
                'thumbnail_url',
                'seller',
                'evaluator',
                'delegation_state',
                'created_at',  # Include creation timestamp
                'is_sold',  # Indicate if the item is sold
                'is_visible',  # Indicate if the item is visible to buyers
            )
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Payment model.
    """
    list_display = ['id', 'item', 'buyer', 'total_price', 'created_at']  # Fields to display
    list_filter = ['created_at']  # Filter by creation date
    search_fields = ['item__title', 'buyer__username']  # Search by item title or buyer username
    readonly_fields = ['created_at', 'total_price']  # Fields that are read-only



    




# admin.site.register(Bid)
