from django.contrib import admin

from bacheca.models import Post

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('messaggio', 'ora_creazione', 'immagine', 'autore')

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff


admin.site.register(Post, PostAdmin)
