# item_management/admin.py

from django.contrib import admin
from .models import Item, Purchase, Bid

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'seller', 'delegation_state')
    list_filter = ('delegation_state', 'seller')
    search_fields = ('title', 'description', 'seller__username')
    readonly_fields = ('id',)
    fieldsets = (
        ('Item Details', {
            'fields': ('id', 'title', 'description', 'price', 'thumbnail_url', 'seller', 'delegation_state')
        }),
    )

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'quantity', 'total_price', 'purchase_date')
    list_filter = ('purchase_date',)
    search_fields = ('item__title', 'item__description', 'item__seller__username')
    readonly_fields = ('id', 'total_price', 'purchase_date')
    fieldsets = (
        ('Purchase Details', {
            'fields': ('id', 'item', 'quantity', 'total_price', 'purchase_date')
        }),
    )
    
admin.site.register(Bid)
