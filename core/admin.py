from django.contrib import admin
from .models import StoreUser

@admin.register(StoreUser)
class StoreUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email')
    class Meta:
        verbose_name_plural = "Users"
