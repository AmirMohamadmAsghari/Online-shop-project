from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,  Address


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'phone', 'is_staff','date_joined')
    search_fields = ('email', 'username', 'phone')
    #list_filter = 'is_staff'
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'phone', 'name')}),
        ('Permissions', {'fields': ('is_staff', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'username', 'phone', 'name', 'is_staff', 'is_active')}
         ),
    )

    # def role_name(self, obj):
    #     return obj.role.name if obj.role else '-'


admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(UserRole)


# class PermissionAdmin(admin.ModelAdmin):
#     list_display = ('action', 'role')
#     search_fields = ('action', 'role__name')
#

class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'postal_code', 'city', 'province')
    search_fields = ('user__email', 'name', 'postal_code')
    #list_filter = ('city', 'province')

admin.site.register(Address, AddressAdmin)
# admin.site.register(CustomPermission, PermissionAdmin)