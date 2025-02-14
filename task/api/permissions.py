from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from  group.models import Membership  

class IsGroupMember(permissions.BasePermission):
    
    def has_permission(self, request, view):
        
        if not request.user.is_authenticated:
            return False
        
        group_id = view.kwargs.get('group_id') 
        
        if not group_id:
            raise PermissionDenied("Group ID not provided.")
        
        if Membership.objects.filter(user=request.user, group_id=group_id).exists():
            return True
        
        raise PermissionDenied("You are not a member of this group.")

class IsGroupAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        group_id = view.kwargs.get('group_id')

        if Membership.objects.filter(user=request.user, group_id=group_id, role='admin').exists():
            return True

        raise PermissionDenied("You must be an admin to access this resource.")

