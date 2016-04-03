from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Author, Node, Post
#
# # Define an inline admin descriptor for Author model
# # which acts a bit like a singleton
# class AuthorInline(admin.StackedInline):
#     model = Author
#
# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = [AuthorInline, ]
#
# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)
    list_display = ['user', 'url']
    ordering = ['user']

class NodeAdmin(admin.ModelAdmin):
    list_display = ['url', 'username', 'password']
    ordering = ['url']

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    ordering = ['title']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(Post, PostAdmin)
