from django.contrib import admin
from .models import CustomerFeedback
# Register your models here.


@admin.register(CustomerFeedback)
class CustomerFeedbackAdmin(admin.ModelAdmin):
    list_display = ('platform', 'message', 'sentiment', 'submitted_at')
    list_filter = ('platform', 'sentiment')
    search_fields = ('message',)