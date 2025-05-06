from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'phonenumber', 'gender', 'dateofbirth', 'is_superuser')
    search_fields = ('email', 'name', 'phonenumber')
    list_filter = ('gender', 'is_superuser')
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'name', 'phonenumber', 'gender', 'dateofbirth', 'address', 'bio', 'profilepicture')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

# Register the CustomUser model with the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)