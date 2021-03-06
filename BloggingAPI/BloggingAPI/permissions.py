from rest_framework import permissions

class AuthorPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Allow get requests for all
        if request.method == 'GET':
            return True
        else:
            return request.user == obj.user or request.user.is_staff

class PostPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Allow get requests for all but only owners to update and delete
        if request.method == 'PUT' or request.method == 'PATCH' or request.method == 'DELETE':
            return request.user == obj.author.user or request.user.is_staff
        else:
            return True

class NodePermissions(permissions.BasePermission):
    #only allow admins to add and remove nodes
    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH' or request.method == 'DELETE':
            return request.user.is_staff
        else:
            return True
