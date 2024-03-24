# item_management/admin.py

from django.contrib import admin
from .models import Item, Bid

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'seller')
    search_fields = ('title', 'seller__username')

    
admin.site.register(Bid)
