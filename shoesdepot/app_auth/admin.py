from django.contrib import admin
from .models import AppUser, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class AppUserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]


admin.site.register(AppUser, AppUserAdmin)
