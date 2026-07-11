from django.contrib import admin
from .models import ContactMessage, GymPlan, GymNotice  # Saare models ek hi baar mein import kar liye

# 1. Contact Message Admin Configuration
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')

# 2. Gym Plan Register
admin.site.register(GymPlan)

# 3. Gym Notice Register
admin.site.register(GymNotice)