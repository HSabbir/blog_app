from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'name')
    list_filter = ('email', 'is_active', 'is_staff')
    ordering = ('-name',)
    list_display = ( 'email', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name')}),
        ('Permissions',
         {
             'fields': (
                 'is_active',
                 'is_staff',
                 'is_superuser',
                 'verified',
                 'groups',
                 'user_permissions'
             )
         }),
    )

    # fieldsets to add a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'name', 'password1', 'password2', 'is_active',
                'is_staff', 'verified',
                'groups', 'user_permissions')}
         ),
    )


admin.site.register(User, UserAdminConfig)
