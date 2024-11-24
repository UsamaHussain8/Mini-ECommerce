from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import StoreUser

class StoreUserInline(admin.StackedInline):
    model = StoreUser
    can_delete = False
    verbose_name_plural = 'StoreUsers'
    
class StoreUserAdmin(admin.ModelAdmin):
    inlines = (StoreUserInline, )
    class Meta:
        verbose_name_plural = "Users"

admin.site.unregister(User)
admin.site.register(User, StoreUserAdmin)