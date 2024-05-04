from django.contrib import admin
from .models import EvaluatorProfile, EvaluationRequest

# Register your models here.
admin.site.register(EvaluatorProfile)
admin.site.register(EvaluationRequest)