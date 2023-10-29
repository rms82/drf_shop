from rest_framework.permissions import BasePermission
 

class SendMailPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('accounts.send_mail'))