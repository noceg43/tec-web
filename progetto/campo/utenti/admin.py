from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.admin import ModelAdmin

# Register your models here.


class GroupAdmin(ModelAdmin):
    actions = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class UserAdmin(ModelAdmin):
    actions = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
