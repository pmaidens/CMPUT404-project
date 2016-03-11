from rest_framework import permissions

class AuthorPermissions(permissions.BasePermission):

    #let admins do anything and allow everyone to GET
    def has_permission(self, request, view):
        if request.method == 'GET' or request.user.is_staff:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Allow get requests for all
        if request.method == 'GET':
            return True
        else:
            return request.user == obj.user
