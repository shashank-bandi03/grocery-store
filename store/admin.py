from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class UserModelAdmin(UserAdmin):
    list_display = ('id', 'email', 'is_admin')
    list_filter = ('id', 'email', 'is_admin')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'id')
    ordering = ('email', 'id')
    filter_horizontal = ()


admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Ratings)
admin.site.register(Reviews)
admin.site.register(Order)
admin.site.register(User, UserModelAdmin)
