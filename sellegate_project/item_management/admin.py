# item_management/admin.py

from django.contrib import admin
from .models import Item, Purchase, Bid, Payment

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'seller', 'delegation_state', 'created_at', 'is_sold', 'is_visible')
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
    list_display = (
        'id',  # Unique ID
        'item',  # The item purchased
        'buyer',  # Buyer of the item
        'total_price',  # Total price of the purchase
        'created_at',  # When the payment was made
    )

    list_filter = ('buyer', 'item')  # Filters for admin list view
    search_fields = ('item__title', 'buyer__username')  # Searchable fields
    ordering = ('-created_at',)  # Default order (most recent first)

    fieldsets = (
        (None, {
            'fields': (
                'item',  # The item being purchased
                'buyer',  # The buyer
                'created_at',  # Display-only field
            ),
        }),
    )

    readonly_fields = ('created_at', 'total_price')  # Make total_price read-only


# @admin.register(Purchase)
# class PurchaseAdmin(admin.ModelAdmin):
#     list_display = ('id', 'item', 'quantity', 'total_price', 'purchase_date')
#     list_filter = ('purchase_date',)
#     search_fields = ('item__title', 'item__description', 'item__seller__username')
#     readonly_fields = ('id', 'total_price', 'purchase_date')
#     fieldsets = (
#         ('Purchase Details', {
#             # 'fields': ('buyer', 'item', 'quantity')
#             'fields': ('buyer', 'item')

#         }),
#     )
    




admin.site.register(Bid)
