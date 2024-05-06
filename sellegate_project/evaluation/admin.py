from django.contrib import admin
from .models import EvaluatorProfile, EvaluationRequest, EvaluationRequest

# Register your models here.

@admin.register(EvaluationRequest)  # Use this decorator to register the model
class EvaluationRequestAdmin(admin.ModelAdmin):
    """
    Admin configuration for AssessmentRequest.
    """
    # List of fields to display in the admin interface
    list_display = ['id', 'item', 'evaluator', 'name', 'price', 'state', 'created_at']

    # Fields to search by in the admin interface
    search_fields = ['name', 'evaluator__username', 'item__title']  # Search by evaluator and item name

    # Fields to filter by in the admin interface
    list_filter = ['state', 'created_at']

    # Fields to be read-only in the admin interface
    readonly_fields = ['created_at']

    # Fields to be editable when creating or editing an instance
    fields = ['item', 'evaluator', 'name', 'message', 'price', 'state', 'created_at']

    # Default ordering for the admin interface
    ordering = ['-created_at']



admin.site.register(EvaluatorProfile)



# OLD \/\/\/\/\/\\/\/\/\/\\/\/\//\
