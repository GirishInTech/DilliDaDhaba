"""
accounts/admin.py

Placeholder – extend this when custom user models are added.
Currently re-exports the default User admin to ensure staff-only roles can be
managed easily from the Dilli Da Dhaba admin panel.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Re-register with the default UserAdmin (no changes needed yet)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
