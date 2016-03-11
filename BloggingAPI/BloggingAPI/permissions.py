from rest_framework import permissions

class AuthorPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Allow get requests for all
        if request.method == 'GET':
            return True
        else:
            return request.user == obj.user or request.user.is_staff
