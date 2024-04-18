from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomPermission, CustomUser, UserRole


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'phone', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'username', 'phone')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'phone', 'name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'role', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'username', 'phone', 'name', 'is_staff', 'is_active', 'role')}
         ),
    )

    def role_name(self, obj):
        return obj.role.name if obj.role else '-'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserRole)


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('action', 'role')
    search_fields = ('action', 'role__name')


admin.site.register(CustomPermission, PermissionAdmin)