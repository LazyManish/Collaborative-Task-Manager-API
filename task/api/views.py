from rest_framework import viewsets
from .permissions import IsGroupMember
from rest_framework.exceptions import PermissionDenied
from .serializers import TaskSerializer
from group.models import Membership
from task.models import TaskModel


class TaskViewSet(viewsets.ModelViewSet):

    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsGroupMember]


    def get_queryset(self):

        user = self.request.user
        group_id = self.kwargs.get('group_id')


        if user.is_authenticated and Membership.objects.filter(user = user, group_id = group_id, role = 'admin').exists():
            return TaskModel.objects.filter(group_id=group_id)
        
        else:
            return TaskModel.objects.filter(group_id=group_id)
        

        
    def perform_create(self, serializer):
        
        group_id = self.kwargs.get('group_id')
       
        if not Membership.objects.filter(user=self.request.user, group_id=group_id, role='admin').exists():
            raise PermissionDenied("Only admins can create tasks.")
        
       
        serializer.save(group_id=group_id)  

    
    def update(self, request, *args, **kwargs):
       
        task = self.get_object()  

        group_id = task.group_id 

        if not Membership.objects.filter(user=request.user, group_id=group_id).exists():
            raise PermissionDenied("You are not a member of this group and cannot modify this task.")

        return super().update(request, *args, **kwargs)